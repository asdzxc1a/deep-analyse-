import re
from pathlib import Path

from deep_analysis.cartography import RepoMap
from deep_analysis.models import ArtifactType, WorkflowFinding


def analyze_workflows(repo_root: Path, repo_map: RepoMap) -> list[WorkflowFinding]:
    findings: list[WorkflowFinding] = []

    for artifact in repo_map.artifacts:
        if not artifact.is_meaningful:
            continue
        if artifact.artifact_type not in {
            ArtifactType.SKILL,
            ArtifactType.CI,
            ArtifactType.DOC,
            ArtifactType.PROMPT,
        }:
            continue

        file_path = repo_root / artifact.path
        content = file_path.read_text(encoding="utf-8")
        lines = _extract_analysis_lines(content)

        trigger_conditions: list[str] = []
        steps: list[str] = []
        decision_gates: list[str] = []
        hard_constraints: list[str] = []
        approval_gates: list[str] = []
        review_loops: list[str] = []
        escalation_paths: list[str] = []
        human_role: str | None = None
        agent_role: str | None = None

        if artifact.artifact_type is ArtifactType.SKILL:
            for line in lines:
                if line.startswith("description:"):
                    trigger_conditions.append(line.split(":", 1)[1].strip())
                else:
                    ordered_step = _extract_ordered_step(line)
                    if ordered_step:
                        steps.append(ordered_step)
                    elif line.lower().startswith("use when "):
                        trigger_conditions.append(line)
                    elif _looks_like_decision_gate(line):
                        decision_gates.append(line)
        elif artifact.artifact_type is ArtifactType.CI:
            trigger_conditions.append("workflow file present")
            steps.extend(_extract_ci_steps(lines))
            decision_gates.extend(_extract_ci_decision_gates(lines))
        else:
            trigger_conditions.extend(_extract_doc_triggers(lines))
            steps.extend(_extract_doc_steps(lines))

        hard_constraints = _extract_hard_constraints(lines)
        approval_gates = _extract_approval_gates(lines)
        review_loops = _extract_review_loops(lines)
        escalation_paths = _extract_escalation_paths(lines)
        human_role, agent_role = _infer_roles(artifact.artifact_type, lines, human_role, agent_role)
        reusable_patterns = _derive_reusable_patterns(
            hard_constraints=hard_constraints,
            approval_gates=approval_gates,
            review_loops=review_loops,
            escalation_paths=escalation_paths,
            human_role=human_role,
            agent_role=agent_role,
        )

        summary = _workflow_summary(artifact.path, artifact.artifact_type, steps)

        if trigger_conditions or steps or hard_constraints or approval_gates or review_loops:
            findings.append(
                WorkflowFinding(
                    path=artifact.path,
                    summary=summary,
                    trigger_conditions=trigger_conditions,
                    steps=steps,
                    decision_gates=decision_gates,
                    hard_constraints=hard_constraints,
                    approval_gates=approval_gates,
                    review_loops=review_loops,
                    escalation_paths=escalation_paths,
                    reusable_patterns=reusable_patterns,
                    human_role=human_role,
                    agent_role=agent_role,
                )
            )

    return findings


def _workflow_summary(path: str, artifact_type: ArtifactType, steps: list[str]) -> str:
    if artifact_type is ArtifactType.SKILL:
        return f"Skill workflow in {path} with {len(steps)} ordered step(s)."
    if artifact_type is ArtifactType.CI:
        return f"Automation workflow in {path} that defines repository checks."
    if artifact_type is ArtifactType.PROMPT:
        return f"Prompt workflow in {path} with {len(steps)} extracted step(s)."
    return f"Documented workflow in {path}."


def _extract_ordered_step(line: str) -> str | None:
    match = re.match(r"^\d+\.\s+(.*)$", line)
    if match:
        return match.group(1).strip()
    return None


def _looks_like_decision_gate(line: str) -> bool:
    lowered = line.lower()
    return any(token in lowered for token in ("must", "if ", "when ", "unless", "required"))


def _extract_hard_constraints(lines: list[str]) -> list[str]:
    constraints: list[str] = []
    for line in lines:
        if _looks_like_hard_constraint(line):
            constraints.append(line)
    return _limit_unique(constraints, limit=8)


def _extract_approval_gates(lines: list[str]) -> list[str]:
    approval_gates: list[str] = []
    for line in lines:
        lowered = line.lower()
        if any(
            phrase in lowered
            for phrase in (
                "wait for user approval",
                "wait for the user's response",
                "user reviews",
                "user approval",
                "before approving",
                "before proceeding",
                "approval",
                "approved",
            )
        ):
            approval_gates.append(line)
    return _limit_unique(approval_gates, limit=8)


def _extract_review_loops(lines: list[str]) -> list[str]:
    review_loops: list[str] = []
    for line in lines:
        lowered = line.lower()
        if any(
            phrase in lowered
            for phrase in (
                "repeat until",
                "until approved",
                "re-dispatch",
                "re-review",
                "review loop",
                "loop exceeds",
            )
        ):
            review_loops.append(line)
    return _limit_unique(review_loops, limit=8)


def _extract_escalation_paths(lines: list[str]) -> list[str]:
    escalation_paths: list[str] = []
    for line in lines:
        lowered = line.lower()
        if any(
            phrase in lowered
            for phrase in (
                "escalate",
                "surface to human",
                "ask for help",
                "blocked",
                "stop",
                "exceeds",
                "operator",
            )
        ):
            escalation_paths.append(line)
    return _limit_unique(escalation_paths, limit=8)


def _infer_roles(
    artifact_type: ArtifactType,
    lines: list[str],
    default_human_role: str | None,
    default_agent_role: str | None,
) -> tuple[str | None, str | None]:
    human_role = default_human_role
    agent_role = default_agent_role
    for line in lines:
        lowered = line.lower()
        if lowered.startswith("human "):
            human_role = line
        elif lowered.startswith("agent "):
            agent_role = line

    if artifact_type is ArtifactType.SKILL:
        human_role = human_role or "Provides goals or approval"
        agent_role = agent_role or "Executes the documented workflow"
    elif artifact_type is ArtifactType.PROMPT:
        human_role = human_role or "Reviews or approves prompt outputs"
        agent_role = agent_role or "Executes the prompted workflow"

    return human_role, agent_role


def _derive_reusable_patterns(
    *,
    hard_constraints: list[str],
    approval_gates: list[str],
    review_loops: list[str],
    escalation_paths: list[str],
    human_role: str | None,
    agent_role: str | None,
) -> list[str]:
    patterns: list[str] = []
    if hard_constraints:
        patterns.append("guardrailed workflow")
    if approval_gates:
        patterns.append("human approval gate")
    if review_loops:
        patterns.append("iterative review loop")
    if escalation_paths:
        patterns.append("human escalation path")
    if human_role and agent_role:
        patterns.append("human-agent handoff")
    return patterns


def _extract_ci_steps(lines: list[str]) -> list[str]:
    steps: list[str] = []
    for line in lines:
        if line.startswith("- "):
            steps.append(line[2:].strip())
        elif line.startswith("run:"):
            steps.append(line.split(":", 1)[1].strip())
    return steps


def _extract_ci_decision_gates(lines: list[str]) -> list[str]:
    gates = ["CI workflow executes on configured GitHub event"]
    for line in lines:
        if line.startswith(("on:", "if:", "branches:", "paths:")):
            gates.append(line)
    return gates


def _extract_doc_triggers(lines: list[str]) -> list[str]:
    triggers: list[str] = []
    for line in lines:
        lowered = line.lower()
        if lowered.startswith(("use when", "when to use", "overview")):
            triggers.append(line)
    if not triggers:
        triggers.append("documented workflow")
    return triggers


def _extract_doc_steps(lines: list[str]) -> list[str]:
    steps: list[str] = []
    for line in lines:
        ordered_step = _extract_ordered_step(line)
        if ordered_step:
            steps.append(ordered_step)
        elif line.startswith("- "):
            steps.append(line[2:].strip())
    return steps[:12]


def _extract_analysis_lines(content: str) -> list[str]:
    lines: list[str] = []
    in_fenced_block = False
    for raw_line in content.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_fenced_block = not in_fenced_block
            continue
        if in_fenced_block or not stripped:
            continue
        lines.append(stripped)
    return lines


def _looks_like_hard_constraint(line: str) -> bool:
    lowered = line.lower()
    return any(
        phrase in lowered
        for phrase in (
            "must",
            "never",
            "required",
            "do not",
            "non-negotiable",
        )
    )


def _limit_unique(values: list[str], limit: int) -> list[str]:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
        if len(seen) == limit:
            break
    return seen
