# Code And Script Logic Analysis Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deepen code and script artifact analysis so dossier pages explain symbols, dependencies, entrypoints, side effects, and operational risks instead of only first-line heuristics.

**Architecture:** Keep the current analysis pipeline and dossier writer shape, but refactor `logic.py` into file-type-specific extractors for code and shell scripts. Feed richer `ArtifactFinding` data into the existing dossier output rather than redesigning the output format again.

**Tech Stack:** Python 3.12, pytest, existing `deep_analysis` package

---

## File Structure

- Create: `docs/specs/2026-03-12-code-script-logic-analysis-design.md`
- Create: `docs/plans/2026-03-12-code-script-logic-analysis.md`
- Create: `tests/fixtures/sample_agent_repo/scripts/start-example.sh`
- Create: `tests/fixtures/sample_agent_repo/src/example.py`
- Create: `tests/fixtures/sample_agent_repo/src/server.js`
- Modify: `tests/test_pipeline.py`
- Modify: `src/deep_analysis/analysis/logic.py`
- Modify: `MEMORY.md`

## Chunk 1: Add Failing Tests And Fixtures

### Task 1: Add realistic code and script fixtures

**Files:**
- Create: `tests/fixtures/sample_agent_repo/scripts/start-example.sh`
- Create: `tests/fixtures/sample_agent_repo/src/example.py`
- Create: `tests/fixtures/sample_agent_repo/src/server.js`

- [ ] **Step 1: Create a Python fixture with imports, definitions, and a main guard**
- [ ] **Step 2: Create a JS fixture with requires, defined functions, and a listen/startup call**
- [ ] **Step 3: Create a shell fixture with commands, env variables, and process control**

### Task 2: Write failing tests for richer logic extraction

**Files:**
- Modify: `tests/test_pipeline.py`

- [ ] **Step 1: Write a test asserting Python artifact findings include imports, defined symbols, and entrypoint cues**
- [ ] **Step 2: Write a test asserting JS artifact findings include imports, defined symbols, and startup cues**
- [ ] **Step 3: Write a test asserting shell artifact findings include commands, environment assumptions, and side effects**
- [ ] **Step 4: Run `source .venv/bin/activate && pytest tests/test_pipeline.py -q`**
- [ ] **Step 5: Verify the new tests fail for the expected missing-analysis reasons**

## Chunk 2: Implement Code And Script Analyzers

### Task 3: Refactor logic analysis into per-type helpers

**Files:**
- Modify: `src/deep_analysis/analysis/logic.py`

- [ ] **Step 1: Add helper routing for code, script, and fallback analysis**
- [ ] **Step 2: Implement Python and JS/TS extraction for imports, definitions, and entrypoints**
- [ ] **Step 3: Implement shell extraction for commands, env vars, file effects, and process behavior**
- [ ] **Step 4: Upgrade summaries, dependencies, failure modes, and reconstruction notes to use the extracted facts**
- [ ] **Step 5: Run `source .venv/bin/activate && pytest tests/test_pipeline.py -q`**
- [ ] **Step 6: Verify all targeted tests pass**

## Chunk 3: Full Verification And Documentation Refresh

### Task 4: Run full verification and smoke analysis

**Files:**
- Modify: `MEMORY.md`

- [ ] **Step 1: Run `source .venv/bin/activate && pytest -q`**
- [ ] **Step 2: Run `source .venv/bin/activate && python -m deep_analysis.cli analyze '/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers' /tmp/superpowers-code-logic-20260312 --export-skill-pack`**
- [ ] **Step 3: Inspect representative generated pages for code and script artifacts**
- [ ] **Step 4: Update `MEMORY.md` with the new slice, verification evidence, and output path**
- [ ] **Step 5: Commit the completed slice**
- [ ] **Step 6: Push the branch**
