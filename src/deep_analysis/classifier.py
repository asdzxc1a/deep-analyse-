from pathlib import PurePosixPath

from deep_analysis.models import Artifact, ArtifactType


EXCLUDED_NAMES = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock"}
CODE_SUFFIXES = {".py", ".js", ".ts", ".tsx"}
DOC_SUFFIXES = {".md", ".txt"}
SCRIPT_SUFFIXES = {".sh"}
TEST_SUFFIXES = {".py", ".js", ".ts", ".tsx"}


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
    elif _is_test_artifact(pure_path):
        artifact_type = ArtifactType.TEST
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

    if name in EXCLUDED_NAMES or "node_modules/" in normalized or "__pycache__/" in normalized:
        is_meaningful = False

    return Artifact(
        path=normalized,
        artifact_type=artifact_type,
        is_meaningful=is_meaningful,
    )


def _is_test_artifact(pure_path: PurePosixPath) -> bool:
    normalized = str(pure_path)
    name = pure_path.name.lower()
    if pure_path.suffix not in TEST_SUFFIXES:
        return False
    return (
        ("tests/" in normalized)
        or name.startswith("test_")
        or name.endswith((".test.js", ".spec.js", ".test.ts", ".spec.ts", ".test.py", ".spec.py"))
    )
