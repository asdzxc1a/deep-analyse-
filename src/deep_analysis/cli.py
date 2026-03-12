import typer


app = typer.Typer(name="deep-analysis", no_args_is_help=True)


@app.command()
def analyze(repo_url: str, output_dir: str, export_skill_pack: bool = False) -> None:
    """Analyze one repository and write dossier/blueprint outputs."""
    raise NotImplementedError("Pipeline not wired yet")


@app.command("export-skill-pack")
def export_skill_pack(source_dir: str, output_dir: str) -> None:
    """Export the reusable analysis skill pack from an existing analysis run."""
    raise NotImplementedError("Skill-pack export not wired yet")


if __name__ == "__main__":
    app()
