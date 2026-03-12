from pathlib import PurePosixPath

from deep_analysis.models import Artifact, ArtifactType


EXCLUDED_NAMES = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock"}


def classify_artifact(path: str) -> Artifact:
    pure_path = PurePosixPath(path)
    normalized = str(pure_path)
    name = pure_path.name

    if name == "SKILL.md" or "skills/" in normalized:
        artifact_type = ArtifactType.SKILL
        is_meaningful = True
    elif pure_path.suffix in {".py", ".js", ".ts", ".tsx"}:
        artifact_type = ArtifactType.CODE
        is_meaningful = True
    elif pure_path.suffix in {".yml", ".yaml"} and ".github/workflows/" in normalized:
        artifact_type = ArtifactType.CI
        is_meaningful = True
    elif pure_path.suffix in {".md", ".txt"}:
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
