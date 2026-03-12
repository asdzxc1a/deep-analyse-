from dataclasses import dataclass
from pathlib import Path

from deep_analysis.analysis.architecture import analyze_architecture
from deep_analysis.analysis.doctrine import analyze_doctrine
from deep_analysis.analysis.domain_translation import build_domain_translation_plan, parse_vision_file
from deep_analysis.analysis.equivalence import analyze_artifact_equivalence
from deep_analysis.analysis.logic import analyze_logic
from deep_analysis.analysis.preservation import analyze_preservation
from deep_analysis.analysis.roles import analyze_roles
from deep_analysis.analysis.workflows import analyze_workflows
from deep_analysis.analysis.workflows import synthesize_repo_workflow_patterns
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


def run_analysis_pipeline(
    repo_url_or_path: str,
    output_root: Path,
    export_skill_pack: bool,
    target_domain: str | None = None,
    vision_file: Path | None = None,
) -> PipelineResult:
    workspace = prepare_repo_workspace(repo_url_or_path, output_root / "workspace")
    repo_map = build_repo_map(workspace.source_repo_path)
    logic_findings = analyze_logic(workspace.source_repo_path, repo_map)
    workflow_findings = analyze_workflows(workspace.source_repo_path, repo_map)
    workflow_patterns = synthesize_repo_workflow_patterns(workflow_findings)
    architecture = analyze_architecture(repo_map)
    preservation = analyze_preservation(workspace.source_repo_path, repo_map)
    doctrine = analyze_doctrine(workspace.source_repo_path, repo_map, workflow_findings, preservation)
    roles = analyze_roles(workflow_findings)
    vision = parse_vision_file(vision_file, target_domain) if target_domain and vision_file is not None else None
    artifact_translations = (
        analyze_artifact_equivalence(repo_map, preservation, doctrine, roles, target_domain)
        if target_domain
        else None
    )
    translation_plan = (
        build_domain_translation_plan(
            workspace.source_repo_path.name,
            target_domain,
            repo_map,
            doctrine,
            roles,
            workflow_patterns,
            artifact_translations or [],
            vision,
        )
        if target_domain
        else None
    )

    if not repo_map.artifacts:
        raise ValueError("No artifacts found during analysis")
    if not any(artifact.is_meaningful for artifact in repo_map.artifacts):
        raise ValueError("No meaningful artifacts found during analysis")
    if not preservation.decisions:
        raise ValueError("No preservation decisions generated")

    analysis_project_dir = output_root / "analysis-project"
    blueprint_dir = output_root / "clone-blueprint"
    skill_pack_dir = output_root / "skill-pack" if export_skill_pack else None

    write_dossier(
        analysis_project_dir,
        workspace.source_repo_path.name,
        repo_map,
        logic_findings,
        workflow_findings,
        workflow_patterns,
        architecture,
        preservation,
        doctrine,
        roles,
        translation_plan,
    )
    write_blueprint_repo(
        blueprint_dir,
        workspace.source_repo_path.name,
        preservation.decisions,
        workflow_patterns,
        translation_plan,
    )

    if skill_pack_dir is not None:
        write_skill_pack(skill_pack_dir)

    return PipelineResult(
        analysis_project_dir=analysis_project_dir,
        blueprint_dir=blueprint_dir,
        skill_pack_dir=skill_pack_dir,
    )
