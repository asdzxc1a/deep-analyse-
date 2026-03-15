# Prompt Template Step Extraction Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve prompt dossier quality by extracting steps and workflow guidance from natural-language prompt templates stored inside fenced blocks.

**Architecture:** Keep the existing workflow extractor stable for skills/docs, but add a prompt-aware path that can read instructional fenced blocks while still ignoring code and diagram noise. Drive the change with a dedicated prompt fixture that mirrors real prompt-template structure.

**Tech Stack:** Python 3.12, pytest, existing workflow extraction and dossier pipeline

---

## Chunk 1: Red Tests For Prompt Template Extraction

**Files:**
- Modify: `tests/test_pipeline.py`
- Create: `tests/fixtures/sample_agent_repo/prompts/implementer-prompt.md`

- [ ] **Step 1: Add a prompt-template fixture whose real instructions live inside a fenced block**

- [ ] **Step 2: Add failing workflow-analysis assertions proving steps are extracted from the prompt template**

- [ ] **Step 3: Add failing dossier assertions for the generated prompt page**

- [ ] **Step 4: Run targeted tests to capture the red state**

Run: `source .venv/bin/activate && pytest tests/test_pipeline.py -q`
Expected: FAIL on the new prompt-step assertions

## Chunk 2: Implement Prompt-Aware Extraction

**Files:**
- Modify: `src/deep_analysis/analysis/workflows.py`

- [ ] **Step 1: Add prompt-aware analysis-line extraction that can inspect fenced blocks**

- [ ] **Step 2: Include only natural-language prompt-template lines and continue filtering technical noise**

- [ ] **Step 3: Reuse the existing step/constraint/role extraction logic on the richer prompt lines**

- [ ] **Step 4: Run targeted tests until green**

Run: `source .venv/bin/activate && pytest tests/test_pipeline.py -q`
Expected: PASS

## Chunk 3: Full Verification And Handoff

**Files:**
- Modify: `MEMORY.md`

- [ ] **Step 1: Run the full test suite**

Run: `source .venv/bin/activate && pytest -q`
Expected: PASS

- [ ] **Step 2: Run a fresh smoke analysis against `superpowers`**

Run: `source .venv/bin/activate && python -m deep_analysis.cli analyze '/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers' /tmp/superpowers-prompt-templates-20260312 --export-skill-pack`
Expected: analysis-project, clone-blueprint, and skill-pack all generated successfully

- [ ] **Step 3: Inspect representative prompt pages**

- [ ] **Step 4: Update `MEMORY.md` with the new capability and next recommended stage**

- [ ] **Step 5: Commit and push**
