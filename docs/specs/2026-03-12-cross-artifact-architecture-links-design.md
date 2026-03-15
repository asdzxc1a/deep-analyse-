# Cross-Artifact Architecture Links Design

## Goal

Deepen architecture reconstruction so docs, prompts, skills, and tests participate in the system graph instead of living mostly outside it.

## Problem

The current cartography layer is strongest for code and shell orchestration:
- JavaScript imports become graph edges
- shell scripts link to runtime targets
- CI workflows link to executed scripts

That leaves three important blind spots for agent/workflow repos:
- docs and READMEs often point to the real entrypoints and operational surfaces
- prompts and skills often reference concrete files, workflows, and scripts by path
- tests often define the contract of the system, but are not yet linked into the architecture map

As a result, the architecture page still under-represents “control paths” and “contract paths,” and dossier pages cannot yet say clearly what drives an artifact, what it drives, and what validates it.

## Design

### 1. Expand artifact classification for tests

Treat test files as first-class meaningful artifacts so they can participate in preservation, logic analysis, and architecture linking.

Heuristic scope for v1:
- files under `tests/`
- filenames beginning with `test_`
- `*.test.js`, `*.spec.js`, `*.test.ts`, `*.spec.ts`

### 2. Expand cartography edge extraction

Add deterministic edge extraction for:

- Python local imports
  - especially to connect test modules to local Python code
- path references in docs, prompts, and skills
  - explicit repo-local paths like `skills/foo/SKILL.md`, `scripts/start.sh`, `src/app.py`
- command references in docs and workflow-bearing markdown
  - commands that invoke local files should resolve to those targets

This slice stays deterministic and path-based. It does not attempt semantic NLP linking beyond direct file/path/command evidence.

### 3. Improve architecture synthesis

Use the richer graph to produce better relationship summaries, especially:
- doc or README entrypoints pointing into workflow/code artifacts
- skills/prompts driving scripts or code
- tests validating implementation artifacts

Relationship language should distinguish:
- operator/documented workflow references
- executable orchestration
- validation/contract coverage

### 4. Feed links back into dossier pages

Artifact pages should gain a connected-artifacts section that answers:
- what drives this artifact
- what this artifact drives
- what validates this artifact

This keeps the dossier reconstruction-oriented at the page level instead of only at the architecture summary level.

## Non-Goals

This slice does not:
- build a full call graph
- add heavy AST dependencies
- infer semantic links without explicit evidence
- redesign the blueprint format

## Success Criteria

After this slice:
- tests become meaningful architecture participants
- docs/prompts/skills can create graph edges via explicit path and command references
- architecture pages show validation and documented-control relationships more clearly
- file dossier pages can point to incoming, outgoing, and validating artifacts
