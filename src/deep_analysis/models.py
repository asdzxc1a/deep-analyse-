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


class PreservationDecision(BaseModel):
    path: str
    decision: str
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


class PreservationReport(BaseModel):
    decisions: list[PreservationDecision]
