# Architecture Reconstruction Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reconstruct architecture relationships across meaningful artifacts so the dossier explains how a repo operates as an interconnected system.

**Architecture:** Extend cartography with deterministic edges from local references, then synthesize those edges into richer architecture summaries, relationships, critical paths, and executable entrypoints. Keep this heuristic and local-path-based so it remains stable and fast for agent/workflow repos.

**Tech Stack:** Python 3.12, pytest, networkx, existing `deep_analysis` package

---

## File Structure

- Create: `docs/specs/2026-03-12-architecture-reconstruction-design.md`
- Create: `docs/plans/2026-03-12-architecture-reconstruction.md`
- Modify: `src/deep_analysis/models.py`
- Modify: `src/deep_analysis/cartography.py`
- Modify: `src/deep_analysis/analysis/architecture.py`
- Modify: `src/deep_analysis/pipeline.py`
- Modify: `src/deep_analysis/synthesis/dossier.py`
- Modify: `tests/test_cartography.py`
- Modify: `tests/test_pipeline.py`
- Modify: `MEMORY.md`

## Chunk 1: Red Tests For Architecture Relationships

### Task 1: Add failing tests for graph edges and architecture synthesis

**Files:**
- Modify: `tests/test_cartography.py`
- Modify: `tests/test_pipeline.py`

- [ ] **Step 1: Write a test asserting cartography records local workflow/script/code edges in the repo graph**
- [ ] **Step 2: Write a test asserting architecture analysis returns relationship summaries and critical paths**
- [ ] **Step 3: Write a dossier rendering test that expects `Relationships` and `Critical Paths` in the architecture page**
- [ ] **Step 4: Run `source .venv/bin/activate && pytest tests/test_cartography.py tests/test_pipeline.py -q`**
- [ ] **Step 5: Verify the new tests fail because architecture reconstruction is not implemented yet**

## Chunk 2: Implement Graph Extraction And Architecture Synthesis

### Task 2: Extend cartography with deterministic local-reference edges

**Files:**
- Modify: `src/deep_analysis/cartography.py`

- [ ] **Step 1: Add helpers that inspect local file contents for import/require references**
- [ ] **Step 2: Add helpers that detect script invocations of local files**
- [ ] **Step 3: Add helpers that detect CI command references to local scripts or sources**
- [ ] **Step 4: Add graph edges only when a referenced local artifact exists**

### Task 3: Synthesize relationships into architecture summaries

**Files:**
- Modify: `src/deep_analysis/models.py`
- Modify: `src/deep_analysis/analysis/architecture.py`
- Modify: `src/deep_analysis/pipeline.py`
- Modify: `src/deep_analysis/synthesis/dossier.py`

- [ ] **Step 1: Extend `ArchitectureSummary` with relationship and critical-path fields**
- [ ] **Step 2: Refactor `analyze_architecture(...)` to inspect the graph and generate narrative, relationship summaries, and critical paths**
- [ ] **Step 3: Update pipeline calls if the analyzer signature changes**
- [ ] **Step 4: Update dossier rendering to show architecture relationships and critical paths**
- [ ] **Step 5: Run `source .venv/bin/activate && pytest tests/test_cartography.py tests/test_pipeline.py -q`**
- [ ] **Step 6: Verify the targeted tests pass**

## Chunk 3: Full Verification And Memory Refresh

### Task 4: Verify on the full suite and a real repo

**Files:**
- Modify: `MEMORY.md`

- [ ] **Step 1: Run `source .venv/bin/activate && pytest -q`**
- [ ] **Step 2: Run `source .venv/bin/activate && python -m deep_analysis.cli analyze '/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers' /tmp/superpowers-architecture-20260312 --export-skill-pack`**
- [ ] **Step 3: Inspect the generated architecture page for real relationships and critical paths**
- [ ] **Step 4: Update `MEMORY.md` with the new slice and verification evidence**
- [ ] **Step 5: Commit the completed slice**
- [ ] **Step 6: Push the branch**
