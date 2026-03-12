from pathlib import Path

from deep_analysis.analysis.architecture import analyze_architecture
from deep_analysis.analysis.workflows import analyze_workflows
from deep_analysis.analysis.workflows import synthesize_repo_workflow_patterns
from deep_analysis.analysis.logic import analyze_logic
from deep_analysis.analysis.preservation import analyze_preservation
from deep_analysis.cartography import build_repo_map
from deep_analysis.pipeline import run_analysis_pipeline
from deep_analysis.synthesis.blueprint import write_blueprint_repo
from deep_analysis.synthesis.dossier import write_dossier
from deep_analysis.synthesis.skill_pack import write_skill_pack


def test_logic_analysis_explains_meaningful_skill_file() -> None:
    repo_map = build_repo_map(Path("tests/fixtures/sample_agent_repo"))
    findings = analyze_logic(Path("tests/fixtures/sample_agent_repo"), repo_map)
    skill_finding = next(f for f in findings if f.path == "skills/example/SKILL.md")
    assert skill_finding.summary
    assert skill_finding.reconstruction_notes


def test_logic_analysis_extracts_python_file_structure() -> None:
    repo_map = build_repo_map(Path("tests/fixtures/sample_agent_repo"))
    findings = analyze_logic(Path("tests/fixtures/sample_agent_repo"), repo_map)
    python_finding = next(f for f in findings if f.path == "src/example.py")
    assert "ExampleRunner" in python_finding.summary
    assert "load_config" in python_finding.key_signals
    assert "main" in python_finding.key_signals
    assert "import os" in python_finding.dependencies
    assert "Entry point via __main__ guard." in python_finding.key_signals


def test_logic_analysis_extracts_javascript_file_structure() -> None:
    repo_map = build_repo_map(Path("tests/fixtures/sample_agent_repo"))
    findings = analyze_logic(Path("tests/fixtures/sample_agent_repo"), repo_map)
    js_finding = next(f for f in findings if f.path == "src/server.js")
    assert "startServer" in js_finding.summary
    assert 'const express = require("express");' in js_finding.dependencies
    assert "Exports symbols via module.exports." in js_finding.key_signals
    assert "Starts a listener or server process at module runtime." in js_finding.failure_modes


def test_logic_analysis_extracts_shell_script_behavior() -> None:
    repo_map = build_repo_map(Path("tests/fixtures/sample_agent_repo"))
    findings = analyze_logic(Path("tests/fixtures/sample_agent_repo"), repo_map)
    shell_finding = next(f for f in findings if f.path == "scripts/start-example.sh")
    assert "node src/server.js" in shell_finding.summary
    assert "PORT" in shell_finding.dependencies
    assert "nohup" in shell_finding.key_signals
    assert "while" not in shell_finding.key_signals
    assert "case" not in shell_finding.key_signals
    assert "Writes files or directories as part of execution." in shell_finding.failure_modes


def test_logic_analysis_ignores_shell_control_flow_when_finding_commands(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    script_dir = repo_root / "scripts"
    script_dir.mkdir(parents=True)
    (script_dir / "start.sh").write_text(
        """#!/usr/bin/env bash
set -eu

while [[ $# -gt 0 ]]; do
  case "$1" in
    --foreground)
      FOREGROUND=1
      shift
      ;;
  esac
done

PORT="${PORT:-3000}"
env PORT="$PORT" node index.js > logs/app.log 2>&1 &
""",
        encoding="utf-8",
    )

    repo_map = build_repo_map(repo_root)
    findings = analyze_logic(repo_root, repo_map)
    shell_finding = next(f for f in findings if f.path == "scripts/start.sh")
    assert "while" not in shell_finding.key_signals
    assert "case" not in shell_finding.key_signals
    assert "--foreground)" not in shell_finding.key_signals
    assert ";;" not in shell_finding.key_signals
    assert "node" in shell_finding.dependencies
    assert "PORT" in shell_finding.dependencies


def test_workflow_analysis_extracts_trigger_and_steps() -> None:
    repo_map = build_repo_map(Path("tests/fixtures/sample_agent_repo"))
    workflow_findings = analyze_workflows(Path("tests/fixtures/sample_agent_repo"), repo_map)
    finding = next(f for f in workflow_findings if f.path == "skills/example/SKILL.md")
    assert finding.trigger_conditions
    assert finding.steps
    assert finding.hard_constraints
    assert finding.approval_gates
    assert finding.review_loops
    assert finding.escalation_paths
    assert finding.reusable_patterns


def test_workflow_analysis_extracts_prompt_semantics() -> None:
    repo_root = Path("tests/fixtures/sample_agent_repo")
    repo_map = build_repo_map(repo_root)
    workflow_findings = analyze_workflows(repo_root, repo_map)
    prompt_finding = next(f for f in workflow_findings if f.path == "prompts/reviewer-prompt.md")
    assert "Use when reviewing a generated spec before implementation." in prompt_finding.trigger_conditions
    assert "Read the spec." in prompt_finding.steps
    assert any("MUST identify any requirement gaps" in item for item in prompt_finding.hard_constraints)
    assert any("approval" in item.lower() for item in prompt_finding.approval_gates)
    assert any("repeat until approved" in item.lower() for item in prompt_finding.review_loops)
    assert any("escalate" in item.lower() for item in prompt_finding.escalation_paths)
    assert "iterative review loop" in prompt_finding.reusable_patterns


def test_repo_workflow_pattern_synthesis_aggregates_repeated_semantics() -> None:
    repo_root = Path("tests/fixtures/sample_agent_repo")
    repo_map = build_repo_map(repo_root)
    workflow_findings = analyze_workflows(repo_root, repo_map)
    patterns = synthesize_repo_workflow_patterns(workflow_findings)
    pattern_names = {pattern.name for pattern in patterns}
    assert "human approval gate" in pattern_names
    assert "iterative review loop" in pattern_names
    assert "human escalation path" in pattern_names
    assert "human-agent handoff" in pattern_names
    approval_pattern = next(pattern for pattern in patterns if pattern.name == "human approval gate")
    assert "skills/example/SKILL.md" in approval_pattern.evidence_artifacts
    assert "prompts/reviewer-prompt.md" in approval_pattern.evidence_artifacts
    assert approval_pattern.reconstruction_note


def test_workflow_analysis_ignores_fenced_code_blocks(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    skill_dir = repo_root / "skills" / "example"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        """---
name: example
description: Use when testing semantic extraction
---

# Example

1. Review the file.
2. Wait for approval.

You MUST wait for user approval.

```dot
"Spec review passed?" -> "Spec review loop" [label="issues found"];
```
""",
        encoding="utf-8",
    )

    repo_map = build_repo_map(repo_root)
    workflow_findings = analyze_workflows(repo_root, repo_map)
    finding = next(f for f in workflow_findings if f.path == "skills/example/SKILL.md")
    joined = "\n".join(
        [
            *finding.hard_constraints,
            *finding.approval_gates,
            *finding.review_loops,
            *finding.escalation_paths,
        ]
    )
    assert "Spec review passed?" not in joined


def test_architecture_and_preservation_use_repo_map() -> None:
    repo_root = Path("tests/fixtures/sample_agent_repo")
    repo_map = build_repo_map(repo_root)
    assert repo_map.graph.has_edge("README.md", "skills/example/SKILL.md")
    assert repo_map.graph.has_edge("README.md", "prompts/reviewer-prompt.md")
    assert repo_map.graph.has_edge("README.md", "scripts/start-example.sh")
    assert repo_map.graph.has_edge("README.md", "tests/test_example.py")
    assert repo_map.graph.has_edge("skills/example/SKILL.md", "prompts/reviewer-prompt.md")
    assert repo_map.graph.has_edge("skills/example/SKILL.md", "scripts/start-example.sh")
    assert repo_map.graph.has_edge("skills/example/SKILL.md", "src/example.py")
    assert repo_map.graph.has_edge("prompts/reviewer-prompt.md", "src/example.py")
    assert repo_map.graph.has_edge("prompts/reviewer-prompt.md", "tests/test_example.py")
    assert repo_map.graph.has_edge("tests/test_example.py", "src/example.py")
    architecture = analyze_architecture(repo_map)
    preservation = analyze_preservation(repo_root, repo_map)
    assert architecture.component_summaries
    assert architecture.relationship_summaries
    assert architecture.critical_paths
    assert any("README.md references skills/example/SKILL.md" in item for item in architecture.relationship_summaries)
    assert any("tests/test_example.py validates src/example.py" in item for item in architecture.relationship_summaries)
    assert preservation.decisions
    decisions = {decision.path: decision for decision in preservation.decisions}
    assert decisions["README.md"].decision == "rewrite-with-differentiation"
    assert decisions["skills/example/SKILL.md"].decision == "rewrite-equivalent"
    assert decisions["src/server.js"].decision == "preserve-core-behavior"
    assert decisions["tests/test_example.py"].decision == "preserve-core-behavior"
    assert decisions["scripts/start-example.sh"].artifact_role == "behavior-bearing implementation"
    assert decisions["skills/example/SKILL.md"].legal_review == "recommended"
    assert decisions["src/server.js"].confidence == "medium"
    assert decisions["README.md"].strategy_note


def test_write_dossier_creates_expected_directories(tmp_path: Path) -> None:
    output_dir = tmp_path / "analysis-project"
    repo_root = Path("tests/fixtures/sample_agent_repo")
    repo_map = build_repo_map(repo_root)
    logic_findings = analyze_logic(repo_root, repo_map)
    workflow_findings = analyze_workflows(repo_root, repo_map)
    architecture = analyze_architecture(repo_map)
    preservation = analyze_preservation(repo_root, repo_map)
    workflow_patterns = synthesize_repo_workflow_patterns(workflow_findings)

    write_dossier(
        output_dir=output_dir,
        repo_name="sample",
        repo_map=repo_map,
        logic_findings=logic_findings,
        workflow_findings=workflow_findings,
        workflow_patterns=workflow_patterns,
        architecture=architecture,
        preservation=preservation,
    )
    assert (output_dir / "01-source-profile").exists()
    assert (output_dir / "03-file-analysis").exists()
    assert (output_dir / "03-file-analysis" / "skills-example-skill-md.md").exists()
    assert (output_dir / "04-workflows-prompts-skills" / "skills-example-skill-md.md").exists()
    repo_map_text = (output_dir / "02-repo-map" / "README.md").read_text(encoding="utf-8")
    assert "skills/example/SKILL.md" in repo_map_text
    file_analysis_text = (
        output_dir / "03-file-analysis" / "skills-example-skill-md.md"
    ).read_text(encoding="utf-8")
    assert "Artifact Type: skill" in file_analysis_text
    assert "Reconstruction Notes" in file_analysis_text
    assert "System Role" in file_analysis_text
    assert "Preserve In Rebuild" in file_analysis_text
    assert "Safe To Change" in file_analysis_text
    assert "Rebuild Strategy" in file_analysis_text
    assert "Suggested First Slice" in file_analysis_text
    assert "Connected Artifacts" in file_analysis_text
    workflow_text = (
        output_dir / "04-workflows-prompts-skills" / "skills-example-skill-md.md"
    ).read_text(encoding="utf-8")
    assert "Trigger Conditions" in workflow_text
    assert "Read the repo." in workflow_text
    assert "Hard Constraints" in workflow_text
    assert "Approval Gates" in workflow_text
    assert "Review Loops" in workflow_text
    assert "Escalation Paths" in workflow_text
    assert "Reusable Patterns" in workflow_text
    assert "Rebuild Guidance" in workflow_text
    repo_patterns_text = (
        output_dir / "04-workflows-prompts-skills" / "repo-patterns.md"
    ).read_text(encoding="utf-8")
    assert "Repo Workflow Patterns" in repo_patterns_text
    assert "human approval gate" in repo_patterns_text
    assert "Evidence Artifacts" in repo_patterns_text
    assert "skills/example/SKILL.md" in repo_patterns_text
    reconstruction_text = (output_dir / "07-reconstruction-plan" / "README.md").read_text(
        encoding="utf-8"
    )
    assert "Start with executable or operator-facing entrypoints" in reconstruction_text
    assert "preservation matrix" in reconstruction_text
    assert "architecture page" in reconstruction_text
    assert "repo workflow patterns" in reconstruction_text
    test_analysis_text = (
        output_dir / "03-file-analysis" / "tests-test-example-py.md"
    ).read_text(encoding="utf-8")
    assert "Artifact Type: test" in test_analysis_text
    assert "Connected Artifacts" in test_analysis_text
    assert "Drives" in test_analysis_text
    assert "src/example.py" in test_analysis_text


def test_write_blueprint_repo_creates_starter_structure(tmp_path: Path) -> None:
    blueprint_dir = tmp_path / "clone-blueprint"
    repo_root = Path("tests/fixtures/sample_agent_repo")
    repo_map = build_repo_map(repo_root)
    preservation = analyze_preservation(repo_root, repo_map)
    workflow_findings = analyze_workflows(repo_root, repo_map)
    workflow_patterns = synthesize_repo_workflow_patterns(workflow_findings)

    write_blueprint_repo(
        blueprint_dir=blueprint_dir,
        repo_name="sample",
        preservation_decisions=preservation.decisions,
        workflow_patterns=workflow_patterns,
    )
    assert (blueprint_dir / "docs" / "preservation-matrix.md").exists()
    assert (blueprint_dir / "docs" / "workflow-patterns.md").exists()
    assert (blueprint_dir / "starter-src").exists()
    assert (blueprint_dir / "starter-tests").exists()
    preservation_text = (blueprint_dir / "docs" / "preservation-matrix.md").read_text(
        encoding="utf-8"
    )
    assert "skills/example/SKILL.md" in preservation_text
    assert "rewrite-equivalent" in preservation_text
    assert "Role" in preservation_text
    assert "Legal Review" in preservation_text
    assert "Confidence" in preservation_text
    assert "Strategy Note" in preservation_text
    workflow_pattern_text = (blueprint_dir / "docs" / "workflow-patterns.md").read_text(
        encoding="utf-8"
    )
    assert "human approval gate" in workflow_pattern_text
    assert "skills/example/SKILL.md" in workflow_pattern_text


def test_run_analysis_pipeline_writes_dossier_and_blueprint(tmp_path: Path) -> None:
    result = run_analysis_pipeline(
        repo_url_or_path="tests/fixtures/sample_agent_repo",
        output_root=tmp_path,
        export_skill_pack=False,
    )
    assert (result.analysis_project_dir / "01-source-profile").exists()
    assert (result.blueprint_dir / "docs" / "preservation-matrix.md").exists()
    assert (result.blueprint_dir / "docs" / "workflow-patterns.md").exists()
    assert (result.analysis_project_dir / "05-architecture" / "README.md").exists()
    assert (result.analysis_project_dir / "04-workflows-prompts-skills" / "repo-patterns.md").exists()
    architecture_text = (result.analysis_project_dir / "05-architecture" / "README.md").read_text(
        encoding="utf-8"
    )
    assert "Entry Points" in architecture_text
    assert "Relationships" in architecture_text
    assert "Critical Paths" in architecture_text


def test_write_skill_pack_creates_reusable_analysis_workflow(tmp_path: Path) -> None:
    write_skill_pack(tmp_path)
    skill_text = (tmp_path / "analysis-system" / "SKILL.md").read_text(encoding="utf-8")
    assert "Analyze one repository at a time" in skill_text
    assert "clone blueprint" in skill_text
