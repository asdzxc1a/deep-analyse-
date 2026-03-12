import networkx as nx

from deep_analysis.cartography import RepoMap
from deep_analysis.models import ArchitectureSummary


def analyze_architecture(repo_map: RepoMap) -> ArchitectureSummary:
    entrypoints = _expand_entrypoints(repo_map)
    component_summaries = _summarize_meaningful_components(repo_map)
    relationship_summaries = _summarize_relationships(repo_map)
    critical_paths = _derive_critical_paths(repo_map, entrypoints)
    validation_paths = _derive_validation_paths(repo_map)
    narrative = _build_architecture_narrative(repo_map, relationship_summaries, critical_paths, validation_paths)
    return ArchitectureSummary(
        component_summaries=component_summaries,
        entrypoints=entrypoints,
        narrative=narrative,
        relationship_summaries=relationship_summaries,
        critical_paths=critical_paths,
        validation_paths=validation_paths,
    )


def _summarize_meaningful_components(repo_map: RepoMap) -> list[str]:
    counts: dict[str, int] = {}
    for artifact in repo_map.artifacts:
        if not artifact.is_meaningful:
            continue
        subsystem = artifact.path.split("/", 1)[0]
        counts[subsystem] = counts.get(subsystem, 0) + 1
    return [f"{subsystem}: {count} meaningful artifact(s)" for subsystem, count in sorted(counts.items())]


def _build_architecture_narrative(
    repo_map: RepoMap,
    relationship_summaries: list[str],
    critical_paths: list[str],
    validation_paths: list[str],
) -> str:
    subsystem_count = len(repo_map.subsystems)
    edge_count = repo_map.graph.number_of_edges()
    if relationship_summaries and critical_paths:
        validation_clause = (
            f" The repo also exposes {len(validation_paths)} validation path(s) that show how tests and CI prove correctness."
            if validation_paths
            else ""
        )
        return (
            f"The repository is organized into {subsystem_count} top-level subsystem(s) with "
            f"{edge_count} inferred architecture relationship(s). Entrypoints identify operator-facing "
            "or executable surfaces, while the critical paths capture the main orchestration flows "
            f"that need to be preserved during reconstruction.{validation_clause}"
        )
    return (
        "The repository is organized around top-level subsystems discovered during cartography. "
        "Entrypoints highlight the files most likely to define usage, behavior, and orchestration."
    )


def _summarize_relationships(repo_map: RepoMap) -> list[str]:
    summaries: list[str] = []
    prioritized_edges = sorted(
        repo_map.graph.edges(),
        key=lambda edge: (
            _relationship_priority(repo_map.graph.nodes[edge[0]].get("artifact_type", "other")),
            edge[0],
            edge[1],
        ),
    )
    for source, target in prioritized_edges:
        source_type = repo_map.graph.nodes[source].get("artifact_type", "other")
        summaries.append(_describe_edge(source, source_type, target))
    return summaries[:20]


def _describe_edge(source: str, source_type: str, target: str) -> str:
    if source_type == "ci":
        return f"{source} invokes {target} during automated verification."
    if source_type == "test":
        return f"{source} validates {target} as part of the executable contract."
    if source_type == "script":
        return f"{source} launches or orchestrates {target}."
    if source_type == "code":
        return f"{source} depends on {target} for local runtime behavior."
    if source_type in {"skill", "prompt", "doc"}:
        return f"{source} references {target} as part of the documented workflow."
    return f"{source} relates to {target}."


def _derive_critical_paths(repo_map: RepoMap, entrypoints: list[str]) -> list[str]:
    critical_paths: list[str] = []
    starting_nodes = [node for node in entrypoints if repo_map.graph.out_degree(node) > 0]
    for start in starting_nodes:
        longest_path = _longest_reachable_path(repo_map.graph, start)
        if len(longest_path) > 1:
            critical_paths.append(" -> ".join(longest_path))
    return _unique_preserve_order(critical_paths)[:6]


def _derive_validation_paths(repo_map: RepoMap) -> list[str]:
    validation_paths: list[str] = []
    for node, attrs in sorted(repo_map.graph.nodes(data=True)):
        artifact_type = attrs.get("artifact_type")
        if artifact_type not in {"test", "ci"}:
            continue
        if repo_map.graph.out_degree(node) == 0:
            continue
        longest_path = _longest_reachable_path(repo_map.graph, node)
        if len(longest_path) > 1:
            validation_paths.append(" -> ".join(longest_path))
    return _unique_preserve_order(validation_paths)[:8]


def _longest_reachable_path(graph: nx.DiGraph, start: str) -> list[str]:
    best_path = [start]

    def dfs(node: str, path: list[str]) -> None:
        nonlocal best_path
        if len(path) > len(best_path):
            best_path = path[:]
        for neighbor in sorted(graph.successors(node)):
            if neighbor in path:
                continue
            dfs(neighbor, [*path, neighbor])

    dfs(start, [start])
    return best_path


def _unique_preserve_order(values: list[str]) -> list[str]:
    seen: list[str] = []
    for value in values:
        if value not in seen:
            seen.append(value)
    return seen


def _expand_entrypoints(repo_map: RepoMap) -> list[str]:
    entrypoints = list(repo_map.entrypoints)
    for node, attrs in repo_map.graph.nodes(data=True):
        artifact_type = attrs.get("artifact_type")
        if repo_map.graph.out_degree(node) == 0:
            continue
        if artifact_type in {"script", "ci"} and node not in entrypoints:
            entrypoints.append(node)
    return _unique_preserve_order(entrypoints)


def _relationship_priority(source_type: str) -> int:
    priorities = {
        "test": 0,
        "skill": 1,
        "prompt": 2,
        "doc": 3,
        "ci": 4,
        "script": 5,
        "code": 6,
    }
    return priorities.get(source_type, 7)
