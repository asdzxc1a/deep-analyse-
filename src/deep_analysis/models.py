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
    summary: str
    reconstruction_notes: str


class WorkflowFinding(BaseModel):
    path: str
    trigger_conditions: list[str]
    steps: list[str]


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


class PreservationReport(BaseModel):
    decisions: list[PreservationDecision]
