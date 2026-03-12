from deep_analysis.cartography import RepoMap
from deep_analysis.models import ArchitectureSummary


def analyze_architecture(repo_map: RepoMap) -> ArchitectureSummary:
    component_summaries = [
        f"{subsystem}: {len(paths)} artifact(s)"
        for subsystem, paths in sorted(repo_map.subsystems.items())
    ]
    narrative = (
        "The repository is organized around top-level subsystems discovered during cartography. "
        "Entrypoints highlight the files most likely to define usage, behavior, and orchestration."
    )
    return ArchitectureSummary(
        component_summaries=component_summaries,
        entrypoints=repo_map.entrypoints,
        narrative=narrative,
    )
