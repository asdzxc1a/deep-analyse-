# Prompt And Skill Semantic Extraction Design

## Goal

Deepen prompt and skill analysis so the dossier captures the operating logic encoded in instruction-heavy repositories, not just their triggers and ordered steps.

This slice focuses on agent, skill, prompt, and workflow repos such as `superpowers`, where the most important behavior often lives in:
- hard constraints
- approval gates
- review loops
- escalation paths
- human/agent responsibility boundaries
- reusable operating patterns

## Current Problem

The existing workflow analyzer extracts trigger conditions, ordered steps, basic decision gates, and rough human/agent roles.

That is useful, but still too shallow. It misses the higher-order semantics that actually determine how the system is meant to operate:
- what is non-negotiable
- where a user must approve before continuing
- when a review loop repeats
- when the system must stop and escalate
- which operating patterns are shared across artifacts

As a result, workflow pages still read like summarized outlines instead of operational reconstruction.

## Chosen Approach

Use deterministic semantic extraction instead of trying to infer intent with a model-heavy layer.

The analyzer will continue to process skills, prompts, docs, and CI files, but skill/prompt extraction will gain specific semantic passes for:
- hard constraints
- approval gates
- review loops
- escalation paths
- reusable operating patterns

These fields should be explicit in the output model and in workflow dossier pages.

## Design

### Data Model

`WorkflowFinding` should be expanded to include:
- `hard_constraints`
- `approval_gates`
- `review_loops`
- `escalation_paths`
- `reusable_patterns`

These are in addition to:
- `summary`
- `trigger_conditions`
- `steps`
- `decision_gates`
- `human_role`
- `agent_role`

### Semantic Extraction

For skills and prompts:
- extract hard constraints from lines containing patterns like `MUST`, `NEVER`, `REQUIRED`, `DO NOT`, `non-negotiable`
- extract approval gates from lines mentioning `approval`, `approve`, `review`, `wait for the user's response`, `user reviews`
- extract review loops from lines mentioning `repeat until`, `re-dispatch`, `loop`, `until approved`, `re-review`
- extract escalation paths from lines mentioning `stop`, `surface to human`, `ask for help`, `blocked`, `exceeds`
- derive reusable pattern labels from the presence of those signals, for example:
  - `guardrailed workflow`
  - `human approval gate`
  - `iterative review loop`
  - `human escalation path`
  - `human-agent handoff`

For docs:
- keep extraction lighter, but allow the same semantic passes if the patterns are present

For CI:
- continue to treat it primarily as operational automation rather than human-instruction semantics

### Output Behavior

Workflow dossier pages should gain new sections:
- `Hard Constraints`
- `Approval Gates`
- `Review Loops`
- `Escalation Paths`
- `Reusable Patterns`

These pages should make it much easier to reconstruct a prompt/skill system in another repo.

### Scope Boundaries

This slice is about explicit semantic structure, not free-form interpretation.

It does not include:
- embedding-based clustering
- LLM-driven semantic summaries
- cross-artifact pattern mining beyond deterministic labels
- architecture changes
- preservation logic changes

## Success Criteria

After this slice:
- skill and prompt pages extract real non-negotiable instructions, approval gates, loops, and escalation rules
- reusable operating patterns are surfaced in a deterministic way
- the sample fixtures and `superpowers` smoke run show materially deeper workflow pages
- full tests and smoke runs pass
