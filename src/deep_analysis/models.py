from enum import Enum

from pydantic import BaseModel


class ArtifactType(str, Enum):
    CODE = "code"
    PROMPT = "prompt"
    SKILL = "skill"
    CONFIG = "config"
    TEST = "test"
    DOC = "doc"
    SCRIPT = "script"
    CI = "ci"
    HOOK = "hook"
    OTHER = "other"


class Artifact(BaseModel):
    path: str
    artifact_type: ArtifactType
    is_meaningful: bool


class RepoProfile(BaseModel):
    name: str
    root_path: str


class ArtifactFinding(BaseModel):
    path: str
    artifact_type: ArtifactType
    summary: str
    line_count: int
    key_signals: list[str]
    dependencies: list[str]
    failure_modes: list[str]
    reconstruction_notes: str


class WorkflowFinding(BaseModel):
    path: str
    summary: str
    trigger_conditions: list[str]
    steps: list[str]
    decision_gates: list[str] = []
    hard_constraints: list[str] = []
    approval_gates: list[str] = []
    review_loops: list[str] = []
    escalation_paths: list[str] = []
    reusable_patterns: list[str] = []
    human_role: str | None = None
    agent_role: str | None = None


class DoctrineSignal(BaseModel):
    category: str
    text: str
    evidence_path: str


class RepoDoctrine(BaseModel):
    core_beliefs: list[str]
    non_negotiables: list[str]
    quality_bar: list[str]
    operator_contract: list[str]
    anti_patterns: list[str]
    evidence_artifacts: list[str]
    signals: list[DoctrineSignal] = []


class RoleDefinition(BaseModel):
    name: str
    responsibilities: list[str]
    evidence_artifacts: list[str]


class RoleHandoff(BaseModel):
    source_role: str
    target_role: str
    contract: str
    evidence_artifacts: list[str]
    approval_owner: str | None = None
    escalation_owner: str | None = None


class RoleSystem(BaseModel):
    roles: list[RoleDefinition]
    handoffs: list[RoleHandoff]


class ArtifactTranslation(BaseModel):
    source_path: str
    source_artifact_type: ArtifactType
    source_role: str
    preservation_decision: str
    translation_action: str
    target_artifact_name: str
    target_artifact_type: str
    target_capability: str
    translation_reason: str


class VisionProfile(BaseModel):
    target_domain: str
    target_audience: list[str]
    philosophies: list[str]
    priorities: list[str]
    preferences: list[str]
    avoid: list[str]
    source_path: str | None = None


class DomainTranslationPlan(BaseModel):
    target_domain: str
    preserve_structures: list[str]
    rename_map: dict[str, str]
    role_map: dict[str, str]
    workflow_map: dict[str, str]
    artifact_map: list[ArtifactTranslation]
    language_shift_rules: list[str]
    target_capabilities: list[str]
    vision_alignment_notes: list[str]


class RepoWorkflowPattern(BaseModel):
    name: str
    summary: str
    evidence_artifacts: list[str]
    reconstruction_note: str


class PreservationDecision(BaseModel):
    path: str
    artifact_role: str
    decision: str
    strategy_note: str
    legal_review: str
    confidence: str
    rationale: str


class DossierSection(BaseModel):
    title: str
    body: str


class BlueprintPlan(BaseModel):
    repo_name: str
    next_steps: list[str]


class ArchitectureSummary(BaseModel):
    component_summaries: list[str]
    entrypoints: list[str] = []
    narrative: str = ""
    relationship_summaries: list[str] = []
    critical_paths: list[str] = []
    validation_paths: list[str] = []


class PreservationReport(BaseModel):
    decisions: list[PreservationDecision]
