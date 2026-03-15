# Architecture Reconstruction Design

## Goal

Deepen system-level analysis so the dossier explains how a repository operates as a connected architecture rather than a collection of independently analyzed files.

This slice focuses on deterministic architecture reconstruction for agent, skill, prompt, and automation repositories. The system should infer meaningful relationships between artifacts from code references, workflow references, script invocations, and shared subsystem boundaries.

## Current Problem

The current architecture layer is too shallow. It reports subsystem counts and entrypoints, but it does not explain:
- which files depend on which other files
- where orchestration begins
- how scripts, code, and workflows connect
- which files form the most important operational paths

That means the dossier still lacks the “how this repo works as a system” view needed for reconstruction.

## Chosen Approach

Use deterministic relationship extraction rather than a full static-analysis engine.

The architecture analyzer will combine:
- repo-map structure
- local import and require references
- script-to-file invocations such as `node src/server.js`
- workflow references to scripts or commands
- doc/skill references to files when they are explicit and local

These relationships will be turned into:
- richer component summaries
- architecture narrative
- relationship summaries
- critical paths
- stronger entrypoint identification

## Design

### Data Model

`ArchitectureSummary` should be expanded to include:
- `relationship_summaries`: human-readable edges between artifacts or subsystems
- `critical_paths`: short descriptions of the most important runtime or orchestration flows

The existing fields remain:
- `component_summaries`
- `entrypoints`
- `narrative`

### Cartography

The existing `RepoMap.graph` is currently just a node list. It should begin carrying useful deterministic edges.

The graph should include:
- import/require edges for local code references
- script invocation edges when a shell file launches a local file
- workflow edges when CI commands reference local scripts or source files

This should remain heuristic and local-path-based. If a reference cannot be mapped to a local artifact safely, skip it.

### Architecture Analysis

`analyze_architecture(...)` should move from simple subsystem counting to architecture synthesis.

It should:
- summarize subsystem roles from meaningful artifact distribution
- surface graph edges as relationship summaries
- identify critical paths such as:
  - workflow -> script -> server
  - skill -> script companion
  - entrypoint -> runtime module
- expand entrypoints when a file is clearly executable, even if cartography did not mark it originally

### Dossier Output

The architecture section in the dossier should gain:
- `Relationships`
- `Critical Paths`

This should make the architecture page useful for rebuild planning instead of only for inventory.

## Non-Goals

This slice does not include:
- full cross-language semantic graphing
- call-graph reconstruction
- runtime tracing
- license or preservation logic changes
- UI changes

## Success Criteria

After this slice:
- the sample fixture repo architecture identifies real relationships across workflow, script, and code files
- the dossier architecture page includes relationship summaries and critical paths
- the `superpowers` smoke run shows architecture pages with connected system behavior, not just subsystem counts
- full tests and smoke runs pass
