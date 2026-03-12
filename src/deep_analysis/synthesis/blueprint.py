from pathlib import Path

from deep_analysis.fs_utils import ensure_dir, write_text
from deep_analysis.synthesis.translation import render_capability_map
from deep_analysis.synthesis.translation import render_domain_translation_map
from deep_analysis.synthesis.translation import render_target_doctrine
from deep_analysis.synthesis.translation import render_target_role_system


def write_blueprint_repo(
    blueprint_dir: Path,
    repo_name: str,
    preservation_decisions: list,
    workflow_patterns: list,
    translation_plan=None,
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
    if translation_plan is not None:
        write_text(blueprint_dir / "docs" / "domain-translation-map.md", render_domain_translation_map(translation_plan))
        write_text(blueprint_dir / "docs" / "role-system.md", render_target_role_system(translation_plan))
        write_text(blueprint_dir / "docs" / "target-doctrine.md", render_target_doctrine(translation_plan))
        write_text(blueprint_dir / "docs" / "marketing-capability-map.md", render_capability_map(translation_plan))
    write_text(blueprint_dir / "starter-src" / "README.md", "# starter-src\n")
    write_text(blueprint_dir / "starter-tests" / "README.md", "# starter-tests\n")
    if translation_plan is not None and translation_plan.target_domain == "marketing":
        ensure_dir(blueprint_dir / "skills-or-prompts" / "skills" / "positioning")
        ensure_dir(blueprint_dir / "skills-or-prompts" / "skills" / "campaign-planning")
        ensure_dir(blueprint_dir / "skills-or-prompts" / "skills" / "copy-review")
        ensure_dir(blueprint_dir / "skills-or-prompts" / "skills" / "launch-verification")
        ensure_dir(blueprint_dir / "skills-or-prompts" / "prompts")
        write_text(blueprint_dir / "skills-or-prompts" / "prompts" / "strategist-prompt.md", "# Strategist Prompt\n")
        write_text(blueprint_dir / "skills-or-prompts" / "prompts" / "copywriter-prompt.md", "# Copywriter Prompt\n")
        write_text(blueprint_dir / "skills-or-prompts" / "prompts" / "analyst-prompt.md", "# Analyst Prompt\n")
        write_text(blueprint_dir / "skills-or-prompts" / "README.md", "# skills-or-prompts\n\nTarget-aware marketing scaffold.\n")
    else:
        write_text(blueprint_dir / "skills-or-prompts" / "README.md", "# skills-or-prompts\n")
    write_text(blueprint_dir / "migration-notes" / "README.md", "# migration-notes\n")
