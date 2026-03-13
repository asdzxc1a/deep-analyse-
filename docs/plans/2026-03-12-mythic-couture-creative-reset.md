# Mythic Couture Creative Reset Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the stronger mythic-couture thesis official in the fashion creator strategy pack so the checked creative system reflects the new cold-audience direction instead of only the earlier rebel/reveal framing.

**Architecture:** Keep the existing pack layered. Promote the deeper concept-board document into the official checked artifacts, refresh the live strategy spec around the master thesis, mark the older execution boards as first-pass material, and extend validation so the pack enforces the new direction.

**Tech Stack:** Markdown strategy documents, shell validation with `rg`, git

---

## Planned File Structure

**Create:**
- `docs/specs/2026-03-12-mythic-couture-creative-reset-design.md`
- `docs/plans/2026-03-12-mythic-couture-creative-reset.md`

**Modify:**
- `marketing-superpowers/strategy/live-fashion-creator-strategy-spec.md`
- `marketing-superpowers/tests/run-strategy-pack-checks.sh`
- `marketing-superpowers/strategy/account/cold-audience-concept-board-v2-deep-analysis.md`
- `marketing-superpowers/strategy/account/production-board-weeks-1-2.md`
- `marketing-superpowers/strategy/account/scripted-shooting-boards-top-5.md`

## Chunk 1: Promote The New Thesis

**Files:**
- Modify: `marketing-superpowers/strategy/live-fashion-creator-strategy-spec.md`

- [ ] **Step 1: Add the master thesis and creative reset framing**

Document:
- she made couture feel alive again
- outer mythic hook
- inner human layer

- [ ] **Step 2: Explain the new emotional mechanics**

Include:
- outward resistance
- inward fascination with beauty
- discovery arc
- mother/stylist trust

## Chunk 2: Make The New Concept Board Official

**Files:**
- Modify: `marketing-superpowers/strategy/account/cold-audience-concept-board-v2-deep-analysis.md`
- Modify: `marketing-superpowers/tests/run-strategy-pack-checks.sh`

- [ ] **Step 1: Ensure the v2 concept board reads as the active upgrade layer**

It should clearly state:
- what v1 missed
- what the new thesis is
- why the new psychology is stronger

- [ ] **Step 2: Make validation require the v2 board**

Assert phrases like:
- `she made couture feel alive again`
- `The Five Viewer Reactions That Build Empires`
- `The Character Must Have at Least Four Modes`

- [ ] **Step 3: Run the strategy checks and confirm green**

Run: `bash marketing-superpowers/tests/run-strategy-pack-checks.sh`

## Chunk 3: Label The Old Execution Layer Honestly

**Files:**
- Modify: `marketing-superpowers/strategy/account/production-board-weeks-1-2.md`
- Modify: `marketing-superpowers/strategy/account/scripted-shooting-boards-top-5.md`

- [ ] **Step 1: Add status notes to both files**

Make it explicit that these are:
- first-pass execution assets
- useful references
- not yet rebuilt to the new mythic-couture standard

## Chunk 4: Verify And Commit

**Files:**
- All files above

- [ ] **Step 1: Run validation**

Run:
- `bash marketing-superpowers/tests/run-strategy-pack-checks.sh`
- `bash marketing-superpowers/tests/run-skill-checks.sh`

- [ ] **Step 2: Run repo tests**

Run:
- `source .venv/bin/activate && pytest -q`

- [ ] **Step 3: Commit**

```bash
git add docs/specs/2026-03-12-mythic-couture-creative-reset-design.md \
  docs/plans/2026-03-12-mythic-couture-creative-reset.md \
  marketing-superpowers/strategy/live-fashion-creator-strategy-spec.md \
  marketing-superpowers/tests/run-strategy-pack-checks.sh \
  marketing-superpowers/strategy/account/cold-audience-concept-board-v2-deep-analysis.md \
  marketing-superpowers/strategy/account/production-board-weeks-1-2.md \
  marketing-superpowers/strategy/account/scripted-shooting-boards-top-5.md
git commit -m "docs: reset creator strategy around mythic couture"
```
