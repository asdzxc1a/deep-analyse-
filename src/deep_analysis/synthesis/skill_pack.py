from pathlib import Path

from deep_analysis.fs_utils import ensure_dir, write_text


def write_skill_pack(output_dir: Path) -> None:
    skill_dir = ensure_dir(output_dir / "analysis-system")
    write_text(
        skill_dir / "SKILL.md",
        (
            "---\n"
            "name: analysis-system\n"
            "description: Reusable repo analysis workflow\n"
            "---\n\n"
            "# Analysis System\n\n"
            "Analyze one repository at a time and produce three outputs:\n"
            "- an analysis-project dossier\n"
            "- a clone blueprint\n"
            "- an optional reusable skill pack\n\n"
            "## Workflow\n\n"
            "1. Clone or open the source repository in an isolated workspace.\n"
            "2. Build a repo map covering meaningful files, entry points, and subsystems.\n"
            "3. Generate file-level analysis pages for every meaningful artifact.\n"
            "4. Extract workflows, triggers, steps, and decision gates from skill, doc, and CI artifacts.\n"
            "5. Write a preservation matrix before creating the clone blueprint.\n"
            "6. Rebuild the source system in your own structure while respecting preservation decisions.\n\n"
            "## Output Contract\n\n"
            "- `analysis-project/` must contain source profile, repo map, file analysis, workflows, architecture, preservation boundaries, and reconstruction plan.\n"
            "- `clone-blueprint/` must contain preservation matrix, reconstruction plan, starter source folders, and differentiation notes.\n"
            "- Human-facing language should be rewritten into the operator's own voice unless preservation review explicitly allows otherwise.\n"
        ),
    )
