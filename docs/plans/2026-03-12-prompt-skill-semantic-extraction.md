# Prompt And Skill Semantic Extraction Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extract the real operating semantics from prompts and skills so workflow dossier pages capture constraints, approval gates, loops, escalation rules, and reusable patterns.

**Architecture:** Extend `WorkflowFinding` with semantic fields, enrich `analyze_workflows(...)` with deterministic semantic passes for skills/prompts/docs, and render those new sections in the existing workflow dossier pages. Keep the extraction rule-based and explicit.

**Tech Stack:** Python 3.12, pytest, existing `deep_analysis` package

---

## File Structure

- Create: `docs/specs/2026-03-12-prompt-skill-semantic-extraction-design.md`
- Create: `docs/plans/2026-03-12-prompt-skill-semantic-extraction.md`
- Create: `tests/fixtures/sample_agent_repo/prompts/reviewer-prompt.md`
- Modify: `tests/fixtures/sample_agent_repo/skills/example/SKILL.md`
- Modify: `src/deep_analysis/models.py`
- Modify: `src/deep_analysis/analysis/workflows.py`
- Modify: `src/deep_analysis/synthesis/dossier.py`
- Modify: `tests/test_pipeline.py`
- Modify: `MEMORY.md`

## Chunk 1: Add Failing Tests And Fixtures

### Task 1: Create richer semantic fixtures

**Files:**
- Create: `tests/fixtures/sample_agent_repo/prompts/reviewer-prompt.md`
- Modify: `tests/fixtures/sample_agent_repo/skills/example/SKILL.md`

- [ ] **Step 1: Add a prompt fixture with constraints, approval gates, loops, and escalation language**
- [ ] **Step 2: Enrich the sample skill fixture with at least one hard constraint, approval gate, and escalation rule**

### Task 2: Write failing tests for semantic workflow extraction

**Files:**
- Modify: `tests/test_pipeline.py`

- [ ] **Step 1: Add a test asserting skill findings expose hard constraints, approval gates, review loops, escalation paths, and reusable patterns**
- [ ] **Step 2: Add a test asserting prompt findings expose the same semantic fields**
- [ ] **Step 3: Add a dossier rendering assertion for the new workflow sections**
- [ ] **Step 4: Run `source .venv/bin/activate && pytest tests/test_pipeline.py -q`**
- [ ] **Step 5: Verify the new tests fail because semantic extraction is not implemented yet**

## Chunk 2: Implement Semantic Extraction And Rendering

### Task 3: Extend workflow findings and extract semantic signals

**Files:**
- Modify: `src/deep_analysis/models.py`
- Modify: `src/deep_analysis/analysis/workflows.py`

- [ ] **Step 1: Extend `WorkflowFinding` with semantic fields**
- [ ] **Step 2: Add helper extraction for hard constraints**
- [ ] **Step 3: Add helper extraction for approval gates**
- [ ] **Step 4: Add helper extraction for review loops**
- [ ] **Step 5: Add helper extraction for escalation paths**
- [ ] **Step 6: Add deterministic reusable pattern labels based on extracted semantics**
- [ ] **Step 7: Run `source .venv/bin/activate && pytest tests/test_pipeline.py -q`**
- [ ] **Step 8: Verify the targeted tests pass**

### Task 4: Render semantic sections in workflow pages

**Files:**
- Modify: `src/deep_analysis/synthesis/dossier.py`

- [ ] **Step 1: Add workflow-page sections for constraints, approval gates, loops, escalation paths, and reusable patterns**
- [ ] **Step 2: Keep rendering stable when a section has no content**
- [ ] **Step 3: Re-run `source .venv/bin/activate && pytest tests/test_pipeline.py -q`**

## Chunk 3: Full Verification And Memory Refresh

### Task 5: Verify on the full suite and real repo

**Files:**
- Modify: `MEMORY.md`

- [ ] **Step 1: Run `source .venv/bin/activate && pytest -q`**
- [ ] **Step 2: Run `source .venv/bin/activate && python -m deep_analysis.cli analyze '/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers' /tmp/superpowers-semantics-20260312 --export-skill-pack`**
- [ ] **Step 3: Inspect representative workflow pages for the new semantic sections**
- [ ] **Step 4: Update `MEMORY.md` with the new slice and verification evidence**
- [ ] **Step 5: Commit the completed slice**
- [ ] **Step 6: Push the branch**
