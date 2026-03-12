from pathlib import Path

from deep_analysis.models import ArtifactTranslation, DomainTranslationPlan, VisionProfile


def parse_vision_file(vision_file: Path, target_domain: str) -> VisionProfile:
    text = vision_file.read_text(encoding="utf-8")
    audience: list[str] = []
    philosophies: list[str] = []
    priorities: list[str] = []
    preferences: list[str] = []
    avoid: list[str] = []
    section = ""

    for raw_line in text.splitlines():
        line = raw_line.strip()
        lower = line.lower()
        if not line:
            continue
        if line.startswith("#"):
            continue
        if lower.startswith("our philosophy"):
            section = "philosophy"
            continue
        if lower.startswith("prioritize"):
            section = "priorities"
            continue
        if lower.startswith("favor"):
            section = "preferences"
            continue
        if lower.startswith("avoid"):
            section = "avoid"
            continue
        if line.startswith("- "):
            item = line[2:].strip()
            if section == "philosophy":
                philosophies.append(item)
            elif section == "priorities":
                priorities.append(item)
            elif section == "preferences":
                preferences.append(item)
            elif section == "avoid":
                avoid.append(item)
            continue
        audience.append(line)

    return VisionProfile(
        target_domain=target_domain,
        target_audience=audience,
        philosophies=philosophies,
        priorities=priorities,
        preferences=preferences,
        avoid=avoid,
        source_path=str(vision_file),
    )


def build_domain_translation_plan(
    repo_name: str,
    target_domain: str,
    repo_map,
    doctrine,
    role_system,
    workflow_patterns: list,
    artifact_map: list[ArtifactTranslation],
    vision: VisionProfile | None,
) -> DomainTranslationPlan:
    rename_map = {artifact.source_path: artifact.target_artifact_name for artifact in artifact_map}
    role_map = {role.name: _translate_role(role.name, target_domain) for role in role_system.roles}
    workflow_map = {
        pattern.name: _translate_pattern_name(pattern.name, target_domain) for pattern in workflow_patterns
    }
    preserve_structures = [
        "approval gates",
        "review loops",
        "escalation paths",
        "human-agent handoffs",
    ]
    if repo_map.entrypoints:
        preserve_structures.append(f"entrypoints around {', '.join(repo_map.entrypoints[:3])}")

    target_capabilities = _unique_ordered(
        [artifact.target_capability for artifact in artifact_map]
        + (vision.priorities if vision else [])
    )
    language_shift_rules = _unique_ordered(
        [
            "Rewrite operator-facing language into the target domain vocabulary.",
            "Preserve workflow rigor even when renaming artifacts.",
            "Replace development-specific examples with target-domain examples.",
        ]
        + ([f"Favor {', '.join(vision.preferences)}."] if vision and vision.preferences else [])
        + ([f"Avoid {', '.join(vision.avoid)}."] if vision and vision.avoid else [])
    )
    vision_alignment_notes = _unique_ordered(
        (vision.target_audience if vision else [])
        + (vision.philosophies if vision else [])
        + doctrine.core_beliefs[:3]
        + [f"Translate {repo_name} into a {target_domain} operating system without dropping its review discipline."]
    )

    return DomainTranslationPlan(
        target_domain=target_domain,
        preserve_structures=preserve_structures,
        rename_map=rename_map,
        role_map=role_map,
        workflow_map=workflow_map,
        artifact_map=artifact_map,
        language_shift_rules=language_shift_rules,
        target_capabilities=target_capabilities,
        vision_alignment_notes=vision_alignment_notes,
    )


def _translate_role(role_name: str, target_domain: str) -> str:
    if target_domain == "marketing":
        mapping = {
            "Human reviewer": "Marketing lead",
            "Human operator": "Marketing operator",
            "Agent executor": "Campaign builder agent",
            "Agent reviewer": "Strategy reviewer agent",
        }
        return mapping.get(role_name, f"{role_name} ({target_domain})")
    return f"{role_name} ({target_domain})"


def _translate_pattern_name(pattern_name: str, target_domain: str) -> str:
    if target_domain == "marketing":
        mapping = {
            "human approval gate": "campaign approval gate",
            "iterative review loop": "iterative campaign review loop",
            "human escalation path": "campaign escalation path",
            "human-agent handoff": "marketing handoff",
            "guardrailed workflow": "guardrailed campaign workflow",
        }
        return mapping.get(pattern_name, f"{pattern_name} ({target_domain})")
    return f"{pattern_name} ({target_domain})"


def _unique_ordered(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered
