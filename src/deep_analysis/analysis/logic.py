from pathlib import Path

from deep_analysis.cartography import RepoMap
from deep_analysis.models import ArtifactFinding


def analyze_logic(repo_root: Path, repo_map: RepoMap) -> list[ArtifactFinding]:
    findings: list[ArtifactFinding] = []

    for artifact in repo_map.artifacts:
        if not artifact.is_meaningful:
            continue

        file_path = repo_root / artifact.path
        content = file_path.read_text(encoding="utf-8")
        first_nonempty = next((line.strip() for line in content.splitlines() if line.strip()), "")
        summary = f"{artifact.artifact_type.value} artifact at {artifact.path}: {first_nonempty}"
        reconstruction_notes = f"Preserve the role of {artifact.path} and rebuild it with equivalent behavior."

        findings.append(
            ArtifactFinding(
                path=artifact.path,
                summary=summary,
                reconstruction_notes=reconstruction_notes,
            )
        )

    return findings
