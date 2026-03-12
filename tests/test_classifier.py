from deep_analysis.config import AnalysisConfig
from deep_analysis.classifier import classify_artifact
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


def test_skill_markdown_classifies_as_skill() -> None:
    artifact = classify_artifact("skills/brainstorming/SKILL.md")
    assert artifact.artifact_type is ArtifactType.SKILL
    assert artifact.is_meaningful is True


def test_support_files_inside_skills_keep_their_real_type() -> None:
    code_artifact = classify_artifact("skills/brainstorming/scripts/index.js")
    doc_artifact = classify_artifact("skills/brainstorming/visual-companion.md")
    assert code_artifact.artifact_type is ArtifactType.CODE
    assert doc_artifact.artifact_type is ArtifactType.DOC


def test_test_files_classify_as_meaningful_test_artifacts() -> None:
    artifact = classify_artifact("tests/test_example.py")
    assert artifact.artifact_type is ArtifactType.TEST
    assert artifact.is_meaningful is True


def test_lockfile_is_not_meaningful_by_default() -> None:
    artifact = classify_artifact("package-lock.json")
    assert artifact.is_meaningful is False
