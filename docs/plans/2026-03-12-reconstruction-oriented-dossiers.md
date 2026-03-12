# Reconstruction-Oriented Dossiers Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make dossier pages directly useful for rebuilding a source repo with a unique vision, not just for reading about the source repo.

**Architecture:** Keep the current analyzers intact and deepen dossier synthesis. Combine logic findings, workflow findings, architecture relationships, and preservation decisions into explicit rebuild guidance on each page and in the reconstruction plan.

**Tech Stack:** Python 3.12, pytest, existing `deep_analysis` package

---

## File Structure

- Create: `docs/specs/2026-03-12-reconstruction-oriented-dossiers-design.md`
- Create: `docs/plans/2026-03-12-reconstruction-oriented-dossiers.md`
- Modify: `src/deep_analysis/synthesis/dossier.py`
- Modify: `tests/test_pipeline.py`
- Modify: `MEMORY.md`

## Chunk 1: Add Failing Tests For Reconstruction Guidance

### Task 1: Add dossier expectations for file and workflow rebuild guidance

**Files:**
- Modify: `tests/test_pipeline.py`

- [ ] **Step 1: Add assertions that file analysis pages include system role, preserve/change boundaries, rebuild strategy, and suggested first slice**
- [ ] **Step 2: Add assertions that workflow pages include rebuild guidance**
- [ ] **Step 3: Add assertions that the reconstruction plan mentions entrypoints, architecture, and preservation together**
- [ ] **Step 4: Run `source .venv/bin/activate && pytest tests/test_pipeline.py -q`**
- [ ] **Step 5: Verify the new tests fail because the dossier is still mostly descriptive**

## Chunk 2: Implement Reconstruction-Oriented Dossier Synthesis

### Task 2: Deepen file and workflow page rendering

**Files:**
- Modify: `src/deep_analysis/synthesis/dossier.py`

- [ ] **Step 1: Add file-page sections for system role, preserve in rebuild, safe to change, rebuild strategy, and suggested first slice**
- [ ] **Step 2: Add workflow-page reconstruction guidance**
- [ ] **Step 3: Keep rendering deterministic and derived from existing findings**
- [ ] **Step 4: Run `source .venv/bin/activate && pytest tests/test_pipeline.py -q`**
- [ ] **Step 5: Verify the targeted dossier tests pass**

### Task 3: Deepen the dossier-level reconstruction plan

**Files:**
- Modify: `src/deep_analysis/synthesis/dossier.py`

- [ ] **Step 1: Rewrite the reconstruction plan to prioritize entrypoints and dependency-aware first slices**
- [ ] **Step 2: Explicitly connect architecture, preservation matrix, and rebuild order**
- [ ] **Step 3: Re-run `source .venv/bin/activate && pytest tests/test_pipeline.py -q`**

## Chunk 3: Full Verification And Memory Refresh

### Task 4: Verify on the full suite and real repo

**Files:**
- Modify: `MEMORY.md`

- [ ] **Step 1: Run `source .venv/bin/activate && pytest -q`**
- [ ] **Step 2: Run `source .venv/bin/activate && python -m deep_analysis.cli analyze '/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers' /tmp/superpowers-rebuild-dossiers-20260312 --export-skill-pack`**
- [ ] **Step 3: Inspect representative file pages, workflow pages, and the reconstruction plan**
- [ ] **Step 4: Update `MEMORY.md` with the new slice and verification evidence**
- [ ] **Step 5: Commit the completed slice**
- [ ] **Step 6: Push the branch**
