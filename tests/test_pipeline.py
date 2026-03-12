from pathlib import Path

from deep_analysis.analysis.architecture import analyze_architecture
from deep_analysis.analysis.workflows import analyze_workflows
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
    finding = workflow_findings[0]
    assert finding.trigger_conditions
    assert finding.steps


def test_workflow_analysis_extracts_prompt_workflows(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    prompt_dir = repo_root / "prompts"
    prompt_dir.mkdir(parents=True)
    (prompt_dir / "reviewer-prompt.md").write_text(
        "# Reviewer Prompt\n\nUse when reviewing a generated spec.\n\n1. Read the spec.\n2. List gaps.\n",
        encoding="utf-8",
    )

    repo_map = build_repo_map(repo_root)
    workflow_findings = analyze_workflows(repo_root, repo_map)
    prompt_finding = next(f for f in workflow_findings if f.path == "prompts/reviewer-prompt.md")
    assert "Use when reviewing a generated spec." in prompt_finding.trigger_conditions
    assert "Read the spec." in prompt_finding.steps


def test_architecture_and_preservation_use_repo_map() -> None:
    repo_root = Path("tests/fixtures/sample_agent_repo")
    repo_map = build_repo_map(repo_root)
    architecture = analyze_architecture(repo_map)
    preservation = analyze_preservation(repo_root, repo_map)
    assert architecture.component_summaries
    assert architecture.relationship_summaries
    assert architecture.critical_paths
    assert preservation.decisions


def test_write_dossier_creates_expected_directories(tmp_path: Path) -> None:
    output_dir = tmp_path / "analysis-project"
    repo_root = Path("tests/fixtures/sample_agent_repo")
    repo_map = build_repo_map(repo_root)
    logic_findings = analyze_logic(repo_root, repo_map)
    workflow_findings = analyze_workflows(repo_root, repo_map)
    architecture = analyze_architecture(repo_map)
    preservation = analyze_preservation(repo_root, repo_map)

    write_dossier(
        output_dir=output_dir,
        repo_name="sample",
        repo_map=repo_map,
        logic_findings=logic_findings,
        workflow_findings=workflow_findings,
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
    workflow_text = (
        output_dir / "04-workflows-prompts-skills" / "skills-example-skill-md.md"
    ).read_text(encoding="utf-8")
    assert "Trigger Conditions" in workflow_text
    assert "Read the repo." in workflow_text


def test_write_blueprint_repo_creates_starter_structure(tmp_path: Path) -> None:
    blueprint_dir = tmp_path / "clone-blueprint"
    repo_root = Path("tests/fixtures/sample_agent_repo")
    repo_map = build_repo_map(repo_root)
    preservation = analyze_preservation(repo_root, repo_map)

    write_blueprint_repo(
        blueprint_dir=blueprint_dir,
        repo_name="sample",
        preservation_decisions=preservation.decisions,
    )
    assert (blueprint_dir / "docs" / "preservation-matrix.md").exists()
    assert (blueprint_dir / "starter-src").exists()
    assert (blueprint_dir / "starter-tests").exists()
    preservation_text = (blueprint_dir / "docs" / "preservation-matrix.md").read_text(
        encoding="utf-8"
    )
    assert "skills/example/SKILL.md" in preservation_text
    assert "rewrite-equivalent" in preservation_text


def test_run_analysis_pipeline_writes_dossier_and_blueprint(tmp_path: Path) -> None:
    result = run_analysis_pipeline(
        repo_url_or_path="tests/fixtures/sample_agent_repo",
        output_root=tmp_path,
        export_skill_pack=False,
    )
    assert (result.analysis_project_dir / "01-source-profile").exists()
    assert (result.blueprint_dir / "docs" / "preservation-matrix.md").exists()
    assert (result.analysis_project_dir / "05-architecture" / "README.md").exists()
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
