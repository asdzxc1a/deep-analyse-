from pathlib import Path

from deep_analysis.cartography import RepoMap
from deep_analysis.models import ArtifactFinding


def analyze_logic(repo_root: Path, repo_map: RepoMap) -> list[ArtifactFinding]:
    findings: list[ArtifactFinding] = []

    for artifact in repo_map.artifacts:
        if not artifact.is_meaningful:
            continue

        file_path = repo_root / artifact.path
        content = file_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        nonempty_lines = [line.strip() for line in lines if line.strip()]
        summary = _summarize_artifact(artifact.path, artifact.artifact_type.value, nonempty_lines)
        key_signals = _extract_key_signals(nonempty_lines)
        dependencies = _extract_dependencies(nonempty_lines)
        failure_modes = _derive_failure_modes(artifact.path, artifact.artifact_type.value)
        reconstruction_notes = f"Preserve the role of {artifact.path} and rebuild it with equivalent behavior."

        findings.append(
            ArtifactFinding(
                path=artifact.path,
                artifact_type=artifact.artifact_type,
                summary=summary,
                line_count=len(lines),
                key_signals=key_signals,
                dependencies=dependencies,
                failure_modes=failure_modes,
                reconstruction_notes=reconstruction_notes,
            )
        )

    return findings


def _summarize_artifact(path: str, artifact_type: str, nonempty_lines: list[str]) -> str:
    first_heading = next((line.lstrip("# ").strip() for line in nonempty_lines if line.startswith("#")), "")
    if "SKILL.md" in path:
        description = next((line.split(":", 1)[1].strip() for line in nonempty_lines if line.startswith("description:")), "")
        if description:
            return f"Skill definition for {path} that activates when {description}."
        if first_heading:
            return f"Skill artifact {path} centered on '{first_heading}'."
    if ".github/workflows/" in path:
        return f"CI workflow at {path} that defines automated verification or delivery steps."
    if first_heading:
        return f"{artifact_type.capitalize()} artifact at {path} focused on '{first_heading}'."
    if nonempty_lines:
        return f"{artifact_type.capitalize()} artifact at {path} beginning with '{nonempty_lines[0]}'."
    return f"{artifact_type.capitalize()} artifact at {path}."


def _extract_key_signals(nonempty_lines: list[str]) -> list[str]:
    signals: list[str] = []
    for line in nonempty_lines:
        if line.startswith(("name:", "description:", "##", "# ", "def ", "class ", "on:", "jobs:")):
            signals.append(line)
        if len(signals) == 5:
            break
    return signals


def _extract_dependencies(nonempty_lines: list[str]) -> list[str]:
    deps: list[str] = []
    for line in nonempty_lines:
        stripped = line.strip()
        if stripped.startswith(("import ", "from ", "uses:", "run:")):
            deps.append(stripped)
        if len(deps) == 5:
            break
    return deps


def _derive_failure_modes(path: str, artifact_type: str) -> list[str]:
    return [
        f"If {path} changes shape or location, any references to it may break.",
        f"If the {artifact_type} semantics drift, downstream reconstruction guidance may become inaccurate.",
    ]
