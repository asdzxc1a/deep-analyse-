# Domain Translation V2 Design

## Goal

Upgrade the system from a reconstruction engine into a reconstruction plus domain-translation engine so it can analyze a source repo like `superpowers` and produce a target-aware rebuild plan for a new domain such as marketing.

## Problem

V1 is now strong at:
- identifying meaningful artifacts
- extracting workflows, constraints, and review loops
- reconstructing architecture and validation paths
- producing a reconstruction-oriented dossier and clone blueprint

That makes it useful for understanding a source repo and preserving its operating structure.

The remaining gap is translation.

Today the system does not explicitly answer:
- what beliefs govern the repo
- which roles and handoffs make the system work
- which source artifacts should become which target-domain artifacts
- how to preserve structure while changing domain language and outputs
- how to inject the user’s own doctrine into the rebuilt system

That means it can explain `superpowers`, but it cannot yet generate a marketing-aware rebuild contract for “my version of `superpowers`.”

## Design

### 1. Add an explicit translation mode

Extend the `analyze` workflow so a run can optionally include:
- a `target_domain` such as `marketing`
- a `vision_file` containing the user’s doctrine, audience, preferences, and differentiation goals

CLI shape:

```bash
python -m deep_analysis.cli analyze \
  https://github.com/obra/superpowers.git \
  /tmp/superpowers-marketing \
  --export-skill-pack \
  --target-domain marketing \
  --vision-file tests/fixtures/marketing_vision.md
```

Rules:
- doctrine and role extraction should run for every repo because they improve reconstruction even without translation mode
- artifact equivalence and domain-translation planning should run only when `target_domain` is provided
- `vision_file` is optional, but when present it should further steer the translation outputs instead of being ignored

### 2. Add doctrine extraction

Create a deterministic `analysis/doctrine.py` pass that synthesizes repo-level beliefs from repeated workflow constraints, preservation guidance, architecture patterns, and human-facing docs.

Add these models:
- `RepoDoctrine`
- `DoctrineSignal`

For v2, doctrine should capture:
- `core_beliefs`
- `non_negotiables`
- `quality_bar`
- `operator_contract`
- `anti_patterns`
- `evidence_artifacts`

This is the missing layer that explains what the repo believes, not just what its files say.

### 3. Add role and handoff extraction

Create a deterministic `analysis/roles.py` pass that converts workflow findings into a repo-level role system.

Add these models:
- `RoleDefinition`
- `RoleHandoff`
- `RoleSystem`

For v2, the role system should capture:
- named roles
- each role’s responsibilities
- approval ownership
- escalation ownership
- handoff edges between human, agent, and automation roles

This makes the repo reconstructable as an operating system instead of a set of isolated prompts and files.

### 4. Add artifact equivalence mapping

Create `analysis/equivalence.py` to propose what each source artifact should become in the target domain.

Add these models:
- `ArtifactTranslation`
- `ArtifactTranslationDecision`

Each translation record should include:
- `source_path`
- `source_artifact_type`
- `source_role`
- `preservation_decision`
- `translation_action`
- `target_artifact_name`
- `target_artifact_type`
- `target_capability`
- `translation_reason`

Initial translation actions:
- `preserve-structure`
- `translate-domain`
- `rewrite-in-user-voice`
- `replace-with-target-equivalent`
- `drop-from-target`
- `new-target-artifact-required`

For the `superpowers -> marketing` path, this layer should be able to suggest mappings such as:
- `systematic-debugging` -> `systematic-campaign-diagnosis`
- `writing-plans` -> `campaign-planning`
- `requesting-code-review` -> `requesting-strategy-review`
- `verification-before-completion` -> `verification-before-launch`

### 5. Add domain-translation planning

Create `analysis/domain_translation.py` to synthesize a target-aware translation plan from:
- source reconstruction outputs
- repo doctrine
- role system
- artifact equivalence mapping
- optional user vision

Add these models:
- `VisionProfile`
- `DomainTranslationPlan`

The translation plan should capture:
- `target_domain`
- `preserve_structures`
- `rename_map`
- `role_map`
- `workflow_map`
- `artifact_map`
- `language_shift_rules`
- `target_capabilities`
- `vision_alignment_notes`

This is the layer that turns “understand the repo” into “build my version of the repo.”

### 6. Keep the translation engine deterministic and inspectable

V2 should stay deterministic and text-first.

It should not depend on:
- embeddings
- opaque clustering services
- an external LLM call

Instead, it should derive outputs from existing findings plus explicit target-domain rules and optional user doctrine text. The first version should be explainable and testable artifact by artifact.

### 7. Extend the dossier

Keep the current dossier structure intact and add four new sections:
- `10-doctrine/README.md`
- `11-role-system/README.md`
- `12-domain-translation/README.md`
- `13-artifact-equivalence/README.md`

Rules:
- `10-doctrine` and `11-role-system` should always be generated
- `12-domain-translation` and `13-artifact-equivalence` should be generated only in translation mode

These sections should explain:
- the governing philosophy of the source repo
- the operational role system
- what changes in the target domain
- what each meaningful artifact should become

### 8. Extend the clone blueprint

Add target-aware blueprint docs:
- `docs/domain-translation-map.md`
- `docs/role-system.md`
- `docs/target-doctrine.md`
- `docs/marketing-capability-map.md`

Also upgrade starter layout generation so target-domain runs create a scaffold that feels like the intended rebuild, not a generic placeholder tree.

For `marketing`, starter directories should be able to include structures like:
- `skills/positioning`
- `skills/campaign-planning`
- `skills/copy-review`
- `skills/launch-verification`
- `prompts/strategist-prompt.md`
- `prompts/copywriter-prompt.md`
- `prompts/analyst-prompt.md`

### 9. Preserve backward compatibility

V1 behavior should continue to work when no `target_domain` is provided.

Backward-compatible expectations:
- current CLI usage still works
- current reconstruction dossier and blueprint still generate
- translation-specific docs do not appear unless translation mode is requested
- tests for existing v1 behavior remain green

## File-Level Design

Create:
- `src/deep_analysis/analysis/doctrine.py`
- `src/deep_analysis/analysis/roles.py`
- `src/deep_analysis/analysis/equivalence.py`
- `src/deep_analysis/analysis/domain_translation.py`
- `src/deep_analysis/synthesis/translation.py`

Modify:
- `src/deep_analysis/models.py`
- `src/deep_analysis/pipeline.py`
- `src/deep_analysis/cli.py`
- `src/deep_analysis/synthesis/dossier.py`
- `src/deep_analysis/synthesis/blueprint.py`
- `src/deep_analysis/synthesis/skill_pack.py`
- `tests/test_pipeline.py`
- `tests/test_cli.py`
- `README.md`
- `MEMORY.md`

Add fixtures:
- `tests/fixtures/marketing_vision.md`
- one or more repo fixture docs/prompts that make doctrine and role extraction testable through repeated evidence

## Non-Goals

This slice does not:
- generate the finished marketing repo itself
- perform legal analysis beyond stronger routing and flags
- add external AI inference
- solve arbitrary domain mapping beyond deterministic target-aware rules
- replace the current reconstruction pipeline with a new architecture

## Success Criteria

After v2:
- a translation-mode run can produce target-aware dossier and blueprint outputs
- the dossier explains source doctrine and role system explicitly
- the blueprint includes a domain-translation map and target capability map
- `superpowers` can be translated into a marketing-oriented rebuild contract with deterministic suggested equivalents
- v1 analyze runs remain backward compatible
