from pathlib import Path

import typer

from deep_analysis.cartography import build_repo_map
from deep_analysis.git_utils import prepare_repo_workspace
from deep_analysis.synthesis.skill_pack import write_skill_pack


app = typer.Typer(name="deep-analysis", no_args_is_help=True)


@app.command()
def analyze(repo_url: str, output_dir: str, export_skill_pack: bool = False) -> None:
    """Analyze one repository and write dossier/blueprint outputs."""
    workspace = prepare_repo_workspace(repo_url, Path(output_dir))
    repo_map = build_repo_map(workspace.source_repo_path)
    meaningful_count = sum(1 for artifact in repo_map.artifacts if artifact.is_meaningful)
    typer.echo(f"Mapped {len(repo_map.artifacts)} artifacts ({meaningful_count} meaningful)")
    raise NotImplementedError("Pipeline not wired yet")


@app.command("export-skill-pack")
def export_skill_pack(source_dir: str, output_dir: str) -> None:
    """Export the reusable analysis skill pack from an existing analysis run."""
    del source_dir
    write_skill_pack(Path(output_dir))
    typer.echo(f"Skill pack written to {output_dir}")


if __name__ == "__main__":
    app()
