from pathlib import Path

from deep_analysis.models import ArtifactType
from deep_analysis.models import DoctrineSignal, RepoDoctrine


def analyze_doctrine(repo_root: Path, repo_map, workflow_findings: list, preservation) -> RepoDoctrine:
    signals: list[DoctrineSignal] = []
    for finding in workflow_findings:
        for item in finding.hard_constraints:
            lowered = item.lower()
            if _is_noise_line(item):
                continue
            signals.append(DoctrineSignal(category="non_negotiable", text=item, evidence_path=finding.path))
            lowered = item.lower()
            if "quality" in lowered or "approval" in lowered or "review" in lowered or "guess" in lowered:
                signals.append(DoctrineSignal(category="belief", text=item, evidence_path=finding.path))
        for item in finding.approval_gates:
            if not _is_noise_line(item):
                signals.append(DoctrineSignal(category="operator_contract", text=item, evidence_path=finding.path))
        for item in finding.review_loops:
            if not _is_noise_line(item):
                signals.append(DoctrineSignal(category="quality_bar", text=item, evidence_path=finding.path))
        for item in finding.escalation_paths:
            if not _is_noise_line(item):
                signals.append(DoctrineSignal(category="anti_pattern", text=item, evidence_path=finding.path))
        for role_text in [finding.human_role, finding.agent_role]:
            if role_text:
                signals.append(DoctrineSignal(category="operator_contract", text=role_text, evidence_path=finding.path))

    for artifact in repo_map.artifacts:
        if not artifact.is_meaningful or artifact.artifact_type not in {ArtifactType.DOC, ArtifactType.SKILL, ArtifactType.PROMPT}:
            continue
        path = repo_root / artifact.path
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            lowered = stripped.lower()
            if _is_noise_line(stripped):
                continue
            if lowered.startswith("this repo believes") or lowered.startswith("operators should") or "quality means" in lowered:
                signals.append(DoctrineSignal(category="belief", text=stripped, evidence_path=artifact.path))
            if lowered.startswith("you must") or lowered.startswith("do not") or lowered.startswith("never"):
                signals.append(DoctrineSignal(category="non_negotiable", text=stripped, evidence_path=artifact.path))
            if "approve" in lowered or "approval" in lowered or lowered.startswith("human ") or "operator" in lowered:
                signals.append(DoctrineSignal(category="operator_contract", text=stripped, evidence_path=artifact.path))
            if lowered.startswith("if the loop exceeds") or lowered.startswith("escalate") or "bypass" in lowered:
                signals.append(DoctrineSignal(category="anti_pattern", text=stripped, evidence_path=artifact.path))

    for decision in preservation.decisions:
        if "verification intent" in decision.strategy_note.lower() or "review" in decision.strategy_note.lower():
            signals.append(
                DoctrineSignal(
                    category="quality_bar",
                    text=decision.strategy_note,
                    evidence_path=decision.path,
                )
            )

    return RepoDoctrine(
        core_beliefs=_unique_ordered(_category_texts(signals, "belief")),
        non_negotiables=_unique_ordered(_category_texts(signals, "non_negotiable")),
        quality_bar=_unique_ordered(_category_texts(signals, "quality_bar")),
        operator_contract=_unique_ordered(_category_texts(signals, "operator_contract")),
        anti_patterns=_unique_ordered(_category_texts(signals, "anti_pattern")),
        evidence_artifacts=_unique_ordered(signal.evidence_path for signal in signals),
        signals=signals,
    )


def _category_texts(signals: list[DoctrineSignal], category: str) -> list[str]:
    return [signal.text for signal in signals if signal.category == category]


def _unique_ordered(items) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def _is_noise_line(text: str) -> bool:
    stripped = text.strip()
    lowered = stripped.lower()
    if not stripped:
        return True
    if stripped.startswith("#"):
        return True
    if stripped.startswith("```") or stripped.startswith("|"):
        return True
    if "`" in stripped:
        return True
    if len(stripped) > 2 and stripped[0].isdigit() and stripped[1:3] == ". ":
        return True
    if lowered.startswith("verify installation") or lowered.startswith("verify syntax"):
        return True
    if lowered.startswith("step ") or lowered.startswith("run:") or lowered.startswith("expected:"):
        return True
    if lowered.startswith("purpose:") or lowered.startswith("description:"):
        return True
    return False
