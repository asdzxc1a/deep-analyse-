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
        lines = [line.strip() for line in content.splitlines() if line.strip()]

        trigger_conditions: list[str] = []
        steps: list[str] = []
        decision_gates: list[str] = []
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
            human_role = "Provides goals or approval"
            agent_role = "Executes the documented workflow"
        elif artifact.artifact_type is ArtifactType.CI:
            trigger_conditions.append("workflow file present")
            steps.extend(_extract_ci_steps(lines))
            decision_gates.extend(_extract_ci_decision_gates(lines))
        else:
            trigger_conditions.extend(_extract_doc_triggers(lines))
            steps.extend(_extract_doc_steps(lines))

        summary = _workflow_summary(artifact.path, artifact.artifact_type, steps)

        if trigger_conditions or steps:
            findings.append(
                WorkflowFinding(
                    path=artifact.path,
                    summary=summary,
                    trigger_conditions=trigger_conditions,
                    steps=steps,
                    decision_gates=decision_gates,
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
