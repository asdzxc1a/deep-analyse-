from dataclasses import dataclass
from pathlib import Path

from deep_analysis.analysis.architecture import analyze_architecture
from deep_analysis.analysis.logic import analyze_logic
from deep_analysis.analysis.preservation import analyze_preservation
from deep_analysis.analysis.workflows import analyze_workflows
from deep_analysis.cartography import build_repo_map
from deep_analysis.git_utils import prepare_repo_workspace
from deep_analysis.synthesis.blueprint import write_blueprint_repo
from deep_analysis.synthesis.dossier import write_dossier
from deep_analysis.synthesis.skill_pack import write_skill_pack


@dataclass(slots=True)
class PipelineResult:
    analysis_project_dir: Path
    blueprint_dir: Path
    skill_pack_dir: Path | None


def run_analysis_pipeline(repo_url_or_path: str, output_root: Path, export_skill_pack: bool) -> PipelineResult:
    workspace = prepare_repo_workspace(repo_url_or_path, output_root / "workspace")
    repo_map = build_repo_map(workspace.source_repo_path)
    logic_findings = analyze_logic(workspace.source_repo_path, repo_map)
    workflow_findings = analyze_workflows(workspace.source_repo_path, repo_map)
    architecture = analyze_architecture(repo_map)
    preservation = analyze_preservation(workspace.source_repo_path, repo_map)

    if not repo_map.artifacts:
        raise ValueError("No artifacts found during analysis")
    if not any(artifact.is_meaningful for artifact in repo_map.artifacts):
        raise ValueError("No meaningful artifacts found during analysis")
    if not preservation.decisions:
        raise ValueError("No preservation decisions generated")

    analysis_project_dir = output_root / "analysis-project"
    blueprint_dir = output_root / "clone-blueprint"
    skill_pack_dir = output_root / "skill-pack" if export_skill_pack else None

    all_findings = list(logic_findings) + list(workflow_findings) + [architecture]
    write_dossier(analysis_project_dir, workspace.source_repo_path.name, repo_map, all_findings)
    write_blueprint_repo(blueprint_dir, workspace.source_repo_path.name, preservation.decisions)

    if skill_pack_dir is not None:
        write_skill_pack(skill_pack_dir)

    return PipelineResult(
        analysis_project_dir=analysis_project_dir,
        blueprint_dir=blueprint_dir,
        skill_pack_dir=skill_pack_dir,
    )
