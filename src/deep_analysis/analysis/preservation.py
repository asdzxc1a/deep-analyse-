from pathlib import Path

from deep_analysis.cartography import RepoMap
from deep_analysis.models import PreservationDecision, PreservationReport


def analyze_preservation(repo_root: Path, repo_map: RepoMap) -> PreservationReport:
    decisions: list[PreservationDecision] = []

    for artifact in repo_map.artifacts:
        if not artifact.is_meaningful:
            continue
        decision = "preserve"
        rationale = f"{artifact.path} contributes to the source system's observable behavior."
        decisions.append(
            PreservationDecision(
                path=artifact.path,
                decision=decision,
                rationale=rationale,
            )
        )

    return PreservationReport(decisions=decisions)
