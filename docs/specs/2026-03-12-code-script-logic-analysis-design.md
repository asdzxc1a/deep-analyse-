# Code And Script Logic Analysis Design

## Goal

Deepen dossier quality for code and script artifacts so generated analysis pages explain what a file does, what it depends on, how it is likely invoked, and what will break if its assumptions drift.

This slice focuses on agent, skill, prompt, and automation repositories, where operational logic often lives in small Python, JavaScript, TypeScript, and shell files.

## Current Problem

The existing logic analyzer is still too shallow for code-bearing artifacts. For many files it produces summaries based on the first heading or first non-empty line, which makes the dossier read like indexing rather than reverse engineering.

This is especially visible in repos like `superpowers`, where support scripts and orchestration files are part of the system behavior and need deeper treatment.

## Chosen Approach

Use file-type-specific structural analysis instead of a heavy AST or parser stack.

The analyzer will branch by artifact type:
- `code` files: detect imports, defined symbols, likely entrypoints, top-level side effects, and likely system role
- `script` files: detect commands, environment variables, file/process side effects, and operational risks
- `skill`, `prompt`, `doc`, and `ci` artifacts: keep the current heuristic path as the fallback

This keeps the slice small, deterministic, and strong enough to materially improve the generated dossier.

## Design

### Logic Analysis

`src/deep_analysis/analysis/logic.py` will be refactored into a dispatcher plus small helpers.

Expected helpers:
- code analyzer for Python and JS/TS files
- script analyzer for shell files
- fallback analyzer for docs, prompts, skills, and CI

For code artifacts, the analyzer should extract:
- imported modules or packages
- defined functions and classes
- likely entrypoint markers such as `if __name__ == "__main__":`, CLI startup calls, `main()`, `app.listen(...)`, or module exports
- top-level side effects such as server startup, immediate execution, env loading, or file writes
- a better role-oriented summary

For script artifacts, the analyzer should extract:
- invoked commands
- referenced environment variables
- file system effects such as `mkdir`, `cp`, `mv`, `rm`, redirection, or chmod
- process control behavior such as `kill`, `pkill`, `nohup`, or background execution
- operational risks and reconstruction notes based on those behaviors

### Output Shape

The current `ArtifactFinding` shape is probably sufficient if we make the fields better:
- `summary` becomes role-oriented
- `key_signals` includes defined symbols, entrypoints, commands, and side-effect markers
- `dependencies` includes imports, command dependencies, and env assumptions
- `failure_modes` becomes specific to the detected behavior
- `reconstruction_notes` becomes more concrete for operational rebuilding

Only extend the model if implementation shows a clear need.

### Dossier Behavior

`src/deep_analysis/synthesis/dossier.py` should remain stable. The goal is for richer logic findings to improve the existing pages automatically, not to trigger another output format redesign.

## Non-Goals

This slice does not include:
- full AST parsing or parser-heavy dependencies
- full architecture reconstruction
- license-aware preservation logic
- interactive rebuild tooling
- UI changes

## Success Criteria

After this slice:
- code-file pages name real symbols, imports, and likely entrypoints
- shell-script pages name commands, env assumptions, and side effects
- the `superpowers` dossier reads more like reverse engineering than placeholder summarization
- tests cover the new behavior with focused fixtures
- full repo tests and a fresh smoke run both pass
