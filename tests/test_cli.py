from pathlib import Path

from deep_analysis.git_utils import prepare_repo_workspace


def test_prepare_repo_workspace_uses_existing_local_repo(tmp_path: Path) -> None:
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()

    workspace = prepare_repo_workspace(str(repo_dir), tmp_path / "workspace")

    assert workspace.source_repo_path == repo_dir
    assert workspace.clone_performed is False
