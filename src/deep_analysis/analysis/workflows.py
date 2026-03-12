from pathlib import Path

from deep_analysis.cartography import RepoMap
from deep_analysis.models import ArtifactType, WorkflowFinding


def analyze_workflows(repo_root: Path, repo_map: RepoMap) -> list[WorkflowFinding]:
    findings: list[WorkflowFinding] = []

    for artifact in repo_map.artifacts:
        if not artifact.is_meaningful:
            continue
        if artifact.artifact_type not in {ArtifactType.SKILL, ArtifactType.CI, ArtifactType.DOC}:
            continue

        file_path = repo_root / artifact.path
        content = file_path.read_text(encoding="utf-8")
        lines = [line.strip() for line in content.splitlines() if line.strip()]

        trigger_conditions: list[str] = []
        steps: list[str] = []

        if artifact.artifact_type is ArtifactType.SKILL:
            for line in lines:
                if line.startswith("description:"):
                    trigger_conditions.append(line.split(":", 1)[1].strip())
                elif line[:2].isdigit() and line[2] == ".":
                    steps.append(line.split(".", 1)[1].strip())
        elif artifact.artifact_type is ArtifactType.CI:
            trigger_conditions.append("workflow file present")
            steps.extend(line for line in lines if line.startswith("- "))
        else:
            trigger_conditions.append("documented workflow")

        if trigger_conditions or steps:
            findings.append(
                WorkflowFinding(
                    path=artifact.path,
                    trigger_conditions=trigger_conditions,
                    steps=steps,
                )
            )

    return findings
