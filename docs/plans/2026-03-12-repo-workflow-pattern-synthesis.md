# Repo Workflow Pattern Synthesis Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Synthesize repo-level workflow patterns from repeated workflow semantics and expose them in the dossier and blueprint so rebuild guidance preserves operating style as well as file structure.

**Architecture:** Keep per-file workflow extraction intact and add a deterministic repo-level synthesis layer that aggregates repeated workflow semantics into named patterns with evidence and reconstruction notes. Feed those patterns into the workflow section, reconstruction plan, and blueprint docs without destabilizing the existing pipeline.

**Tech Stack:** Python 3.12, pytest, existing deep-analysis workflow analysis and synthesis pipeline

---

## Chunk 1: Red Tests For Repo-Level Pattern Outputs

**Files:**
- Modify: `tests/test_pipeline.py`
- Modify: `tests/fixtures/sample_agent_repo/README.md`
- Modify: `tests/fixtures/sample_agent_repo/prompts/reviewer-prompt.md`
- Modify: `tests/fixtures/sample_agent_repo/skills/example/SKILL.md`

- [ ] **Step 1: Tighten the fixture wording only if needed so repeated workflow semantics are explicit across multiple artifacts**

- [ ] **Step 2: Add failing tests for repo-level workflow pattern synthesis**

- [ ] **Step 3: Add failing dossier and blueprint assertions for**
  - a workflow patterns page
  - repo-level pattern evidence
  - reconstruction guidance that references the synthesized patterns

- [ ] **Step 4: Run targeted tests to capture the red state**

Run: `source .venv/bin/activate && pytest tests/test_pipeline.py -q`
Expected: FAIL on the new workflow-pattern assertions

## Chunk 2: Implement Pattern Synthesis

**Files:**
- Modify: `src/deep_analysis/models.py`
- Modify: `src/deep_analysis/analysis/workflows.py`
- Modify: `src/deep_analysis/pipeline.py`
- Modify: `src/deep_analysis/synthesis/dossier.py`
- Modify: `src/deep_analysis/synthesis/blueprint.py`

- [ ] **Step 1: Add a small model for synthesized repo workflow patterns**

- [ ] **Step 2: Implement deterministic aggregation of repeated workflow semantics**

- [ ] **Step 3: Pass synthesized patterns through the pipeline**

- [ ] **Step 4: Write a repo-level workflow patterns page in the dossier**

- [ ] **Step 5: Add workflow-pattern guidance to the clone blueprint and reconstruction plan**

- [ ] **Step 6: Run targeted tests until green**

Run: `source .venv/bin/activate && pytest tests/test_pipeline.py -q`
Expected: PASS

## Chunk 3: Full Verification And Handoff

**Files:**
- Modify: `MEMORY.md`

- [ ] **Step 1: Run the full test suite**

Run: `source .venv/bin/activate && pytest -q`
Expected: PASS

- [ ] **Step 2: Run a fresh smoke analysis against `superpowers`**

Run: `source .venv/bin/activate && python -m deep_analysis.cli analyze '/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers' /tmp/superpowers-workflow-patterns-20260312 --export-skill-pack`
Expected: analysis-project, clone-blueprint, and skill-pack all generated successfully

- [ ] **Step 3: Inspect the generated workflow-pattern outputs**

- [ ] **Step 4: Update `MEMORY.md` with the new capability and next recommended stage**

- [ ] **Step 5: Commit and push**
