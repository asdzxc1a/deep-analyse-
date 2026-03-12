# Validation-Aware Architecture Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make architecture output distinguish runtime paths from validation paths and use both in reconstruction guidance.

**Architecture:** Extend the existing deterministic graph synthesis instead of replacing it. Add a separate validation-path bucket sourced from tests and CI, expose it in the architecture dossier, and thread the result into reconstruction guidance and tests.

**Tech Stack:** Python 3.12, pytest, NetworkX, existing deep-analysis architecture pipeline

---

## Chunk 1: Red Tests For Validation Paths

**Files:**
- Modify: `tests/test_pipeline.py`

- [ ] **Step 1: Add failing architecture assertions for validation paths**

- [ ] **Step 2: Add failing dossier assertions for a `Validation Paths` section**

- [ ] **Step 3: Add failing reconstruction-plan assertions for validation-aware rebuild order**

- [ ] **Step 4: Run targeted tests to capture the red state**

Run: `source .venv/bin/activate && pytest tests/test_pipeline.py -q`
Expected: FAIL on the new validation-path assertions

## Chunk 2: Implement Validation-Aware Architecture

**Files:**
- Modify: `src/deep_analysis/models.py`
- Modify: `src/deep_analysis/analysis/architecture.py`
- Modify: `src/deep_analysis/synthesis/dossier.py`

- [ ] **Step 1: Add architecture summary support for validation paths**

- [ ] **Step 2: Derive validation paths from test and CI graph sources**

- [ ] **Step 3: Update architecture narrative and dossier rendering**

- [ ] **Step 4: Update reconstruction guidance to mention validation flow**

- [ ] **Step 5: Run targeted tests until green**

Run: `source .venv/bin/activate && pytest tests/test_pipeline.py -q`
Expected: PASS

## Chunk 3: Final V1 Verification And Documentation

**Files:**
- Modify: `README.md`
- Modify: `MEMORY.md`

- [ ] **Step 1: Run the full test suite**

Run: `source .venv/bin/activate && pytest -q`
Expected: PASS

- [ ] **Step 2: Run a fresh smoke analysis against `superpowers`**

Run: `source .venv/bin/activate && python -m deep_analysis.cli analyze '/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers' /tmp/superpowers-v1-final-20260312 --export-skill-pack`
Expected: analysis-project, clone-blueprint, and skill-pack all generated successfully

- [ ] **Step 3: Refresh README and MEMORY so the app is shippable as a coherent v1**

- [ ] **Step 4: Commit and push**
