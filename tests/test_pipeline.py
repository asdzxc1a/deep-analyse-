from pathlib import Path

from deep_analysis.analysis.architecture import analyze_architecture
from deep_analysis.analysis.workflows import analyze_workflows
from deep_analysis.analysis.logic import analyze_logic
from deep_analysis.analysis.preservation import analyze_preservation
from deep_analysis.cartography import build_repo_map
from deep_analysis.pipeline import run_analysis_pipeline
from deep_analysis.synthesis.blueprint import write_blueprint_repo
from deep_analysis.synthesis.dossier import write_dossier


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


def test_architecture_and_preservation_use_repo_map() -> None:
    repo_root = Path("tests/fixtures/sample_agent_repo")
    repo_map = build_repo_map(repo_root)
    architecture = analyze_architecture(repo_map)
    preservation = analyze_preservation(repo_root, repo_map)
    assert architecture.component_summaries
    assert preservation.decisions


def test_write_dossier_creates_expected_directories(tmp_path: Path) -> None:
    output_dir = tmp_path / "analysis-project"
    write_dossier(output_dir=output_dir, repo_name="sample", repo_map=None, findings=[])
    assert (output_dir / "01-source-profile").exists()
    assert (output_dir / "03-file-analysis").exists()


def test_write_blueprint_repo_creates_starter_structure(tmp_path: Path) -> None:
    blueprint_dir = tmp_path / "clone-blueprint"
    write_blueprint_repo(blueprint_dir=blueprint_dir, repo_name="sample", preservation_decisions=[])
    assert (blueprint_dir / "docs" / "preservation-matrix.md").exists()
    assert (blueprint_dir / "starter-src").exists()
    assert (blueprint_dir / "starter-tests").exists()


def test_run_analysis_pipeline_writes_dossier_and_blueprint(tmp_path: Path) -> None:
    result = run_analysis_pipeline(
        repo_url_or_path="tests/fixtures/sample_agent_repo",
        output_root=tmp_path,
        export_skill_pack=False,
    )
    assert (result.analysis_project_dir / "01-source-profile").exists()
    assert (result.blueprint_dir / "docs" / "preservation-matrix.md").exists()
