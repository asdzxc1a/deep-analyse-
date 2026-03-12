from deep_analysis.models import RoleDefinition, RoleHandoff, RoleSystem


def analyze_roles(workflow_findings: list) -> RoleSystem:
    role_evidence: dict[str, set[str]] = {}
    role_responsibilities: dict[str, list[str]] = {}
    handoffs: list[RoleHandoff] = []

    for finding in workflow_findings:
        role_names: list[str] = []
        if finding.human_role:
            human_name = _normalize_role_name(finding.human_role, default="Human reviewer")
            _record_role(role_evidence, role_responsibilities, human_name, finding.path, finding.human_role)
            role_names.append(human_name)
        if finding.agent_role:
            agent_name = _normalize_role_name(finding.agent_role, default="Agent executor")
            _record_role(role_evidence, role_responsibilities, agent_name, finding.path, finding.agent_role)
            role_names.append(agent_name)

        if len(role_names) >= 2:
            handoffs.append(
                RoleHandoff(
                    source_role=role_names[1],
                    target_role=role_names[0],
                    contract=finding.summary,
                    evidence_artifacts=[finding.path],
                    approval_owner=role_names[0] if finding.approval_gates else None,
                    escalation_owner=role_names[0] if finding.escalation_paths else None,
                )
            )

    roles = [
        RoleDefinition(
            name=name,
            responsibilities=_unique_ordered(role_responsibilities.get(name, [])),
            evidence_artifacts=sorted(role_evidence.get(name, set())),
        )
        for name in sorted(role_evidence)
    ]
    return RoleSystem(roles=roles, handoffs=handoffs)


def _normalize_role_name(text: str, default: str) -> str:
    lowered = text.lower()
    if "human reviewer" in lowered:
        return "Human reviewer"
    if "human operator" in lowered:
        return "Human operator"
    if "human" in lowered:
        return "Human reviewer"
    if "agent" in lowered and "review" in lowered:
        return "Agent reviewer"
    if "agent" in lowered:
        return "Agent executor"
    return default


def _record_role(
    role_evidence: dict[str, set[str]],
    role_responsibilities: dict[str, list[str]],
    name: str,
    evidence_path: str,
    responsibility: str,
) -> None:
    role_evidence.setdefault(name, set()).add(evidence_path)
    role_responsibilities.setdefault(name, []).append(responsibility)


def _unique_ordered(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered
