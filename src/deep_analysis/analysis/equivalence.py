from pathlib import Path

from deep_analysis.models import ArtifactTranslation, ArtifactType


def analyze_artifact_equivalence(
    repo_map,
    preservation,
    doctrine,
    role_system,
    target_domain: str,
) -> list[ArtifactTranslation]:
    del doctrine, role_system

    translations: list[ArtifactTranslation] = []
    decisions_by_path = {decision.path: decision for decision in preservation.decisions}

    for artifact in repo_map.artifacts:
        if not artifact.is_meaningful:
            continue
        decision = decisions_by_path.get(artifact.path)
        source_name = Path(artifact.path).stem
        target_name, target_type, capability, action = _map_target(target_domain, artifact.path, artifact.artifact_type)
        translations.append(
            ArtifactTranslation(
                source_path=artifact.path,
                source_artifact_type=artifact.artifact_type,
                source_role=decision.artifact_role if decision else "meaningful artifact",
                preservation_decision=decision.decision if decision else "review",
                translation_action=action,
                target_artifact_name=target_name or source_name,
                target_artifact_type=target_type,
                target_capability=capability,
                translation_reason=_build_reason(target_domain, artifact.path, decision.decision if decision else "review"),
            )
        )
    return translations


def _map_target(target_domain: str, path: str, artifact_type: ArtifactType) -> tuple[str, str, str, str]:
    base = Path(path).stem.replace("_", "-")
    if target_domain == "marketing":
        if "systematic-debugging" in path:
            return "systematic-campaign-diagnosis", "skill", "campaign diagnosis", "replace-with-target-equivalent"
        if "writing-plans" in path:
            return "campaign-planning", "skill", "campaign planning", "replace-with-target-equivalent"
        if "requesting-code-review" in path:
            return "requesting-strategy-review", "skill", "strategy review", "replace-with-target-equivalent"
        if "verification-before-completion" in path:
            return "verification-before-launch", "skill", "launch verification", "replace-with-target-equivalent"
        if artifact_type == ArtifactType.SKILL:
            return f"{base}-marketing", "skill", "marketing workflow", "translate-domain"
        if artifact_type == ArtifactType.PROMPT:
            return f"{base}-marketing", "prompt", "marketing prompt", "rewrite-in-user-voice"
        if artifact_type == ArtifactType.TEST:
            return f"{base}-marketing", "test", "marketing verification", "preserve-structure"
        if artifact_type == ArtifactType.DOC:
            return f"{base}-marketing", "doc", "marketing doctrine", "rewrite-in-user-voice"
        if artifact_type == ArtifactType.SCRIPT:
            return f"{base}-marketing", "script", "campaign runtime support", "translate-domain"
        if artifact_type == ArtifactType.CODE:
            return f"{base}-marketing", "code", "marketing runtime", "preserve-structure"
    return base, artifact_type.value, f"{target_domain} capability", "translate-domain"


def _build_reason(target_domain: str, path: str, preservation_decision: str) -> str:
    return (
        f"Translate {path} into a {target_domain}-domain equivalent while respecting preservation decision "
        f"`{preservation_decision}`."
    )
