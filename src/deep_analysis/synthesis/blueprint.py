from pathlib import Path

from deep_analysis.fs_utils import ensure_dir, write_text


def write_blueprint_repo(blueprint_dir: Path, repo_name: str, preservation_decisions: list) -> None:
    ensure_dir(blueprint_dir / "docs")
    ensure_dir(blueprint_dir / "docs" / "source-repo-dossier")
    ensure_dir(blueprint_dir / "docs" / "architecture")
    ensure_dir(blueprint_dir / "skills-or-prompts")
    ensure_dir(blueprint_dir / "starter-src")
    ensure_dir(blueprint_dir / "starter-tests")
    ensure_dir(blueprint_dir / "migration-notes")

    write_text(blueprint_dir / "README.md", f"# {repo_name} Clone Blueprint\n")
    write_text(blueprint_dir / "docs" / "preservation-matrix.md", "# Preservation Matrix\n")
    write_text(blueprint_dir / "docs" / "reconstruction-plan.md", "# Reconstruction Plan\n")
    write_text(blueprint_dir / "docs" / "differentiation-notes.md", "# Differentiation Notes\n")
    write_text(blueprint_dir / "starter-src" / "README.md", "# starter-src\n")
    write_text(blueprint_dir / "starter-tests" / "README.md", "# starter-tests\n")
