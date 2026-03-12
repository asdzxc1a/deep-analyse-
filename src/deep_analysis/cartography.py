from dataclasses import dataclass
from pathlib import Path
import re

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
    existing_paths: set[str] = set()

    for file_path in sorted(path for path in repo_root.rglob("*") if path.is_file()):
        relative_path = file_path.relative_to(repo_root).as_posix()
        existing_paths.add(relative_path)
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

    for artifact in artifacts:
        if not artifact.is_meaningful:
            continue
        _add_relationship_edges(repo_root, artifact.path, existing_paths, graph)

    return RepoMap(
        artifacts=artifacts,
        subsystems=subsystems,
        entrypoints=entrypoints,
        graph=graph,
    )


def _add_relationship_edges(repo_root: Path, source_path: str, existing_paths: set[str], graph: nx.DiGraph) -> None:
    content = (repo_root / source_path).read_text(encoding="utf-8")
    references = set()
    references.update(_extract_javascript_local_refs(source_path, content, existing_paths))
    references.update(_extract_script_local_refs(source_path, content, existing_paths))
    references.update(_extract_ci_local_refs(source_path, content, existing_paths))

    for target in sorted(references):
        if target != source_path:
            graph.add_edge(source_path, target)


def _extract_javascript_local_refs(source_path: str, content: str, existing_paths: set[str]) -> set[str]:
    references: set[str] = set()
    if not source_path.endswith((".js", ".ts", ".tsx")):
        return references

    patterns = [
        r"""require\(["'](\.[^"']+)["']\)""",
        r"""from\s+["'](\.[^"']+)["']""",
        r"""import\(["'](\.[^"']+)["']\)""",
    ]
    for pattern in patterns:
        for match in re.findall(pattern, content):
            resolved = _resolve_relative_reference(source_path, match, existing_paths)
            if resolved:
                references.add(resolved)
    return references


def _extract_script_local_refs(source_path: str, content: str, existing_paths: set[str]) -> set[str]:
    references: set[str] = set()
    if not source_path.endswith(".sh"):
        return references

    command_patterns = [
        r"""(?:^|\s)node\s+([A-Za-z0-9_./-]+\.(?:js|ts|tsx))""",
        r"""(?:^|\s)(?:bash|sh|python|python3)\s+([A-Za-z0-9_./-]+\.(?:sh|py|js|ts|tsx))""",
        r"""(?:^|\s)\./([A-Za-z0-9_./-]+\.(?:sh|py|js|ts|tsx))""",
    ]
    for pattern in command_patterns:
        for match in re.findall(pattern, content, flags=re.MULTILINE):
            resolved = _resolve_workspace_path(source_path, match, existing_paths)
            if resolved:
                references.add(resolved)
    return references


def _extract_ci_local_refs(source_path: str, content: str, existing_paths: set[str]) -> set[str]:
    references: set[str] = set()
    if ".github/workflows/" not in source_path:
        return references

    for match in re.findall(r"""run:\s+(.+)""", content):
        for pattern in (
            r"""(?:^|\s)(?:bash|sh|python|python3|node)\s+([A-Za-z0-9_./-]+\.(?:sh|py|js|ts|tsx))""",
            r"""(?:^|\s)\./([A-Za-z0-9_./-]+\.(?:sh|py|js|ts|tsx))""",
        ):
            for path_match in re.findall(pattern, match):
                resolved = _resolve_workspace_path(source_path, path_match, existing_paths)
                if resolved:
                    references.add(resolved)
    return references


def _resolve_relative_reference(source_path: str, reference: str, existing_paths: set[str]) -> str | None:
    source_parent = Path(source_path).parent
    candidate_base = (source_parent / reference).as_posix()
    return _choose_existing_path(candidate_base, existing_paths)


def _resolve_workspace_path(source_path: str, reference: str, existing_paths: set[str]) -> str | None:
    reference = reference.lstrip("./")
    if reference in existing_paths:
        return reference

    source_parent = Path(source_path).parent
    candidate_base = (source_parent / reference).as_posix()
    return _choose_existing_path(candidate_base, existing_paths)


def _choose_existing_path(candidate_base: str, existing_paths: set[str]) -> str | None:
    candidates = [
        candidate_base,
        f"{candidate_base}.js",
        f"{candidate_base}.ts",
        f"{candidate_base}.tsx",
        f"{candidate_base}.py",
        f"{candidate_base}.sh",
        f"{candidate_base}/index.js",
        f"{candidate_base}/index.ts",
    ]
    for candidate in candidates:
        normalized = candidate.replace("\\", "/")
        if normalized in existing_paths:
            return normalized
    return None
