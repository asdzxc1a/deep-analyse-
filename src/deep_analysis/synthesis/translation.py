from deep_analysis.models import DomainTranslationPlan, RepoDoctrine, RoleSystem


def render_doctrine(doctrine: RepoDoctrine) -> str:
    lines = ["# Doctrine", "", "## Core Beliefs", ""]
    lines.extend(f"- {item}" for item in doctrine.core_beliefs or ["None"])
    lines.extend(["", "## Non-Negotiables", ""])
    lines.extend(f"- {item}" for item in doctrine.non_negotiables or ["None"])
    lines.extend(["", "## Quality Bar", ""])
    lines.extend(f"- {item}" for item in doctrine.quality_bar or ["None"])
    lines.extend(["", "## Operator Contract", ""])
    lines.extend(f"- {item}" for item in doctrine.operator_contract or ["None"])
    lines.extend(["", "## Anti-Patterns", ""])
    lines.extend(f"- {item}" for item in doctrine.anti_patterns or ["None"])
    lines.extend(["", "## Evidence Artifacts", ""])
    lines.extend(f"- {item}" for item in doctrine.evidence_artifacts or ["None"])
    lines.append("")
    return "\n".join(lines)


def render_role_system(role_system: RoleSystem) -> str:
    lines = ["# Role System", "", "## Roles", ""]
    if role_system.roles:
        for role in role_system.roles:
            lines.extend([f"### {role.name}", ""])
            lines.extend(f"- {item}" for item in role.responsibilities or ["No responsibilities captured"])
            lines.extend(["", "Evidence:", ""])
            lines.extend(f"- {item}" for item in role.evidence_artifacts or ["None"])
            lines.append("")
    else:
        lines.append("No roles captured.")
    lines.extend(["## Handoffs", ""])
    if role_system.handoffs:
        for handoff in role_system.handoffs:
            lines.extend(
                [
                    f"- {handoff.source_role} -> {handoff.target_role}: {handoff.contract}",
                    f"  - Approval owner: {handoff.approval_owner or 'None'}",
                    f"  - Escalation owner: {handoff.escalation_owner or 'None'}",
                ]
            )
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def render_domain_translation(plan: DomainTranslationPlan) -> str:
    lines = [f"# Domain Translation ({plan.target_domain})", "", "## Preserve Structures", ""]
    lines.extend(f"- {item}" for item in plan.preserve_structures or ["None"])
    lines.extend(["", "## Role Map", ""])
    lines.extend(f"- {source} -> {target}" for source, target in plan.role_map.items() or [("None", "None")])
    lines.extend(["", "## Workflow Map", ""])
    lines.extend(f"- {source} -> {target}" for source, target in plan.workflow_map.items() or [("None", "None")])
    lines.extend(["", "## Language Shift Rules", ""])
    lines.extend(f"- {item}" for item in plan.language_shift_rules or ["None"])
    lines.extend(["", "## Target Capabilities", ""])
    lines.extend(f"- {item}" for item in plan.target_capabilities or ["None"])
    lines.extend(["", "## Vision Alignment Notes", ""])
    lines.extend(f"- {item}" for item in plan.vision_alignment_notes or ["None"])
    lines.append("")
    return "\n".join(lines)


def render_artifact_equivalence(plan: DomainTranslationPlan) -> str:
    lines = [
        "# Artifact Equivalence",
        "",
        "| Source Path | Action | Target Artifact | Target Type | Target Capability | Reason |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for artifact in plan.artifact_map:
        lines.append(
            f"| {artifact.source_path} | {artifact.translation_action} | {artifact.target_artifact_name} | "
            f"{artifact.target_artifact_type} | {artifact.target_capability} | {artifact.translation_reason} |"
        )
    return "\n".join(lines) + "\n"


def render_target_doctrine(plan: DomainTranslationPlan) -> str:
    return (
        f"# Target Doctrine ({plan.target_domain})\n\n"
        "## Translation Rules\n\n"
        + "\n".join(f"- {item}" for item in plan.language_shift_rules or ["None"])
        + "\n\n## Vision Alignment\n\n"
        + "\n".join(f"- {item}" for item in plan.vision_alignment_notes or ["None"])
        + "\n"
    )


def render_target_role_system(plan: DomainTranslationPlan) -> str:
    lines = [f"# Target Role System ({plan.target_domain})", ""]
    lines.extend(f"- {source} -> {target}" for source, target in plan.role_map.items() or [("None", "None")])
    lines.append("")
    return "\n".join(lines)


def render_domain_translation_map(plan: DomainTranslationPlan) -> str:
    lines = [f"# Domain Translation Map ({plan.target_domain})", ""]
    lines.extend(f"- {source} -> {target}" for source, target in plan.rename_map.items() or [("None", "None")])
    lines.append("")
    return "\n".join(lines)


def render_capability_map(plan: DomainTranslationPlan) -> str:
    lines = [f"# {plan.target_domain.capitalize()} Capability Map", ""]
    lines.extend(f"- {item}" for item in plan.target_capabilities or ["None"])
    lines.append("")
    return "\n".join(lines)
