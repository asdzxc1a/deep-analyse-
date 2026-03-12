import re
from pathlib import Path, PurePosixPath

from deep_analysis.cartography import RepoMap
from deep_analysis.models import ArtifactFinding, ArtifactType


def analyze_logic(repo_root: Path, repo_map: RepoMap) -> list[ArtifactFinding]:
    findings: list[ArtifactFinding] = []

    for artifact in repo_map.artifacts:
        if not artifact.is_meaningful:
            continue

        file_path = repo_root / artifact.path
        content = file_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        nonempty_lines = [line.strip() for line in lines if line.strip()]

        if artifact.artifact_type in {ArtifactType.CODE, ArtifactType.TEST}:
            findings.append(_analyze_code_artifact(artifact.path, artifact.artifact_type, lines, nonempty_lines))
            continue
        if artifact.artifact_type is ArtifactType.SCRIPT:
            findings.append(_analyze_script_artifact(artifact.path, lines, nonempty_lines))
            continue

        findings.append(_analyze_fallback_artifact(artifact.path, artifact.artifact_type, lines, nonempty_lines))

    return findings


def _analyze_code_artifact(
    path: str,
    artifact_type: ArtifactType,
    lines: list[str],
    nonempty_lines: list[str],
) -> ArtifactFinding:
    suffix = PurePosixPath(path).suffix
    if suffix == ".py":
        return _analyze_python_artifact(path, artifact_type, lines, nonempty_lines)
    return _analyze_javascript_artifact(path, artifact_type, lines, nonempty_lines)


def _analyze_python_artifact(
    path: str,
    artifact_type: ArtifactType,
    lines: list[str],
    nonempty_lines: list[str],
) -> ArtifactFinding:
    imports = [line.strip() for line in lines if line.strip().startswith(("import ", "from "))]
    function_names = re.findall(r"^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", "\n".join(lines), flags=re.MULTILINE)
    class_names = re.findall(r"^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)\s*[:(]", "\n".join(lines), flags=re.MULTILINE)
    key_signals = [*class_names, *function_names]

    if '__name__ == "__main__"' in "\n".join(lines):
        key_signals.append("Entry point via __main__ guard.")

    summary = _summarize_python_artifact(path, artifact_type, class_names, function_names, key_signals)
    dependencies = _limit_unique(imports)
    failure_modes = [
        f"If imports used by {path} move or disappear, the module will fail before its core logic runs.",
        "Entry point assumptions will drift if CLI startup behavior changes without updating orchestration.",
    ]
    reconstruction_notes = _build_reconstruction_notes(path, key_signals, "module")

    return ArtifactFinding(
        path=path,
        artifact_type=artifact_type,
        summary=summary,
        line_count=len(lines),
        key_signals=_limit_unique(key_signals),
        dependencies=dependencies,
        failure_modes=failure_modes,
        reconstruction_notes=reconstruction_notes,
    )


def _analyze_javascript_artifact(
    path: str,
    artifact_type: ArtifactType,
    lines: list[str],
    nonempty_lines: list[str],
) -> ArtifactFinding:
    content = "\n".join(lines)
    imports = [line.strip() for line in lines if _is_javascript_import(line.strip())]
    function_names = re.findall(r"^\s*function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", content, flags=re.MULTILINE)
    function_names.extend(
        re.findall(
            r"^\s*(?:const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[A-Za-z_][A-Za-z0-9_]*)\s*=>",
            content,
            flags=re.MULTILINE,
        )
    )

    key_signals = _limit_unique(function_names)
    if "module.exports" in content:
        key_signals.append("Exports symbols via module.exports.")
    if "require.main === module" in content or "app.listen(" in content or ".listen(" in content:
        key_signals.append("Runtime entrypoint detected.")

    summary = _summarize_javascript_artifact(path, artifact_type, function_names)
    dependencies = _limit_unique(imports)
    failure_modes = [
        f"If required modules in {path} change shape, startup will fail before request handling begins.",
    ]
    if ".listen(" in content:
        failure_modes.append("Starts a listener or server process at module runtime.")
    else:
        failure_modes.append("Runtime invocation assumptions may drift if entrypoint behavior changes.")
    reconstruction_notes = _build_reconstruction_notes(path, function_names, "service module")

    return ArtifactFinding(
        path=path,
        artifact_type=artifact_type,
        summary=summary,
        line_count=len(lines),
        key_signals=_limit_unique(key_signals),
        dependencies=dependencies,
        failure_modes=failure_modes,
        reconstruction_notes=reconstruction_notes,
    )


def _analyze_script_artifact(path: str, lines: list[str], nonempty_lines: list[str]) -> ArtifactFinding:
    commands = _extract_shell_commands(lines)
    env_vars = _extract_env_vars("\n".join(lines))
    key_signals = _extract_script_signals(lines, commands)
    dependencies = _limit_unique(commands + env_vars)
    summary = _summarize_script_artifact(path, lines, commands)
    failure_modes = [
        f"If command availability or paths referenced by {path} change, the script will fail during orchestration.",
    ]
    if _script_writes_files(lines):
        failure_modes.append("Writes files or directories as part of execution.")
    else:
        failure_modes.append("Operational assumptions may drift if runtime setup changes.")
    reconstruction_notes = _build_script_reconstruction_notes(path, commands, env_vars)

    return ArtifactFinding(
        path=path,
        artifact_type=ArtifactType.SCRIPT,
        summary=summary,
        line_count=len(lines),
        key_signals=key_signals,
        dependencies=dependencies,
        failure_modes=failure_modes,
        reconstruction_notes=reconstruction_notes,
    )


def _analyze_fallback_artifact(
    path: str,
    artifact_type: ArtifactType,
    lines: list[str],
    nonempty_lines: list[str],
) -> ArtifactFinding:
    summary = _summarize_fallback_artifact(path, artifact_type.value, nonempty_lines)
    key_signals = _extract_fallback_key_signals(nonempty_lines)
    dependencies = _extract_fallback_dependencies(nonempty_lines)
    failure_modes = _derive_fallback_failure_modes(path, artifact_type.value)
    reconstruction_notes = f"Preserve the role of {path} and rebuild it with equivalent behavior."

    return ArtifactFinding(
        path=path,
        artifact_type=artifact_type,
        summary=summary,
        line_count=len(lines),
        key_signals=key_signals,
        dependencies=dependencies,
        failure_modes=failure_modes,
        reconstruction_notes=reconstruction_notes,
    )


def _summarize_python_artifact(
    path: str,
    artifact_type: ArtifactType,
    class_names: list[str],
    function_names: list[str],
    key_signals: list[str],
) -> str:
    artifact_label = "Python test module" if artifact_type is ArtifactType.TEST else "Python module"
    named_items = [*class_names, *function_names]
    if named_items:
        lead = ", ".join(named_items[:3])
        suffix = " and exposes an executable entrypoint." if "Entry point via __main__ guard." in key_signals else "."
        return f"{artifact_label} at {path} defines {lead}{suffix}"
    return f"{artifact_label} at {path} with limited structural signals."


def _summarize_javascript_artifact(path: str, artifact_type: ArtifactType, function_names: list[str]) -> str:
    artifact_label = "JavaScript test module" if artifact_type is ArtifactType.TEST else "JavaScript module"
    if function_names:
        lead = ", ".join(function_names[:3])
        return f"{artifact_label} at {path} defines {lead} and coordinates runtime startup."
    return f"{artifact_label} at {path} with limited structural signals."


def _summarize_script_artifact(path: str, lines: list[str], commands: list[str]) -> str:
    runtime_target = next((_extract_runtime_command(line) for line in lines if "node " in line), "")
    if runtime_target:
        return f"Shell script at {path} launches {runtime_target} and manages runtime artifacts."
    if commands:
        return f"Shell script at {path} orchestrates {', '.join(commands[:3])}."
    return f"Shell script at {path} with limited operational signals."


def _summarize_fallback_artifact(path: str, artifact_type: str, nonempty_lines: list[str]) -> str:
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


def _extract_fallback_key_signals(nonempty_lines: list[str]) -> list[str]:
    signals: list[str] = []
    for line in nonempty_lines:
        if line.startswith(("name:", "description:", "##", "# ", "def ", "class ", "on:", "jobs:")):
            signals.append(line)
        if len(signals) == 5:
            break
    return signals


def _extract_fallback_dependencies(nonempty_lines: list[str]) -> list[str]:
    deps: list[str] = []
    for line in nonempty_lines:
        stripped = line.strip()
        if stripped.startswith(("import ", "from ", "uses:", "run:")):
            deps.append(stripped)
        if len(deps) == 5:
            break
    return deps


def _derive_fallback_failure_modes(path: str, artifact_type: str) -> list[str]:
    return [
        f"If {path} changes shape or location, any references to it may break.",
        f"If the {artifact_type} semantics drift, downstream reconstruction guidance may become inaccurate.",
    ]


def _is_javascript_import(line: str) -> bool:
    return (
        line.startswith("import ")
        or " require(" in line
        or line.startswith("const ")
        or line.startswith("let ")
        or line.startswith("var ")
    ) and "require(" in line or line.startswith("import ")


def _extract_shell_commands(lines: list[str]) -> list[str]:
    commands: list[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#") or line in {"set -e", "set -u", "set -eu"}:
            continue
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", line):
            continue
        token = _extract_shell_command_token(line)
        if not token:
            continue
        commands.append(token)
    return _limit_unique(commands)


def _extract_env_vars(content: str) -> list[str]:
    matches = re.findall(r"\$\{?([A-Z][A-Z0-9_]*)", content)
    return _limit_unique(matches)


def _extract_script_signals(lines: list[str], commands: list[str]) -> list[str]:
    signals: list[str] = []
    for line in lines:
        stripped = line.strip()
        if "nohup" in stripped:
            signals.append("nohup")
        if "&" in stripped and not stripped.startswith("#"):
            signals.append("Background process launch detected.")
        if "chmod " in stripped:
            signals.append("Adjusts file permissions.")
        if re.search(r">\s*['\"]?[^'\"]+", stripped) or " > " in stripped:
            signals.append("Redirects command output to files.")
        if len(signals) >= 5:
            break
    signals.extend(commands[:2])
    return _limit_unique(signals)


def _script_writes_files(lines: list[str]) -> bool:
    markers = ("mkdir ", "cp ", "mv ", "rm ", "chmod ", ">", ">>")
    return any(any(marker in line for marker in markers) for line in lines)


def _build_reconstruction_notes(path: str, key_signals: list[str], artifact_role: str) -> str:
    if key_signals:
        lead = ", ".join(key_signals[:3])
        return f"Rebuild {path} as a {artifact_role} that preserves these observable responsibilities: {lead}."
    return f"Preserve the role of {path} and rebuild it with equivalent behavior."


def _build_script_reconstruction_notes(path: str, commands: list[str], env_vars: list[str]) -> str:
    details: list[str] = []
    if commands:
        details.append(f"command flow ({', '.join(commands[:3])})")
    if env_vars:
        details.append(f"environment contract ({', '.join(env_vars[:3])})")
    if details:
        return f"Rebuild {path} with the same {' and '.join(details)}."
    return f"Preserve the role of {path} and rebuild it with equivalent behavior."


def _limit_unique(values: list[str], limit: int = 8) -> list[str]:
    seen: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.append(value)
        if len(seen) == limit:
            break
    return seen


def _extract_shell_command_token(line: str) -> str | None:
    cleaned = line.lstrip("(")
    parts = cleaned.split()
    if not parts:
        return None

    control_flow = {"while", "case", "do", "done", "then", "fi", "if", "else", "elif", "esac", "for", "in"}
    if parts[0] in control_flow:
        return None

    index = 0
    if parts[0] == "env":
        index = 1

    while index < len(parts) and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", parts[index]):
        index += 1

    if index >= len(parts):
        return None

    token = parts[index]
    if token in control_flow or token in {"shift", "break", "continue", ";;"}:
        return None

    if token.endswith(")") or token.startswith("--"):
        return None

    shell_builtins = {"echo", "exit", "cd", "export", "local", "read", "printf", "return", "trap", "source", "."}
    if token in shell_builtins:
        return None

    return token


def _extract_runtime_command(line: str) -> str:
    stripped = line.strip()
    if not stripped:
        return ""

    if stripped.startswith("env "):
        parts = stripped.split()
        index = 1
        while index < len(parts) and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", parts[index]):
            index += 1
        stripped = " ".join(parts[index:])

    stripped = stripped.split(">", 1)[0].strip()
    stripped = stripped.rstrip("&").strip()
    return stripped
