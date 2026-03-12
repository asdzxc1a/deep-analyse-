from pathlib import Path

from deep_analysis.cartography import RepoMap
from deep_analysis.models import ArtifactType, PreservationDecision, PreservationReport


def analyze_preservation(repo_root: Path, repo_map: RepoMap) -> PreservationReport:
    decisions: list[PreservationDecision] = []

    for artifact in repo_map.artifacts:
        if not artifact.is_meaningful:
            continue
        artifact_role = _classify_artifact_role(artifact.path, artifact.artifact_type)
        decision = _choose_decision(artifact.path, artifact.artifact_type, artifact_role)
        strategy_note = _build_strategy_note(artifact_role, decision)
        legal_review = _determine_legal_review(artifact_role, decision)
        confidence = _determine_confidence(artifact.artifact_type, decision)
        rationale = _build_rationale(artifact.path, artifact_role, decision)
        decisions.append(
            PreservationDecision(
                path=artifact.path,
                artifact_role=artifact_role,
                decision=decision,
                strategy_note=strategy_note,
                legal_review=legal_review,
                confidence=confidence,
                rationale=rationale,
            )
        )

    return PreservationReport(decisions=decisions)


def _classify_artifact_role(path: str, artifact_type: ArtifactType) -> str:
    if artifact_type in {ArtifactType.CODE, ArtifactType.SCRIPT, ArtifactType.TEST, ArtifactType.HOOK}:
        return "behavior-bearing implementation"
    if artifact_type in {ArtifactType.CI, ArtifactType.CONFIG}:
        return "environment-coupled operations"
    if artifact_type in {ArtifactType.SKILL, ArtifactType.PROMPT}:
        return "human-facing workflow system"
    if artifact_type is ArtifactType.DOC and _is_strategy_doc(path):
        return "strategy-bearing language"
    if artifact_type is ArtifactType.DOC:
        return "human-facing workflow reference"
    return "supporting artifact"


def _choose_decision(path: str, artifact_type: ArtifactType, artifact_role: str) -> str:
    if artifact_role == "strategy-bearing language":
        return "rewrite-with-differentiation"
    if artifact_role in {"human-facing workflow system", "human-facing workflow reference"}:
        return "rewrite-equivalent"
    if artifact_role == "environment-coupled operations":
        return "preserve-with-review"
    if artifact_role == "behavior-bearing implementation":
        return "preserve-core-behavior"
    return "preserve-with-review" if artifact_type in {ArtifactType.CI, ArtifactType.CONFIG} else "preserve-core-behavior"


def _build_strategy_note(artifact_role: str, decision: str) -> str:
    if decision == "rewrite-with-differentiation":
        return "Preserve the product role, but intentionally differentiate the language, framing, and positioning."
    if decision == "rewrite-equivalent":
        return "Preserve the operator workflow and system intent, but rewrite the wording into your own voice."
    if decision == "preserve-with-review":
        return "Preserve the operational role, but review environment assumptions and coupling before reuse."
    if artifact_role == "behavior-bearing implementation":
        return "Preserve the observable behavior, interfaces, and orchestration role while allowing implementation changes."
    return "Preserve the artifact's system role with targeted human review."


def _determine_legal_review(artifact_role: str, decision: str) -> str:
    if decision == "rewrite-with-differentiation":
        return "required-before-reuse"
    if artifact_role in {"human-facing workflow system", "human-facing workflow reference"}:
        return "recommended"
    if artifact_role == "environment-coupled operations":
        return "recommended"
    return "not-usually-needed"


def _determine_confidence(artifact_type: ArtifactType, decision: str) -> str:
    if artifact_type in {ArtifactType.SKILL, ArtifactType.PROMPT, ArtifactType.DOC}:
        return "high"
    if decision == "preserve-core-behavior":
        return "medium"
    return "medium"


def _build_rationale(path: str, artifact_role: str, decision: str) -> str:
    if decision == "rewrite-with-differentiation":
        return (
            f"{path} shapes positioning or operator-facing language. Preserve the system role, but rewrite the framing "
            "and wording so the rebuilt system has its own strategic voice."
        )
    if decision == "rewrite-equivalent":
        return (
            f"{path} carries human-facing workflow semantics. Preserve the process and intent, but re-express the text "
            "in your own language."
        )
    if decision == "preserve-with-review":
        return (
            f"{path} encodes operational or environment-specific behavior. Preserve it carefully, but review coupling, "
            "assumptions, and direct reuse risks before carrying it forward."
        )
    return (
        f"{path} is {artifact_role} and contributes to observable system behavior. Preserve the role and interfaces, "
        "but allow implementation-level changes."
    )


def _is_strategy_doc(path: str) -> bool:
    normalized = path.lower()
    return any(
        token in normalized
        for token in (
            "readme",
            "release-notes",
            "release_notes",
            "positioning",
            "marketing",
        )
    )
