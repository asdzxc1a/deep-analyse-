from pathlib import Path

from typer.testing import CliRunner

from deep_analysis.cli import app
from deep_analysis.analysis.domain_translation import parse_vision_file
from deep_analysis.git_utils import prepare_repo_workspace
from deep_analysis.synthesis.skill_pack import write_skill_pack


def test_cli_analyze_accepts_translation_mode_arguments(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "analyze",
            "tests/fixtures/sample_agent_repo",
            str(tmp_path / "out"),
            "--target-domain",
            "marketing",
            "--vision-file",
            "tests/fixtures/marketing_vision.md",
        ],
    )

    assert result.exit_code == 0


def test_cli_rejects_vision_file_without_target_domain(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "analyze",
            "tests/fixtures/sample_agent_repo",
            str(tmp_path / "out"),
            "--vision-file",
            "tests/fixtures/marketing_vision.md",
        ],
    )

    assert result.exit_code != 0
    assert "target-domain" in result.stdout.lower() or "target-domain" in result.stderr.lower()


def test_parse_vision_file_ignores_markdown_heading() -> None:
    profile = parse_vision_file(Path("tests/fixtures/marketing_vision.md"), "marketing")

    assert "# Marketing Vision" not in profile.target_audience
    assert "research before messaging" in profile.philosophies


def test_prepare_repo_workspace_uses_existing_local_repo(tmp_path: Path) -> None:
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()

    workspace = prepare_repo_workspace(str(repo_dir), tmp_path / "workspace")

    assert workspace.source_repo_path == repo_dir
    assert workspace.clone_performed is False


def test_write_skill_pack_creates_installable_layout(tmp_path: Path) -> None:
    output_dir = tmp_path / "skill-pack"
    write_skill_pack(output_dir)
    assert (output_dir / "analysis-system" / "SKILL.md").exists()
