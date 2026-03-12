from pathlib import Path

from deep_analysis.fs_utils import ensure_dir, write_text


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


def write_dossier(output_dir: Path, repo_name: str, repo_map, findings: list) -> None:
    ensure_dir(output_dir)

    for directory in DOSSIER_DIRS:
        ensure_dir(output_dir / directory)

    write_text(output_dir / "01-source-profile" / "README.md", f"# Source Profile\n\nRepo: {repo_name}\n")
    write_text(output_dir / "02-repo-map" / "README.md", "# Repo Map\n")
    write_text(output_dir / "03-file-analysis" / "README.md", f"# File Analysis\n\nFindings: {len(findings)}\n")
