# Fashion Creator Growth System Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first `marketing-superpowers` vertical system for an eight-year-old fashion creator whose growth engine is the contrast between wild tomboy energy and high-fashion transformation, producing repeatable strategy, review, and posting workflows for Instagram, TikTok, and YouTube.

**Architecture:** Build this vertical as the first concrete specialization of the core marketing operating system. The implementation should create a reusable skill-pack structure with doctrine, core vertical skills, platform-aware prompts, examples, and deterministic prompt/fixture tests so the system can be used immediately for creator growth work and later extended to other business verticals.

**Tech Stack:** Markdown skill files, Markdown prompt files, repository documentation, shell-based fixture tests, Python 3.12 or shell validation helpers only if needed

---

## Planned File Structure

**Target repo root:** `marketing-superpowers/`

**Create:**
- `README.md`
  - Product overview and how the creator-growth system works.
- `doctrine/fashion-creator-doctrine.md`
  - Core philosophy, approval rules, and positioning for the fashion creator vertical.
- `skills/creator-diagnosis/SKILL.md`
  - Diagnose content gaps, hook problems, platform confusion, and growth bottlenecks.
- `skills/creator-content-planning/SKILL.md`
  - Turn diagnosis into a weekly content engine with recurring series and platform-specific execution.
- `skills/contrast-message-architecture/SKILL.md`
  - Define creator identity, content pillars, and contrast logic.
- `skills/viral-content-review/SKILL.md`
  - Review content for hook strength, contrast clarity, and shareability.
- `skills/posting-readiness-check/SKILL.md`
  - Verify publish readiness per platform.
- `skills/content-postmortem/SKILL.md`
  - Analyze outcomes and recommend the next cycle.
- `prompts/instagram-reviewer-prompt.md`
  - Review logic specific to Instagram short-form identity building.
- `prompts/tiktok-reviewer-prompt.md`
  - Review logic specific to TikTok virality and hook performance.
- `prompts/youtube-reviewer-prompt.md`
  - Review logic specific to YouTube story depth and attachment.
- `examples/weekly-plan-example.md`
  - Example weekly plan for the creator.
- `examples/content-pillar-example.md`
  - Example content architecture and series map.
- `examples/postmortem-example.md`
  - Example performance review and next-step interpretation.
- `tests/prompts/creator-diagnosis.txt`
  - Prompt fixture that should trigger diagnosis behavior.
- `tests/prompts/creator-content-planning.txt`
  - Prompt fixture for weekly planning behavior.
- `tests/prompts/viral-content-review.txt`
  - Prompt fixture for review behavior.
- `tests/prompts/posting-readiness.txt`
  - Prompt fixture for readiness checks.
- `tests/test-skill-coverage.md`
  - Expected behavior checklist for skill coverage and role separation.
- `tests/run-skill-checks.sh`
  - Lightweight deterministic validation script for the skill-pack structure and required phrases.

**Modify later if needed during execution:**
- `skills/*/supporting-files/...`
  - Only if a skill becomes too large and needs focused references.

## Chunk 1: Repo Foundation And Doctrine

**Files:**
- Create: `marketing-superpowers/README.md`
- Create: `marketing-superpowers/doctrine/fashion-creator-doctrine.md`

- [ ] **Step 1: Write the failing doctrine validation checklist in the README draft**

Document that the repo must clearly state:
- the creator contrast
- the growth-first goal
- the platform roles
- the preserved approval and review discipline

- [ ] **Step 2: Write the doctrine file with the approved philosophy**

Include:
- research before messaging
- strategy before content batching
- review before posting
- verification before publish
- escalation when content conflicts with age, safety, or identity

- [ ] **Step 3: Add the product-level README**

Include:
- what this vertical is
- how it maps to the core marketing operating system
- what skills exist
- how Instagram, TikTok, and YouTube are treated differently

- [ ] **Step 4: Run a manual structure check**

Run: `test -f marketing-superpowers/README.md && test -f marketing-superpowers/doctrine/fashion-creator-doctrine.md`
Expected: exit code 0

- [ ] **Step 5: Commit**

```bash
git add marketing-superpowers/README.md marketing-superpowers/doctrine/fashion-creator-doctrine.md
git commit -m "feat: add creator vertical doctrine"
```

## Chunk 2: Build The First Three Core Skills

**Files:**
- Create: `marketing-superpowers/skills/creator-diagnosis/SKILL.md`
- Create: `marketing-superpowers/skills/creator-content-planning/SKILL.md`
- Create: `marketing-superpowers/skills/contrast-message-architecture/SKILL.md`
- Create: `marketing-superpowers/tests/prompts/creator-diagnosis.txt`
- Create: `marketing-superpowers/tests/prompts/creator-content-planning.txt`
- Create: `marketing-superpowers/examples/content-pillar-example.md`

- [ ] **Step 1: Write the failing prompt fixtures**

Make the fixtures require the system to:
- diagnose weak or random posting
- propose content pillars
- create a weekly plan
- preserve the contrast identity

- [ ] **Step 2: Write `creator-diagnosis`**

The skill must diagnose:
- what is spreading
- what is only pretty
- what the real creator advantage is
- what content patterns should stop

- [ ] **Step 3: Write `creator-content-planning`**

The skill must produce:
- weekly content buckets
- platform roles
- recurring series
- test matrix for hook and format experiments

- [ ] **Step 4: Write `contrast-message-architecture`**

The skill must define:
- creator identity
- content world
- emotional promise
- contrast logic
- boundaries for what fits or breaks the brand

- [ ] **Step 5: Add the content-pillar example**

Include:
- contrast transformations
- attitude moments
- character series
- behind-the-look stories

- [ ] **Step 6: Run the skill structure test**

Run: `bash marketing-superpowers/tests/run-skill-checks.sh`
Expected: FAIL at first until the checker and required files exist

## Chunk 3: Build Review, Readiness, And Postmortem Skills

**Files:**
- Create: `marketing-superpowers/skills/viral-content-review/SKILL.md`
- Create: `marketing-superpowers/skills/posting-readiness-check/SKILL.md`
- Create: `marketing-superpowers/skills/content-postmortem/SKILL.md`
- Create: `marketing-superpowers/tests/prompts/viral-content-review.txt`
- Create: `marketing-superpowers/tests/prompts/posting-readiness.txt`
- Create: `marketing-superpowers/examples/postmortem-example.md`

- [ ] **Step 1: Write the failing prompt fixtures for review and readiness**

The fixtures should force the skills to answer:
- is the hook strong enough
- is the contrast visible fast enough
- is the platform edit right
- what was learned from performance

- [ ] **Step 2: Write `viral-content-review`**

The skill must review:
- hook quality
- personality visibility
- contrast clarity
- shareability
- whether the post is strong enough to publish

- [ ] **Step 3: Write `posting-readiness-check`**

The skill must verify:
- platform fit
- pacing
- reveal strength
- cover
- caption
- CTA discipline

- [ ] **Step 4: Write `content-postmortem`**

The skill must analyze:
- what held attention
- what drove rewatches
- what drove shares
- what patterns should repeat or stop

- [ ] **Step 5: Add a postmortem example**

Use a plausible content-performance example with:
- one strong performer
- one weak performer
- one ambiguous test

- [ ] **Step 6: Run the skill structure test again**

Run: `bash marketing-superpowers/tests/run-skill-checks.sh`
Expected: still FAIL until the checker script is implemented

## Chunk 4: Add Platform-Specific Reviewer Prompts

**Files:**
- Create: `marketing-superpowers/prompts/instagram-reviewer-prompt.md`
- Create: `marketing-superpowers/prompts/tiktok-reviewer-prompt.md`
- Create: `marketing-superpowers/prompts/youtube-reviewer-prompt.md`
- Modify: `marketing-superpowers/skills/viral-content-review/SKILL.md`
- Modify: `marketing-superpowers/skills/posting-readiness-check/SKILL.md`

- [ ] **Step 1: Write the failing expectation list in `tests/test-skill-coverage.md`**

State that platform reviewers must differ on:
- TikTok hook intensity
- Instagram identity and visual world
- YouTube depth and story payoff

- [ ] **Step 2: Write the Instagram reviewer prompt**

Focus on:
- recognizability
- visual identity
- fast but slightly cleaner edit logic

- [ ] **Step 3: Write the TikTok reviewer prompt**

Focus on:
- immediate hook
- surprise
- energy
- rewatch/share impulse

- [ ] **Step 4: Write the YouTube reviewer prompt**

Focus on:
- narrative structure
- emotional payoff
- character depth
- retention over a longer arc

- [ ] **Step 5: Link the reviewer prompts from the relevant skills**

Make `viral-content-review` and `posting-readiness-check` explicitly route to the platform-specific prompts.

- [ ] **Step 6: Run the checker**

Run: `bash marketing-superpowers/tests/run-skill-checks.sh`
Expected: FAIL until the checker script is implemented with the new required files and phrase checks

## Chunk 5: Implement Deterministic Skill-Pack Checks

**Files:**
- Create: `marketing-superpowers/tests/run-skill-checks.sh`
- Create: `marketing-superpowers/tests/test-skill-coverage.md`

- [ ] **Step 1: Write the failing checker script**

The script should verify:
- all required skill files exist
- all required prompt files exist
- doctrine file exists
- required phrases appear in the right files

- [ ] **Step 2: Add required phrase checks**

Examples:
- `creator-diagnosis` must mention diagnosis of weak/random posting
- `creator-content-planning` must mention weekly content system
- `contrast-message-architecture` must mention the tomboy/high-fashion contrast
- `viral-content-review` must mention hook and shareability
- `posting-readiness-check` must mention publish readiness
- `content-postmortem` must mention rewatches, shares, and what to repeat or stop

- [ ] **Step 3: Run the checker and make it fail for any missing requirements**

Run: `bash marketing-superpowers/tests/run-skill-checks.sh`
Expected: FAIL until all required files and phrases exist

- [ ] **Step 4: Make the skill-pack pass the checker**

Run: `bash marketing-superpowers/tests/run-skill-checks.sh`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add marketing-superpowers/tests/run-skill-checks.sh marketing-superpowers/tests/test-skill-coverage.md marketing-superpowers/skills marketing-superpowers/prompts marketing-superpowers/examples
git commit -m "feat: add creator vertical skills and checks"
```

## Chunk 6: Final Review, Docs, And Verification

**Files:**
- Modify: `marketing-superpowers/README.md`
- Modify: `marketing-superpowers/doctrine/fashion-creator-doctrine.md`

- [ ] **Step 1: Review the README against the spec**

Confirm it explains:
- the creator position
- the platform roles
- the six-stage operating system
- the vertical skill set

- [ ] **Step 2: Review the doctrine file against the spec**

Confirm it includes:
- growth-first posture
- contrast identity
- approval gates
- escalation rules
- age/brand-safety boundaries

- [ ] **Step 3: Run the checker**

Run: `bash marketing-superpowers/tests/run-skill-checks.sh`
Expected: PASS

- [ ] **Step 4: Run a full file-structure verification**

Run: `find marketing-superpowers -maxdepth 3 -type f | sort`
Expected: all planned skills, prompts, doctrine, examples, and tests are present

- [ ] **Step 5: Commit**

```bash
git add marketing-superpowers/README.md marketing-superpowers/doctrine/fashion-creator-doctrine.md
git commit -m "docs: finalize fashion creator vertical"
```

## Build Order Summary

1. foundation and doctrine
2. diagnosis, planning, and message architecture
3. review, readiness, and postmortem
4. platform-specific reviewer prompts
5. deterministic skill-pack checker
6. final docs and verification
