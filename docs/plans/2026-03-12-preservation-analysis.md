# Preservation Analysis Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make preservation analysis more reconstruction-grade by adding richer decisions, clearer rationale, strategy notes, and future legal-review signals.

**Architecture:** Extend the preservation decision model, deepen `analyze_preservation(...)` with artifact-role heuristics and strategy/legal flags, and render the richer decision set in the clone blueprint preservation matrix. Keep the system deterministic and explicit that the legal flags are workflow guidance, not legal advice.

**Tech Stack:** Python 3.12, pytest, existing `deep_analysis` package

---

## File Structure

- Create: `docs/specs/2026-03-12-preservation-analysis-design.md`
- Create: `docs/plans/2026-03-12-preservation-analysis.md`
- Modify: `src/deep_analysis/models.py`
- Modify: `src/deep_analysis/analysis/preservation.py`
- Modify: `src/deep_analysis/synthesis/blueprint.py`
- Modify: `tests/test_pipeline.py`
- Modify: `MEMORY.md`

## Chunk 1: Add Failing Tests For Richer Preservation Decisions

### Task 1: Write failing tests for nuanced decisions and matrix output

**Files:**
- Modify: `tests/test_pipeline.py`

- [ ] **Step 1: Add assertions that strategy-bearing docs use `rewrite-with-differentiation`**
- [ ] **Step 2: Add assertions that skills/prompts use `rewrite-equivalent`**
- [ ] **Step 3: Add assertions that code/scripts use `preserve-core-behavior`**
- [ ] **Step 4: Add assertions that preservation decisions expose role, legal-review, confidence, and strategy note fields**
- [ ] **Step 5: Add assertions that the preservation matrix renders the richer columns**
- [ ] **Step 6: Run `source .venv/bin/activate && pytest tests/test_pipeline.py -q`**
- [ ] **Step 7: Verify the new tests fail because the richer preservation model is not implemented yet**

## Chunk 2: Implement The Richer Preservation Model

### Task 2: Extend preservation decisions and heuristics

**Files:**
- Modify: `src/deep_analysis/models.py`
- Modify: `src/deep_analysis/analysis/preservation.py`

- [ ] **Step 1: Extend `PreservationDecision` with artifact role, strategy note, legal review, and confidence**
- [ ] **Step 2: Add deterministic role classification for meaningful artifacts**
- [ ] **Step 3: Add richer decision heuristics and rationale generation**
- [ ] **Step 4: Add explicit legal-review flags and confidence labels**
- [ ] **Step 5: Run `source .venv/bin/activate && pytest tests/test_pipeline.py -q`**
- [ ] **Step 6: Verify the targeted preservation tests pass**

### Task 3: Render the richer preservation matrix

**Files:**
- Modify: `src/deep_analysis/synthesis/blueprint.py`

- [ ] **Step 1: Expand the matrix columns to include role, legal review, confidence, and strategy note**
- [ ] **Step 2: Keep the matrix readable and stable for existing output paths**
- [ ] **Step 3: Re-run `source .venv/bin/activate && pytest tests/test_pipeline.py -q`**

## Chunk 3: Full Verification And Memory Refresh

### Task 4: Verify on the full suite and real repo

**Files:**
- Modify: `MEMORY.md`

- [ ] **Step 1: Run `source .venv/bin/activate && pytest -q`**
- [ ] **Step 2: Run `source .venv/bin/activate && python -m deep_analysis.cli analyze '/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers' /tmp/superpowers-preservation-20260312 --export-skill-pack`**
- [ ] **Step 3: Inspect the generated preservation matrix for richer decisions**
- [ ] **Step 4: Update `MEMORY.md` with the new slice and verification evidence**
- [ ] **Step 5: Commit the completed slice**
- [ ] **Step 6: Push the branch**
