from pathlib import Path

import typer

from deep_analysis.pipeline import run_analysis_pipeline
from deep_analysis.synthesis.skill_pack import write_skill_pack


app = typer.Typer(name="deep-analysis", no_args_is_help=True)


@app.command()
def analyze(
    repo_url: str,
    output_dir: str,
    export_skill_pack: bool = False,
    target_domain: str | None = None,
    vision_file: Path | None = None,
) -> None:
    """Analyze one repository and write dossier/blueprint outputs."""
    if vision_file is not None and target_domain is None:
        raise typer.BadParameter("--vision-file requires --target-domain")
    result = run_analysis_pipeline(
        repo_url,
        Path(output_dir),
        export_skill_pack,
        target_domain=target_domain,
        vision_file=vision_file,
    )
    typer.echo(f"Analysis project written to {result.analysis_project_dir}")
    typer.echo(f"Blueprint written to {result.blueprint_dir}")
    typer.echo(f"Skill pack exported: {bool(result.skill_pack_dir)}")


@app.command("export-skill-pack")
def export_skill_pack(source_dir: str, output_dir: str) -> None:
    """Export the reusable analysis skill pack from an existing analysis run."""
    del source_dir
    write_skill_pack(Path(output_dir))
    typer.echo(f"Skill pack written to {output_dir}")


if __name__ == "__main__":
    app()
