from pathlib import Path

from deep_analysis.fs_utils import ensure_dir, safe_slug, write_text
from deep_analysis.models import ArchitectureSummary, PreservationReport


DOSSIER_DIRS = [
    "01-source-profile",
    "02-repo-map",
    "03-file-analysis",
    "04-workflows-prompts-skills",
    "05-architecture",
    "06-preservation-boundaries",
    "07-reconstruction-plan",
    "08-clone-blueprint",
    "09-optional-skill-pack",
]


def write_dossier(
    output_dir: Path,
    repo_name: str,
    repo_map,
    logic_findings: list,
    workflow_findings: list,
    architecture: ArchitectureSummary,
    preservation: PreservationReport,
) -> None:
    ensure_dir(output_dir)

    for directory in DOSSIER_DIRS:
        ensure_dir(output_dir / directory)

    meaningful_artifacts = [artifact for artifact in repo_map.artifacts if artifact.is_meaningful]

    write_text(
        output_dir / "01-source-profile" / "README.md",
        (
            f"# Source Profile\n\n"
            f"Repo: {repo_name}\n\n"
            f"- Total artifacts: {len(repo_map.artifacts)}\n"
            f"- Meaningful artifacts: {len(meaningful_artifacts)}\n"
            f"- Entrypoints: {len(repo_map.entrypoints)}\n"
        ),
    )
    write_text(
        output_dir / "02-repo-map" / "README.md",
        _render_repo_map(repo_map, meaningful_artifacts),
    )
    _write_file_analysis(
        output_dir / "03-file-analysis",
        repo_map,
        logic_findings,
        preservation,
        architecture,
        workflow_findings,
    )
    _write_workflow_analysis(output_dir / "04-workflows-prompts-skills", workflow_findings, preservation)
    write_text(output_dir / "05-architecture" / "README.md", _render_architecture(architecture))
    write_text(output_dir / "06-preservation-boundaries" / "README.md", _render_preservation(preservation))
    write_text(
        output_dir / "07-reconstruction-plan" / "README.md",
        _render_reconstruction_plan(repo_name, logic_findings, workflow_findings, architecture),
    )
    write_text(
        output_dir / "08-clone-blueprint" / "README.md",
        "# Clone Blueprint\n\nSee the sibling `clone-blueprint/` output for generated reconstruction assets.\n",
    )
    write_text(
        output_dir / "09-optional-skill-pack" / "README.md",
        "# Optional Skill Pack\n\nRun `deep-analysis export-skill-pack <analysis-run> <output-dir>` to export the reusable workflow.\n",
    )


def _write_file_analysis(
    output_dir: Path,
    repo_map,
    logic_findings: list,
    preservation: PreservationReport,
    architecture: ArchitectureSummary,
    workflow_findings: list,
) -> None:
    index_lines = ["# File Analysis", ""]
    preservation_by_path = {decision.path: decision for decision in preservation.decisions}
    workflows_by_path = {finding.path: finding for finding in workflow_findings}
    for finding in logic_findings:
        slug = safe_slug(finding.path) + ".md"
        index_lines.append(f"- [{finding.path}](./{slug})")
        write_text(
            output_dir / slug,
            _render_artifact_finding(
                finding,
                repo_map,
                preservation_by_path.get(finding.path),
                architecture,
                workflows_by_path.get(finding.path),
            ),
        )
    write_text(output_dir / "README.md", "\n".join(index_lines) + "\n")


def _write_workflow_analysis(output_dir: Path, workflow_findings: list, preservation: PreservationReport) -> None:
    index_lines = ["# Workflows, Prompts, and Skills", ""]
    preservation_by_path = {decision.path: decision for decision in preservation.decisions}
    for finding in workflow_findings:
        slug = safe_slug(finding.path) + ".md"
        index_lines.append(f"- [{finding.path}](./{slug})")
        write_text(output_dir / slug, _render_workflow_finding(finding, preservation_by_path.get(finding.path)))
    write_text(output_dir / "README.md", "\n".join(index_lines) + "\n")


def _render_repo_map(repo_map, meaningful_artifacts: list) -> str:
    lines = ["# Repo Map", "", "## Entry Points", ""]
    for entrypoint in repo_map.entrypoints:
        lines.append(f"- {entrypoint}")
    lines.extend(["", "## Subsystems", ""])
    for subsystem, paths in sorted(repo_map.subsystems.items()):
        lines.append(f"- {subsystem}: {len(paths)} artifact(s)")
    lines.extend(["", "## Meaningful Artifacts", ""])
    for artifact in meaningful_artifacts:
        lines.append(f"- {artifact.path} ({artifact.artifact_type.value})")
    return "\n".join(lines) + "\n"


def _render_artifact_finding(finding, repo_map, preservation_decision, architecture: ArchitectureSummary, workflow_finding) -> str:
    system_role = _describe_system_role(finding, preservation_decision, architecture)
    preserve_lines = _build_preserve_lines(finding, preservation_decision, architecture, workflow_finding)
    change_lines = _build_change_lines(finding, preservation_decision)
    rebuild_strategy = _build_rebuild_strategy(finding, preservation_decision, workflow_finding)
    first_slice = _build_first_slice(finding, preservation_decision, architecture, workflow_finding)
    connections = _build_connected_artifacts(finding.path, repo_map)
    lines = [
        f"# {finding.path}",
        "",
        f"Artifact Type: {finding.artifact_type.value}",
        f"Line Count: {finding.line_count}",
        "",
        "## Summary",
        "",
        finding.summary,
        "",
        "## Key Signals",
        "",
    ]
    lines.extend(f"- {signal}" for signal in finding.key_signals or ["None captured"])
    lines.extend(["", "## Dependencies", ""])
    lines.extend(f"- {dep}" for dep in finding.dependencies or ["None detected"])
    lines.extend(["", "## Failure Modes", ""])
    lines.extend(f"- {mode}" for mode in finding.failure_modes)
    lines.extend(["", "## System Role", "", system_role, ""])
    lines.extend(["## Preserve In Rebuild", ""])
    lines.extend(f"- {item}" for item in preserve_lines)
    lines.extend(["", "## Safe To Change", ""])
    lines.extend(f"- {item}" for item in change_lines)
    lines.extend(["", "## Rebuild Strategy", "", rebuild_strategy, ""])
    lines.extend(["## Suggested First Slice", "", first_slice, ""])
    lines.extend(["", "## Connected Artifacts", ""])
    lines.extend(["### Driven By", ""])
    lines.extend(f"- {item}" for item in connections["driven_by"])
    lines.extend(["", "### Drives", ""])
    lines.extend(f"- {item}" for item in connections["drives"])
    lines.extend(["", "### Validated By", ""])
    lines.extend(f"- {item}" for item in connections["validated_by"])
    lines.extend(["", "## Reconstruction Notes", "", finding.reconstruction_notes, ""])
    return "\n".join(lines)


def _render_workflow_finding(finding, preservation_decision) -> str:
    lines = [
        f"# {finding.path}",
        "",
        "## Summary",
        "",
        finding.summary,
        "",
        "## Trigger Conditions",
        "",
    ]
    lines.extend(f"- {condition}" for condition in finding.trigger_conditions)
    lines.extend(["", "## Ordered Steps", ""])
    lines.extend(f"- {step}" for step in finding.steps or ["No ordered steps extracted"])
    if finding.decision_gates:
        lines.extend(["", "## Decision Gates", ""])
        lines.extend(f"- {gate}" for gate in finding.decision_gates)
    lines.extend(["", "## Hard Constraints", ""])
    lines.extend(f"- {item}" for item in finding.hard_constraints or ["None"])
    lines.extend(["", "## Approval Gates", ""])
    lines.extend(f"- {item}" for item in finding.approval_gates or ["None"])
    lines.extend(["", "## Review Loops", ""])
    lines.extend(f"- {item}" for item in finding.review_loops or ["None"])
    lines.extend(["", "## Escalation Paths", ""])
    lines.extend(f"- {item}" for item in finding.escalation_paths or ["None"])
    lines.extend(["", "## Reusable Patterns", ""])
    lines.extend(f"- {item}" for item in finding.reusable_patterns or ["None"])
    if finding.human_role or finding.agent_role:
        lines.extend(["", "## Roles", ""])
        if finding.human_role:
            lines.append(f"- Human: {finding.human_role}")
        if finding.agent_role:
            lines.append(f"- Agent: {finding.agent_role}")
    lines.extend(["", "## Rebuild Guidance", ""])
    lines.extend(f"- {item}" for item in _build_workflow_guidance(finding, preservation_decision))
    lines.append("")
    return "\n".join(lines)


def _render_architecture(architecture: ArchitectureSummary) -> str:
    lines = ["# Architecture", "", architecture.narrative, "", "## Components", ""]
    lines.extend(f"- {summary}" for summary in architecture.component_summaries)
    lines.extend(["", "## Entry Points", ""])
    lines.extend(f"- {entrypoint}" for entrypoint in architecture.entrypoints or ["None"])
    lines.extend(["", "## Relationships", ""])
    lines.extend(f"- {summary}" for summary in architecture.relationship_summaries or ["None"])
    lines.extend(["", "## Critical Paths", ""])
    lines.extend(f"- {path}" for path in architecture.critical_paths or ["None"])
    return "\n".join(lines) + "\n"


def _render_preservation(preservation: PreservationReport) -> str:
    lines = ["# Preservation Boundaries", "", "| Path | Decision | Rationale |", "| --- | --- | --- |"]
    for decision in preservation.decisions:
        lines.append(f"| {decision.path} | {decision.decision} | {decision.rationale} |")
    return "\n".join(lines) + "\n"


def _render_reconstruction_plan(
    repo_name: str,
    logic_findings: list,
    workflow_findings: list,
    architecture: ArchitectureSummary,
) -> str:
    entrypoint_list = ", ".join(architecture.entrypoints[:3]) if architecture.entrypoints else "documented operator entrypoints"
    critical_path = architecture.critical_paths[0] if architecture.critical_paths else "Use the architecture page to recover the highest-leverage execution path."
    return (
        f"# Reconstruction Plan\n\n"
        f"Target repo: {repo_name}\n\n"
        "1. Start with executable or operator-facing entrypoints so the rebuilt system has a usable spine early.\n"
        f"   Prioritize: {entrypoint_list}.\n"
        "2. Recreate the workflow layer next so approvals, review loops, and operator expectations exist before broad implementation.\n"
        f"   This repo currently has {len(workflow_findings)} workflow-bearing artifact(s).\n"
        "3. Use the architecture page to rebuild dependencies in a system-aware order instead of file-by-file drift.\n"
        f"   First critical path: {critical_path}\n"
        "4. Apply the preservation matrix before carrying language, prompts, or implementation details into the blueprint repo.\n"
        f"   This repo currently has {len(logic_findings)} meaningful artifact(s) to rebuild against those boundaries.\n"
    )


def _describe_system_role(finding, preservation_decision, architecture: ArchitectureSummary) -> str:
    role = preservation_decision.artifact_role if preservation_decision else "meaningful system artifact"
    if finding.path in architecture.entrypoints:
        return f"This file is a {role} and acts as a repo entrypoint or first-touch surface for system behavior."
    return f"This file is a {role} that contributes to the repo's observable behavior or operator workflow."


def _build_preserve_lines(finding, preservation_decision, architecture: ArchitectureSummary, workflow_finding) -> list[str]:
    lines = [
        "Preserve the artifact's role in the system even if the implementation or wording changes.",
    ]
    if preservation_decision:
        lines.append(preservation_decision.strategy_note)
    if finding.dependencies:
        lines.append(f"Keep the key dependencies or interfaces aligned with: {', '.join(finding.dependencies[:3])}.")
    if finding.path in architecture.entrypoints:
        lines.append("Maintain an entrypoint with the same operational purpose so users or automation can trigger the rebuilt system.")
    if workflow_finding and (workflow_finding.approval_gates or workflow_finding.review_loops):
        lines.append("Preserve the human approval and review-loop behavior attached to this artifact.")
    return lines


def _build_change_lines(finding, preservation_decision) -> list[str]:
    if not preservation_decision:
        return ["Implementation details may change as long as the artifact keeps the same system role."]
    if preservation_decision.decision == "rewrite-with-differentiation":
        return ["Rewrite the framing, positioning, and wording so the rebuilt system has its own voice."]
    if preservation_decision.decision == "rewrite-equivalent":
        return ["Change the wording, examples, and organization while preserving the workflow semantics."]
    if preservation_decision.decision == "preserve-with-review":
        return ["Adapt environment assumptions, local paths, and execution details to match the new operating context."]
    return ["Change internal implementation details while preserving interfaces, side effects, and observable behavior."]


def _build_rebuild_strategy(finding, preservation_decision, workflow_finding) -> str:
    strategy_parts = [finding.reconstruction_notes]
    if preservation_decision:
        strategy_parts.append(preservation_decision.strategy_note)
    if workflow_finding and workflow_finding.steps:
        strategy_parts.append(
            "Rebuild the surrounding workflow with the same step order before broadening the implementation surface."
        )
    return " ".join(strategy_parts)


def _build_first_slice(finding, preservation_decision, architecture: ArchitectureSummary, workflow_finding) -> str:
    if finding.path in architecture.entrypoints:
        return "Create a minimal but runnable version of this entrypoint that reaches the same observable start condition."
    if workflow_finding:
        return "Recreate the smallest version of this workflow with one trigger, one approval gate, and one successful completion path."
    if preservation_decision and preservation_decision.artifact_role == "behavior-bearing implementation":
        return "Implement the smallest behavior slice that preserves the file's public interface and one core execution path."
    return "Rebuild the smallest version of this artifact that preserves its system role and one concrete output."


def _build_workflow_guidance(finding, preservation_decision) -> list[str]:
    guidance = [
        "Recreate the trigger condition and first successful path before expanding edge cases.",
    ]
    if finding.hard_constraints:
        guidance.append("Carry the non-negotiable constraints forward so the rebuilt workflow keeps its safety boundaries.")
    if finding.approval_gates:
        guidance.append("Preserve the approval gate structure so human checkpoints remain explicit.")
    if finding.review_loops:
        guidance.append("Implement at least one review loop in the rebuilt version before automating more branches.")
    if finding.escalation_paths:
        guidance.append("Keep a visible escalation path for blocked or ambiguous cases.")
    if preservation_decision:
        guidance.append(preservation_decision.strategy_note)
    return guidance


def _build_connected_artifacts(path: str, repo_map) -> dict[str, list[str]]:
    incoming = sorted(repo_map.graph.predecessors(path))
    outgoing = sorted(repo_map.graph.successors(path))
    validated_by = [
        source
        for source in incoming
        if repo_map.graph.nodes[source].get("artifact_type") == "test"
    ]
    driven_by = [source for source in incoming if source not in validated_by]
    return {
        "driven_by": driven_by or ["No explicit incoming links detected"],
        "drives": outgoing or ["No explicit outgoing links detected"],
        "validated_by": validated_by or ["No explicit validating artifacts detected"],
    }
