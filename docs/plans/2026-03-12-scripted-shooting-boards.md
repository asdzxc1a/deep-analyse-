# Scripted Shooting Boards Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add production-grade scripted shooting boards to the fashion creator strategy pack so the first 2-week content cycle can be shot from exact hooks, shot orders, edit rhythms, captions, and platform variations instead of only from high-level concepts.

**Architecture:** Keep the strategy pack layered. The concept board remains the idea bank, the production board becomes the scheduling overview, and a new scripted-board file becomes the operational shooting document. Validation should fail until the scripted-board artifact exists and contains the required execution sections.

**Tech Stack:** Markdown strategy documents, shell-based validation with `rg`, git

---

## Planned File Structure

**Modify:**
- `marketing-superpowers/tests/run-strategy-pack-checks.sh`
  - Require the scripted execution assets and assert key execution phrases.
- `marketing-superpowers/strategy/account/production-board-weeks-1-2.md`
  - Replace the loose post list with a board-mapped production schedule.

**Keep and commit:**
- `marketing-superpowers/strategy/account/cold-audience-concept-board-v1.md`
  - Retain as the approved concept bank and cold-audience screen.

**Create:**
- `marketing-superpowers/strategy/account/scripted-shooting-boards-top-5.md`
  - Five detailed production boards with opening lines, first 3 seconds, shot lists, edit rhythms, captions, cover text, and platform variations.

## Chunk 1: Validation First

**Files:**
- Modify: `marketing-superpowers/tests/run-strategy-pack-checks.sh`

- [ ] **Step 1: Add the new required strategy files**

Require:
- `production-board-weeks-1-2.md`
- `cold-audience-concept-board-v1.md`
- `scripted-shooting-boards-top-5.md`

- [ ] **Step 2: Add failing assertions for the scripted board format**

Assert that the scripted board file contains:
- `Opening Line`
- `First 3 Seconds`
- `Shot List`
- `Edit Rhythm`
- `Platform Variation`

- [ ] **Step 3: Run the strategy checks and confirm red**

Run: `bash marketing-superpowers/tests/run-strategy-pack-checks.sh`
Expected: FAIL because the scripted board file does not exist yet

## Chunk 2: Script The Top Five Concepts

**Files:**
- Create: `marketing-superpowers/strategy/account/scripted-shooting-boards-top-5.md`

- [ ] **Step 1: Choose the five concepts that best cover the first cycle**

Use a mix of:
- refusal tension
- impossible transformation
- anti-reaction reveal
- luxury-location dominance
- editorial ending after chaos

- [ ] **Step 2: Write each scripted board with production-ready detail**

Each board must include:
- objective
- opening line
- first 3 seconds
- shot list
- edit rhythm
- caption
- cover text
- platform variation
- why it should work

- [ ] **Step 3: Keep captions polished and fashion-aware**

Use short, elevated captions that support the luxury image without flattening personality.

## Chunk 3: Tighten The 2-Week Production Layer

**Files:**
- Modify: `marketing-superpowers/strategy/account/production-board-weeks-1-2.md`

- [ ] **Step 1: Convert the old post list into a mapped schedule**

For each planned post include:
- board reference
- platform
- shoot block
- objective
- batch notes

- [ ] **Step 2: Make the schedule usable on set**

Show which posts can be batched from the same location or wardrobe setup.

## Chunk 4: Verify And Commit

**Files:**
- Modify: `marketing-superpowers/tests/run-strategy-pack-checks.sh`
- Modify: `marketing-superpowers/strategy/account/production-board-weeks-1-2.md`
- Create: `marketing-superpowers/strategy/account/scripted-shooting-boards-top-5.md`
- Add: `marketing-superpowers/strategy/account/cold-audience-concept-board-v1.md`

- [ ] **Step 1: Run strategy validation**

Run: `bash marketing-superpowers/tests/run-strategy-pack-checks.sh`
Expected: `Strategy pack checks passed`

- [ ] **Step 2: Review the scripted board file manually**

Confirm the five boards are:
- non-obvious
- cold-audience oriented
- production-ready

- [ ] **Step 3: Commit**

```bash
git add docs/specs/2026-03-12-scripted-shooting-boards-design.md \
  docs/plans/2026-03-12-scripted-shooting-boards.md \
  marketing-superpowers/tests/run-strategy-pack-checks.sh \
  marketing-superpowers/strategy/account/cold-audience-concept-board-v1.md \
  marketing-superpowers/strategy/account/production-board-weeks-1-2.md \
  marketing-superpowers/strategy/account/scripted-shooting-boards-top-5.md
git commit -m "feat: add scripted shooting boards"
```
