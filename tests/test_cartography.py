from pathlib import Path

from deep_analysis.cartography import build_repo_map


def test_build_repo_map_collects_meaningful_artifacts() -> None:
    repo_root = Path("tests/fixtures/sample_agent_repo")
    repo_map = build_repo_map(repo_root)
    paths = {artifact.path for artifact in repo_map.artifacts if artifact.is_meaningful}
    assert "skills/example/SKILL.md" in paths
    assert ".github/workflows/test.yml" in paths
