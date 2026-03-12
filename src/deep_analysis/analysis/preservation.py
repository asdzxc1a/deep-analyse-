from pathlib import Path

from deep_analysis.cartography import RepoMap
from deep_analysis.models import PreservationDecision, PreservationReport


def analyze_preservation(repo_root: Path, repo_map: RepoMap) -> PreservationReport:
    decisions: list[PreservationDecision] = []

    for artifact in repo_map.artifacts:
        if not artifact.is_meaningful:
            continue
        if artifact.artifact_type.value in {"skill", "prompt", "doc"}:
            decision = "rewrite-equivalent"
            rationale = (
                f"{artifact.path} carries human-facing language and workflow semantics that should be "
                "re-expressed in your own voice while preserving intent."
            )
        elif artifact.artifact_type.value in {"ci", "config"}:
            decision = "preserve-with-review"
            rationale = f"{artifact.path} encodes operational behavior that can be preserved with environment-specific review."
        else:
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
