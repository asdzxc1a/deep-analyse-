from pathlib import Path

from deep_analysis.analysis.workflows import analyze_workflows
from deep_analysis.analysis.logic import analyze_logic
from deep_analysis.cartography import build_repo_map


def test_logic_analysis_explains_meaningful_skill_file() -> None:
    repo_map = build_repo_map(Path("tests/fixtures/sample_agent_repo"))
    findings = analyze_logic(Path("tests/fixtures/sample_agent_repo"), repo_map)
    skill_finding = next(f for f in findings if f.path == "skills/example/SKILL.md")
    assert skill_finding.summary
    assert skill_finding.reconstruction_notes


def test_workflow_analysis_extracts_trigger_and_steps() -> None:
    repo_map = build_repo_map(Path("tests/fixtures/sample_agent_repo"))
    workflow_findings = analyze_workflows(Path("tests/fixtures/sample_agent_repo"), repo_map)
    finding = workflow_findings[0]
    assert finding.trigger_conditions
    assert finding.steps
