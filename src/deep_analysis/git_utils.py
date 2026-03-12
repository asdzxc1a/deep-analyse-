from dataclasses import dataclass
from pathlib import Path

from git import Repo

from deep_analysis.fs_utils import ensure_dir


@dataclass(slots=True)
class RepoWorkspace:
    source_repo_path: Path
    workspace_root: Path
    clone_performed: bool


def prepare_repo_workspace(repo_url_or_path: str, workspace_root: Path) -> RepoWorkspace:
    source_path = Path(repo_url_or_path).expanduser()
    workspace_root = ensure_dir(workspace_root)

    if source_path.exists():
        return RepoWorkspace(
            source_repo_path=source_path,
            workspace_root=workspace_root,
            clone_performed=False,
        )

    clone_path = workspace_root / "source-repo"
    Repo.clone_from(repo_url_or_path, clone_path)
    return RepoWorkspace(
        source_repo_path=clone_path,
        workspace_root=workspace_root,
        clone_performed=True,
    )
