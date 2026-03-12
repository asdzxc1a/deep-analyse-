# Test And Fixture Preservation Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Distinguish production artifacts, tests, and fixtures in preservation analysis so the blueprint preserves verification contracts without over-preserving harness-specific implementation.

**Architecture:** Keep the preservation pass deterministic and path-based. Add test-aware roles and decision categories, detect fixture artifacts from stable path/name signals, and propagate the richer guidance into the preservation matrix and reconstruction plan.

**Tech Stack:** Python 3.12, pytest, existing preservation analysis and blueprint synthesis pipeline

---

## Chunk 1: Red Tests For Test And Fixture Preservation

**Files:**
- Modify: `tests/test_pipeline.py`
- Create: `tests/fixtures/sample_agent_repo/tests/fixtures/sample-output.md`

- [ ] **Step 1: Add a sample fixture artifact inside the sample repo**

- [ ] **Step 2: Add failing preservation assertions for**
  - test artifacts using `preserve-verification-contract`
  - fixture artifacts using `adapt-test-fixture`
  - role and rationale text that explain contract-vs-harness boundaries

- [ ] **Step 3: Add failing blueprint assertions for preservation output and reconstruction-plan wording**

- [ ] **Step 4: Run targeted tests to capture the red state**

Run: `source .venv/bin/activate && pytest tests/test_pipeline.py -q`
Expected: FAIL on the new preservation assertions

## Chunk 2: Implement Test-Aware Preservation Guidance

**Files:**
- Modify: `src/deep_analysis/analysis/preservation.py`
- Modify: `src/deep_analysis/synthesis/blueprint.py`

- [ ] **Step 1: Add test-aware role classification and fixture detection**

- [ ] **Step 2: Introduce new preservation decision categories for tests and fixtures**

- [ ] **Step 3: Improve strategy notes, legal-review flags, confidence, and rationales to reflect contract-vs-harness guidance**

- [ ] **Step 4: Update blueprint output so reconstruction guidance references verification contracts and fixture adaptation**

- [ ] **Step 5: Run targeted tests until green**

Run: `source .venv/bin/activate && pytest tests/test_pipeline.py -q`
Expected: PASS

## Chunk 3: Full Verification And Handoff

**Files:**
- Modify: `MEMORY.md`

- [ ] **Step 1: Run the full test suite**

Run: `source .venv/bin/activate && pytest -q`
Expected: PASS

- [ ] **Step 2: Run a fresh smoke analysis against `superpowers`**

Run: `source .venv/bin/activate && python -m deep_analysis.cli analyze '/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers' /tmp/superpowers-test-preservation-20260312 --export-skill-pack`
Expected: analysis-project, clone-blueprint, and skill-pack all generated successfully

- [ ] **Step 3: Inspect representative preservation outputs**

- [ ] **Step 4: Update `MEMORY.md` with the new capability and next recommended stage**

- [ ] **Step 5: Commit and push**
