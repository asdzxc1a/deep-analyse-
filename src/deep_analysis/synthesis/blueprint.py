from pathlib import Path

from deep_analysis.fs_utils import ensure_dir, write_text


def write_blueprint_repo(
    blueprint_dir: Path,
    repo_name: str,
    preservation_decisions: list,
    workflow_patterns: list,
) -> None:
    ensure_dir(blueprint_dir / "docs")
    ensure_dir(blueprint_dir / "docs" / "source-repo-dossier")
    ensure_dir(blueprint_dir / "docs" / "architecture")
    ensure_dir(blueprint_dir / "skills-or-prompts")
    ensure_dir(blueprint_dir / "starter-src")
    ensure_dir(blueprint_dir / "starter-tests")
    ensure_dir(blueprint_dir / "migration-notes")

    write_text(blueprint_dir / "README.md", f"# {repo_name} Clone Blueprint\n")
    matrix_lines = [
        "# Preservation Matrix",
        "",
        "| Path | Role | Decision | Legal Review | Confidence | Strategy Note | Rationale |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for decision in preservation_decisions:
        matrix_lines.append(
            "| "
            + " | ".join(
                [
                    decision.path,
                    decision.artifact_role,
                    decision.decision,
                    decision.legal_review,
                    decision.confidence,
                    decision.strategy_note,
                    decision.rationale,
                ]
            )
            + " |"
        )
    write_text(blueprint_dir / "docs" / "preservation-matrix.md", "\n".join(matrix_lines) + "\n")
    write_text(
        blueprint_dir / "docs" / "reconstruction-plan.md",
        (
            "# Reconstruction Plan\n\n"
            "1. Start with preserved structure and interfaces.\n"
            "2. Rewrite workflow-language artifacts into your own voice.\n"
            "3. Preserve the repo workflow patterns captured in `docs/workflow-patterns.md` while rebuilding operator behavior.\n"
            "4. Preserve verification contracts from tests, but allow the rebuilt harness, assertions framework, and test layout to change.\n"
            "5. Adapt fixtures and sample verification data to the rebuilt system instead of carrying them over blindly.\n"
            "6. Build implementation slices guided by the preservation matrix.\n"
        ),
    )
    pattern_lines = ["# Workflow Patterns", ""]
    for pattern in workflow_patterns:
        pattern_lines.extend([f"## {pattern.name}", "", pattern.summary, "", "### Evidence Artifacts", ""])
        pattern_lines.extend(f"- {artifact}" for artifact in pattern.evidence_artifacts)
        pattern_lines.extend(["", "### Reconstruction Note", "", pattern.reconstruction_note, ""])
    if not workflow_patterns:
        pattern_lines.append("No repeated repo-level workflow patterns were synthesized.")
    write_text(blueprint_dir / "docs" / "workflow-patterns.md", "\n".join(pattern_lines) + "\n")
    write_text(
        blueprint_dir / "docs" / "differentiation-notes.md",
        "# Differentiation Notes\n\nDocument where your version should intentionally diverge in positioning, language, or workflow design.\n",
    )
    write_text(blueprint_dir / "starter-src" / "README.md", "# starter-src\n")
    write_text(blueprint_dir / "starter-tests" / "README.md", "# starter-tests\n")
    write_text(blueprint_dir / "skills-or-prompts" / "README.md", "# skills-or-prompts\n")
    write_text(blueprint_dir / "migration-notes" / "README.md", "# migration-notes\n")
