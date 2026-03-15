# Cross-Artifact Architecture Links Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strengthen architecture reconstruction so docs, prompts, skills, and tests create useful graph edges and dossier pages can show what drives, what is driven, and what validates each artifact.

**Architecture:** Extend deterministic cartography rather than introducing heavy parser infrastructure. Add first-class test classification, extract explicit local path and command references from workflow-bearing markdown and tests, synthesize richer relationship summaries, and surface the new graph context in dossier pages.

**Tech Stack:** Python 3.12, pytest, NetworkX, existing deep-analysis synthesis pipeline

---

## Chunk 1: Red Tests And Fixture Coverage

**Files:**
- Modify: `tests/test_classifier.py`
- Modify: `tests/test_pipeline.py`
- Modify: `tests/fixtures/sample_agent_repo/README.md`
- Modify: `tests/fixtures/sample_agent_repo/prompts/reviewer-prompt.md`
- Modify: `tests/fixtures/sample_agent_repo/skills/example/SKILL.md`
- Create: `tests/fixtures/sample_agent_repo/tests/test_example.py`

- [ ] **Step 1: Add a classifier test for first-class test artifacts**

- [ ] **Step 2: Enrich the sample fixture docs/prompts/skills with explicit local path and command references**

- [ ] **Step 3: Add a sample test artifact that imports local code and references runtime behavior**

- [ ] **Step 4: Add failing pipeline tests for**
  - doc/prompt/skill graph edges
  - test-to-implementation graph edges
  - architecture summaries that describe validation relationships
  - dossier pages that expose connected artifacts

- [ ] **Step 5: Run targeted tests to capture the red state**

Run: `source .venv/bin/activate && pytest tests/test_classifier.py tests/test_pipeline.py -q`
Expected: FAIL on the new architecture-link assertions

## Chunk 2: Cartography And Synthesis

**Files:**
- Modify: `src/deep_analysis/classifier.py`
- Modify: `src/deep_analysis/cartography.py`
- Modify: `src/deep_analysis/analysis/architecture.py`
- Modify: `src/deep_analysis/analysis/logic.py`
- Modify: `src/deep_analysis/synthesis/dossier.py`

- [ ] **Step 1: Classify test artifacts as meaningful**

- [ ] **Step 2: Add deterministic local-reference extraction for**
  - Python local imports
  - markdown path references
  - markdown command references
  - test-to-target references

- [ ] **Step 3: Update architecture relationship summaries so tests read as validators and docs/prompts read as workflow drivers**

- [ ] **Step 4: Update logic analysis to treat test code as code-bearing artifacts rather than fallback docs**

- [ ] **Step 5: Surface connected artifacts in file dossier pages**

- [ ] **Step 6: Run targeted tests until green**

Run: `source .venv/bin/activate && pytest tests/test_classifier.py tests/test_pipeline.py -q`
Expected: PASS

## Chunk 3: Full Verification And Handoff

**Files:**
- Modify: `MEMORY.md`

- [ ] **Step 1: Run the full test suite**

Run: `source .venv/bin/activate && pytest -q`
Expected: PASS

- [ ] **Step 2: Run a fresh smoke analysis against `superpowers`**

Run: `source .venv/bin/activate && python -m deep_analysis.cli analyze '/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers' /tmp/superpowers-cross-links-20260312 --export-skill-pack`
Expected: analysis-project, clone-blueprint, and skill-pack all generated successfully

- [ ] **Step 3: Inspect representative architecture and dossier pages for cross-artifact links**

- [ ] **Step 4: Update `MEMORY.md` with the new capability and next recommended stage**

- [ ] **Step 5: Commit and push**
