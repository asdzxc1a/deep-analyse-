from pathlib import PurePosixPath

from deep_analysis.models import Artifact, ArtifactType


EXCLUDED_NAMES = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock"}
CODE_SUFFIXES = {".py", ".js", ".ts", ".tsx"}
DOC_SUFFIXES = {".md", ".txt"}
SCRIPT_SUFFIXES = {".sh"}


def classify_artifact(path: str) -> Artifact:
    pure_path = PurePosixPath(path)
    normalized = str(pure_path)
    name = pure_path.name

    if name == "SKILL.md":
        artifact_type = ArtifactType.SKILL
        is_meaningful = True
    elif ".github/workflows/" in normalized and pure_path.suffix in {".yml", ".yaml"}:
        artifact_type = ArtifactType.CI
        is_meaningful = True
    elif pure_path.suffix in CODE_SUFFIXES:
        artifact_type = ArtifactType.CODE
        is_meaningful = True
    elif pure_path.suffix in SCRIPT_SUFFIXES:
        artifact_type = ArtifactType.SCRIPT
        is_meaningful = True
    elif "prompt" in name.lower() and pure_path.suffix in DOC_SUFFIXES:
        artifact_type = ArtifactType.PROMPT
        is_meaningful = True
    elif pure_path.suffix in DOC_SUFFIXES:
        artifact_type = ArtifactType.DOC
        is_meaningful = True
    else:
        artifact_type = ArtifactType.OTHER
        is_meaningful = False

    if name in EXCLUDED_NAMES or "node_modules/" in normalized:
        is_meaningful = False

    return Artifact(
        path=normalized,
        artifact_type=artifact_type,
        is_meaningful=is_meaningful,
    )
