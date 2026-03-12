from dataclasses import dataclass
from pathlib import Path

import networkx as nx

from deep_analysis.classifier import classify_artifact
from deep_analysis.models import Artifact


@dataclass(slots=True)
class RepoMap:
    artifacts: list[Artifact]
    subsystems: dict[str, list[str]]
    entrypoints: list[str]
    graph: nx.DiGraph


def build_repo_map(repo_root: Path) -> RepoMap:
    artifacts: list[Artifact] = []
    subsystems: dict[str, list[str]] = {}
    entrypoints: list[str] = []
    graph = nx.DiGraph()

    for file_path in sorted(path for path in repo_root.rglob("*") if path.is_file()):
        relative_path = file_path.relative_to(repo_root).as_posix()
        artifact = classify_artifact(relative_path)
        artifacts.append(artifact)
        graph.add_node(relative_path, artifact_type=artifact.artifact_type.value)

        top_level = relative_path.split("/", 1)[0]
        subsystems.setdefault(top_level, []).append(relative_path)

        if artifact.is_meaningful and (
            relative_path.endswith("README.md")
            or relative_path.endswith("SKILL.md")
            or ".github/workflows/" in relative_path
        ):
            entrypoints.append(relative_path)

    return RepoMap(
        artifacts=artifacts,
        subsystems=subsystems,
        entrypoints=entrypoints,
        graph=graph,
    )
