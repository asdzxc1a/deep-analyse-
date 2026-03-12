# Domain Translation V2 Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the deep-analysis system so it can analyze a source repo and, when given a target domain and optional user vision, generate doctrine, role-system, artifact-equivalence, and domain-translation outputs for a target-aware rebuild.

**Architecture:** Keep the current v1 reconstruction pipeline intact, add deterministic doctrine and role extraction for all runs, and layer target-domain translation on top as an optional mode. Translation mode should synthesize artifact equivalence, target capabilities, rename maps, and target-aware blueprint scaffolding without breaking existing v1 runs.

**Tech Stack:** Python 3.12, typer, pydantic, pytest, existing deep-analysis pipeline and synthesis modules

---

## Planned File Structure

**Create:**
- `src/deep_analysis/analysis/doctrine.py`
  - Deterministic extraction of repo-level beliefs, non-negotiables, quality bar, operator contract, and anti-patterns.
- `src/deep_analysis/analysis/roles.py`
  - Deterministic extraction of roles, responsibilities, handoffs, approvals, and escalation ownership from workflow findings.
- `src/deep_analysis/analysis/equivalence.py`
  - Mapping from source artifacts to target-domain equivalents using workflow, preservation, doctrine, and role evidence.
- `src/deep_analysis/analysis/domain_translation.py`
  - Translation planner that combines source analysis, optional vision input, and target-domain rules into a rebuild contract.
- `src/deep_analysis/synthesis/translation.py`
  - Render helpers for doctrine, role system, artifact-equivalence pages, domain-translation pages, and target-aware blueprint docs.
- `tests/fixtures/marketing_vision.md`
  - Deterministic vision input for translation-mode tests.

**Modify:**
- `src/deep_analysis/models.py`
  - Add new models for doctrine, roles, equivalence, vision, and translation planning.
- `src/deep_analysis/pipeline.py`
  - Wire doctrine, roles, equivalence, and translation through the analysis pipeline with backward-compatible defaults.
- `src/deep_analysis/cli.py`
  - Add `--target-domain` and `--vision-file` support plus validation.
- `src/deep_analysis/synthesis/dossier.py`
  - Add doctrine, role-system, translation, and equivalence sections.
- `src/deep_analysis/synthesis/blueprint.py`
  - Add target-aware blueprint docs and starter layout generation.
- `src/deep_analysis/synthesis/skill_pack.py`
  - Document translation-mode usage in the exported skill pack.
- `tests/test_pipeline.py`
  - Cover doctrine extraction, role extraction, translation outputs, and backward compatibility.
- `tests/test_cli.py`
  - Cover CLI translation-mode arguments and validation behavior.
- `tests/fixtures/sample_agent_repo/README.md`
  - Strengthen doctrine and system-role evidence if needed.
- `tests/fixtures/sample_agent_repo/skills/example/SKILL.md`
  - Strengthen role, approval, and operating-philosophy evidence if needed.
- `tests/fixtures/sample_agent_repo/prompts/reviewer-prompt.md`
  - Strengthen reviewer responsibilities and approval ownership if needed.
- `README.md`
  - Document translation mode, target-domain usage, and expected outputs.
- `MEMORY.md`
  - Record v2 capabilities, commands, and next-step handoff.

## Chunk 1: Red Tests For Doctrine And Role Extraction

**Files:**
- Create: `tests/fixtures/marketing_vision.md`
- Modify: `tests/fixtures/sample_agent_repo/README.md`
- Modify: `tests/fixtures/sample_agent_repo/skills/example/SKILL.md`
- Modify: `tests/fixtures/sample_agent_repo/prompts/reviewer-prompt.md`
- Modify: `tests/test_pipeline.py`

- [ ] **Step 1: Add a deterministic marketing vision fixture**

Write `tests/fixtures/marketing_vision.md` with explicit statements for:
- target audience
- marketing philosophy
- channels to prioritize
- tone and differentiation rules
- what to avoid

- [ ] **Step 2: Strengthen source fixture doctrine signals only where current wording is too weak**

Adjust the sample repo fixtures so repeated signals clearly express:
- operator philosophy
- non-negotiables
- review ownership
- escalation ownership
- handoff expectations

- [ ] **Step 3: Add failing doctrine extraction assertions**

Add tests in `tests/test_pipeline.py` that expect:
- extracted core beliefs
- extracted non-negotiables
- extracted operator contract
- evidence artifacts listed for doctrine findings

- [ ] **Step 4: Add failing role-system assertions**

Add tests in `tests/test_pipeline.py` that expect:
- at least one human reviewer role
- at least one agent executor role
- one or more role handoffs
- explicit approval and escalation ownership

- [ ] **Step 5: Run the targeted tests to capture the red state**

Run: `source .venv/bin/activate && pytest tests/test_pipeline.py -q`
Expected: FAIL on doctrine and role-system assertions because the new analyzers and models do not exist yet

## Chunk 2: Implement Doctrine And Role Models Plus Analyzers

**Files:**
- Create: `src/deep_analysis/analysis/doctrine.py`
- Create: `src/deep_analysis/analysis/roles.py`
- Modify: `src/deep_analysis/models.py`
- Modify: `src/deep_analysis/pipeline.py`
- Modify: `tests/test_pipeline.py`

- [ ] **Step 1: Add new pydantic models in `src/deep_analysis/models.py`**

Add:
- `DoctrineSignal`
- `RepoDoctrine`
- `RoleDefinition`
- `RoleHandoff`
- `RoleSystem`

Model fields should include:
- doctrine evidence paths
- role responsibilities
- handoff source and destination roles
- handoff trigger or contract summary

- [ ] **Step 2: Implement `analysis/doctrine.py`**

Build deterministic extraction from:
- workflow hard constraints
- approval and review semantics
- preservation strategy notes
- source docs with repeated operating-language signals

Return a `RepoDoctrine` with populated evidence.

- [ ] **Step 3: Implement `analysis/roles.py`**

Derive role definitions and handoffs from workflow findings by normalizing:
- human roles
- agent roles
- reviewer roles
- approval owners
- escalation owners

- [ ] **Step 4: Wire doctrine and role extraction into `run_analysis_pipeline`**

Rules:
- always compute doctrine and role system
- do not require translation mode for these outputs
- keep current pipeline output directories intact

- [ ] **Step 5: Run targeted tests until green**

Run: `source .venv/bin/activate && pytest tests/test_pipeline.py -q`
Expected: PASS for doctrine and role-system assertions while existing v1 assertions remain green

## Chunk 3: Red Tests For Translation Mode And Artifact Equivalence

**Files:**
- Modify: `tests/test_pipeline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Add failing artifact-equivalence assertions**

Expect translation mode to emit mappings like:
- source workflow artifact -> target marketing skill
- source review artifact -> target strategy review artifact
- source verification artifact -> target launch-verification artifact

- [ ] **Step 2: Add failing domain-translation output assertions**

Expect dossier and blueprint generation to include:
- `10-doctrine/README.md`
- `11-role-system/README.md`
- `12-domain-translation/README.md`
- `13-artifact-equivalence/README.md`
- `clone-blueprint/docs/domain-translation-map.md`
- `clone-blueprint/docs/role-system.md`
- `clone-blueprint/docs/target-doctrine.md`
- `clone-blueprint/docs/marketing-capability-map.md`

- [ ] **Step 3: Add CLI validation tests**

Use `typer.testing.CliRunner` in `tests/test_cli.py` to cover:
- `--target-domain marketing`
- `--vision-file tests/fixtures/marketing_vision.md`
- rejection of `--vision-file` without `--target-domain`

- [ ] **Step 4: Run targeted tests to capture the red state**

Run: `source .venv/bin/activate && pytest tests/test_pipeline.py tests/test_cli.py -q`
Expected: FAIL on new translation-mode and CLI assertions

## Chunk 4: Implement Artifact Equivalence, Vision Parsing, And Domain Translation

**Files:**
- Create: `src/deep_analysis/analysis/equivalence.py`
- Create: `src/deep_analysis/analysis/domain_translation.py`
- Modify: `src/deep_analysis/models.py`
- Modify: `src/deep_analysis/pipeline.py`
- Modify: `src/deep_analysis/cli.py`
- Modify: `tests/test_pipeline.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Extend models for translation mode**

Add:
- `ArtifactTranslation`
- `VisionProfile`
- `DomainTranslationPlan`

Include fields for:
- target domain
- translation action
- target artifact name and type
- target capability
- rename map
- language shift rules
- vision alignment notes

- [ ] **Step 2: Implement artifact-equivalence mapping**

Use the existing artifact type, workflow semantics, preservation decision, doctrine, and role evidence to assign one translation action per meaningful artifact.

For deterministic v2, support at least:
- `preserve-structure`
- `translate-domain`
- `rewrite-in-user-voice`
- `replace-with-target-equivalent`
- `drop-from-target`
- `new-target-artifact-required`

- [ ] **Step 3: Implement vision-file parsing and translation planning**

Parse the vision markdown as simple structured prose.

Generate a `DomainTranslationPlan` that includes:
- preserved structures
- renamed roles
- translated workflows
- target capabilities
- language-shift rules
- notes where user doctrine overrides source style

- [ ] **Step 4: Add CLI and pipeline support**

Update `src/deep_analysis/cli.py` and `src/deep_analysis/pipeline.py` so:
- existing analyze runs still work unchanged
- translation mode is optional
- `vision_file` is validated and loaded only when requested

- [ ] **Step 5: Run targeted tests until green**

Run: `source .venv/bin/activate && pytest tests/test_pipeline.py tests/test_cli.py -q`
Expected: PASS

## Chunk 5: Render Translation Outputs Into Dossier, Blueprint, And Skill Pack

**Files:**
- Create: `src/deep_analysis/synthesis/translation.py`
- Modify: `src/deep_analysis/synthesis/dossier.py`
- Modify: `src/deep_analysis/synthesis/blueprint.py`
- Modify: `src/deep_analysis/synthesis/skill_pack.py`
- Modify: `tests/test_pipeline.py`

- [ ] **Step 1: Add render helpers in `synthesis/translation.py`**

Create focused render functions for:
- doctrine summary page
- role-system page
- domain-translation page
- artifact-equivalence page
- target doctrine
- role system
- domain-translation map
- marketing capability map

- [ ] **Step 2: Extend dossier generation**

Update `src/deep_analysis/synthesis/dossier.py` so:
- `10-doctrine/README.md` is always written
- `11-role-system/README.md` is always written
- `12-domain-translation/README.md` is written only in translation mode
- `13-artifact-equivalence/README.md` is written only in translation mode

- [ ] **Step 3: Extend blueprint generation**

Update `src/deep_analysis/synthesis/blueprint.py` so translation mode writes:
- `docs/domain-translation-map.md`
- `docs/role-system.md`
- `docs/target-doctrine.md`
- `docs/marketing-capability-map.md`

Also generate target-aware starter structure for `marketing` runs, including starter role and skill placeholders instead of only generic folders.

- [ ] **Step 4: Extend the skill-pack guidance**

Update `src/deep_analysis/synthesis/skill_pack.py` so exported instructions show both:
- reconstruction-only usage
- translation-mode usage with `--target-domain` and `--vision-file`

- [ ] **Step 5: Run dossier and blueprint assertions**

Run: `source .venv/bin/activate && pytest tests/test_pipeline.py -q`
Expected: PASS with the new translation pages and blueprint docs present

## Chunk 6: Docs, Full Verification, And Handoff

**Files:**
- Modify: `README.md`
- Modify: `MEMORY.md`

- [ ] **Step 1: Update `README.md`**

Document:
- translation mode purpose
- analyze command examples
- marketing-target example
- output directories and new translation docs
- backward-compatible non-translation usage

- [ ] **Step 2: Update `MEMORY.md`**

Record:
- doctrine extraction
- role-system extraction
- translation-mode support
- example commands
- current recommended next stage after v2

- [ ] **Step 3: Run the full test suite**

Run: `source .venv/bin/activate && pytest -q`
Expected: PASS

- [ ] **Step 4: Run a local smoke analysis for translation mode**

Run: `source .venv/bin/activate && python -m deep_analysis.cli analyze '/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers' /tmp/superpowers-domain-translation-v2 --export-skill-pack --target-domain marketing --vision-file tests/fixtures/marketing_vision.md`
Expected: dossier, blueprint, and skill-pack generated with doctrine, role-system, domain-translation, and artifact-equivalence outputs

- [ ] **Step 5: Run a remote smoke analysis for translation mode**

Run: `source .venv/bin/activate && python -m deep_analysis.cli analyze https://github.com/obra/superpowers.git /tmp/superpowers-domain-translation-v2-remote --export-skill-pack --target-domain marketing --vision-file tests/fixtures/marketing_vision.md`
Expected: remote clone completes and translation-mode outputs are generated successfully

- [ ] **Step 6: Inspect the most important generated pages**

Inspect:
- `analysis-project/10-doctrine/README.md`
- `analysis-project/11-role-system/README.md`
- `analysis-project/12-domain-translation/README.md`
- `analysis-project/13-artifact-equivalence/README.md`
- `clone-blueprint/docs/domain-translation-map.md`
- `clone-blueprint/docs/marketing-capability-map.md`

- [ ] **Step 7: Commit and push**

Suggested commit sequence:
- `git commit -m "feat: extract doctrine and role system"`
- `git commit -m "feat: add domain translation planning"`
- `git commit -m "docs: describe translation mode"`

## Build Order Summary

1. Fixtures and red tests for doctrine and roles
2. Doctrine and role analyzers plus new models
3. Red tests for translation mode and CLI behavior
4. Artifact equivalence and domain translation planner
5. Dossier, blueprint, and skill-pack rendering
6. README, MEMORY, full verification, and smoke runs
