from pathlib import Path

from deep_analysis.fs_utils import ensure_dir, write_text


def write_skill_pack(output_dir: Path) -> None:
    skill_dir = ensure_dir(output_dir / "analysis-system")
    write_text(
        skill_dir / "SKILL.md",
        "---\nname: analysis-system\ndescription: Reusable repo analysis workflow\n---\n\n# Analysis System\n",
    )
