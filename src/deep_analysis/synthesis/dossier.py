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
    _write_file_analysis(output_dir / "03-file-analysis", logic_findings)
    _write_workflow_analysis(output_dir / "04-workflows-prompts-skills", workflow_findings)
    write_text(output_dir / "05-architecture" / "README.md", _render_architecture(architecture))
    write_text(output_dir / "06-preservation-boundaries" / "README.md", _render_preservation(preservation))
    write_text(
        output_dir / "07-reconstruction-plan" / "README.md",
        _render_reconstruction_plan(repo_name, logic_findings, workflow_findings),
    )
    write_text(
        output_dir / "08-clone-blueprint" / "README.md",
        "# Clone Blueprint\n\nSee the sibling `clone-blueprint/` output for generated reconstruction assets.\n",
    )
    write_text(
        output_dir / "09-optional-skill-pack" / "README.md",
        "# Optional Skill Pack\n\nRun `deep-analysis export-skill-pack <analysis-run> <output-dir>` to export the reusable workflow.\n",
    )


def _write_file_analysis(output_dir: Path, logic_findings: list) -> None:
    index_lines = ["# File Analysis", ""]
    for finding in logic_findings:
        slug = safe_slug(finding.path) + ".md"
        index_lines.append(f"- [{finding.path}](./{slug})")
        write_text(output_dir / slug, _render_artifact_finding(finding))
    write_text(output_dir / "README.md", "\n".join(index_lines) + "\n")


def _write_workflow_analysis(output_dir: Path, workflow_findings: list) -> None:
    index_lines = ["# Workflows, Prompts, and Skills", ""]
    for finding in workflow_findings:
        slug = safe_slug(finding.path) + ".md"
        index_lines.append(f"- [{finding.path}](./{slug})")
        write_text(output_dir / slug, _render_workflow_finding(finding))
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


def _render_artifact_finding(finding) -> str:
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
    lines.extend(["", "## Reconstruction Notes", "", finding.reconstruction_notes, ""])
    return "\n".join(lines)


def _render_workflow_finding(finding) -> str:
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
    if finding.human_role or finding.agent_role:
        lines.extend(["", "## Roles", ""])
        if finding.human_role:
            lines.append(f"- Human: {finding.human_role}")
        if finding.agent_role:
            lines.append(f"- Agent: {finding.agent_role}")
    lines.append("")
    return "\n".join(lines)


def _render_architecture(architecture: ArchitectureSummary) -> str:
    lines = ["# Architecture", "", architecture.narrative, "", "## Components", ""]
    lines.extend(f"- {summary}" for summary in architecture.component_summaries)
    lines.extend(["", "## Entry Points", ""])
    lines.extend(f"- {entrypoint}" for entrypoint in architecture.entrypoints or ["None"])
    return "\n".join(lines) + "\n"


def _render_preservation(preservation: PreservationReport) -> str:
    lines = ["# Preservation Boundaries", "", "| Path | Decision | Rationale |", "| --- | --- | --- |"]
    for decision in preservation.decisions:
        lines.append(f"| {decision.path} | {decision.decision} | {decision.rationale} |")
    return "\n".join(lines) + "\n"


def _render_reconstruction_plan(repo_name: str, logic_findings: list, workflow_findings: list) -> str:
    return (
        f"# Reconstruction Plan\n\n"
        f"Target repo: {repo_name}\n\n"
        f"1. Recreate the {len(workflow_findings)} workflow-bearing artifacts in your own language.\n"
        f"2. Rebuild the {len(logic_findings)} meaningful artifacts while preserving their system roles.\n"
        "3. Apply the preservation matrix before carrying source material into the blueprint repo.\n"
    )
