# Mythic Couture Scripted Boards Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the production board and top five scripted shooting boards so the execution layer matches the official mythic-couture creative reset instead of the earlier rebel-reveal framework.

**Architecture:** Keep the same strategy-pack files, but change their emotional and narrative center. The production board should become an episode schedule for the first two-week season, and the scripted board file should carry the master thesis, viewer psychology, and richer character world directly inside the execution instructions.

**Tech Stack:** Markdown strategy documents, shell validation with `rg`, git

---

## Planned File Structure

**Create:**
- `docs/specs/2026-03-12-mythic-couture-scripted-boards-design.md`
- `docs/plans/2026-03-12-mythic-couture-scripted-boards.md`

**Modify:**
- `marketing-superpowers/strategy/account/production-board-weeks-1-2.md`
- `marketing-superpowers/strategy/account/scripted-shooting-boards-top-5.md`
- `marketing-superpowers/tests/run-strategy-pack-checks.sh`

## Chunk 1: Validation First

**Files:**
- Modify: `marketing-superpowers/tests/run-strategy-pack-checks.sh`

- [ ] **Step 1: Require the new episode language**

Assert:
- `The Audition`
- `The Reject Pile`
- `she made couture feel alive again`
- `Protective Tenderness`

- [ ] **Step 2: Run the strategy checks and confirm red**

Run: `bash marketing-superpowers/tests/run-strategy-pack-checks.sh`
Expected: FAIL before the execution docs are rewritten

## Chunk 2: Rewrite The Production Board

**Files:**
- Modify: `marketing-superpowers/strategy/account/production-board-weeks-1-2.md`

- [ ] **Step 1: Replace the old first-pass status framing**

Turn the file into an active production board for the opening season.

- [ ] **Step 2: Schedule the first two weeks around episode logic**

Map the cycle to:
- Day 1
- Day 2
- Day 3
- Day 4
- Day 5
- Day 6
- Day 7

## Chunk 3: Rewrite The Top Five Scripted Boards

**Files:**
- Modify: `marketing-superpowers/strategy/account/scripted-shooting-boards-top-5.md`

- [ ] **Step 1: Replace the older top five concepts**

Use:
- Day 1: The Audition
- Day 2: She Noticed Something You Did Not
- Day 3: The Reject Pile
- Day 5: The Wrong Soundtrack
- Day 7: She Teaches You Something (And Gets It Slightly Wrong)

- [ ] **Step 2: Keep the production headings**

Each board must still include:
- Opening Line
- First 3 Seconds
- Shot List
- Edit Rhythm
- Platform Variation

- [ ] **Step 3: Add richer psychological framing**

Each board should include:
- Mythic Claim
- Psychology
- deeper character or world-building logic

## Chunk 4: Verify And Commit

**Files:**
- All files above

- [ ] **Step 1: Run verification**

Run:
- `bash marketing-superpowers/tests/run-strategy-pack-checks.sh`
- `bash marketing-superpowers/tests/run-skill-checks.sh`
- `source .venv/bin/activate && pytest -q`

- [ ] **Step 2: Commit**

```bash
git add docs/specs/2026-03-12-mythic-couture-scripted-boards-design.md \
  docs/plans/2026-03-12-mythic-couture-scripted-boards.md \
  marketing-superpowers/strategy/account/production-board-weeks-1-2.md \
  marketing-superpowers/strategy/account/scripted-shooting-boards-top-5.md \
  marketing-superpowers/tests/run-strategy-pack-checks.sh
git commit -m "feat: rewrite creator shooting boards for mythic couture"
```
