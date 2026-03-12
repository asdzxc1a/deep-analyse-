from deep_analysis.config import AnalysisConfig
from deep_analysis.models import Artifact, ArtifactType


def test_default_focus_is_agent_workflow_repos() -> None:
    config = AnalysisConfig()
    assert config.primary_repo_focus == "agent-workflow"


def test_artifact_requires_path_and_type() -> None:
    artifact = Artifact(
        path="skills/brainstorming/SKILL.md",
        artifact_type=ArtifactType.SKILL,
        is_meaningful=True,
    )
    assert artifact.path.endswith("SKILL.md")
