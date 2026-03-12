# Preservation Analysis Design

## Goal

Deepen preservation analysis so the clone blueprint explains not only what to preserve or rewrite, but why, with more operational, strategic, and future legal-review context.

This slice focuses on making the preservation matrix reconstruction-grade for agent, skill, prompt, and workflow repositories.

## Current Problem

The existing preservation analyzer is too coarse. It mostly assigns:
- `rewrite-equivalent`
- `preserve-with-review`
- `preserve`

That is directionally helpful, but still too weak for real rebuild work because it does not explain:
- whether the artifact is behavior-bearing vs language-bearing
- whether it should be rewritten verbatim-equivalent or intentionally differentiated
- whether legal review is prudent before reuse
- whether the artifact is strategically central or peripheral

As a result, the clone blueprint still lacks enough decision-making support for confident reconstruction.

## Chosen Approach

Use a richer deterministic preservation model rather than trying to do true legal analysis.

The system will remain explicit that it is not giving legal advice, but it will surface:
- stronger decision categories
- artifact role
- strategy guidance
- legal-review flags
- heuristic confidence

This gives the operator a much better reconstruction map while preserving deterministic behavior.

## Design

### Decision Model

`PreservationDecision` should expand to include:
- `artifact_role`
- `strategy_note`
- `legal_review`
- `confidence`

Suggested decision vocabulary:
- `rewrite-with-differentiation`
- `rewrite-equivalent`
- `preserve-core-behavior`
- `preserve-with-review`

### Decision Heuristics

The analyzer should distinguish between:

#### Human-facing strategy artifacts
Examples:
- top-level README-like docs
- release notes
- positioning docs

Decision:
- `rewrite-with-differentiation`

Reasoning:
- these shape product voice and market positioning
- they should not be carried over mechanically into a rebuilt system

#### Human-facing operational workflow artifacts
Examples:
- skills
- prompts
- procedure docs

Decision:
- usually `rewrite-equivalent`

Reasoning:
- preserve the operator workflow and system intent
- rewrite into the new operator’s own language

#### Behavior-bearing implementation artifacts
Examples:
- code
- scripts
- hooks
- tests

Decision:
- `preserve-core-behavior`

Reasoning:
- preserve the observable system role and interfaces
- reimplementation details may change

#### Environment-coupled operational artifacts
Examples:
- CI
- config

Decision:
- `preserve-with-review`

Reasoning:
- these often encode environment assumptions, automation, or deployment coupling
- they should be preserved carefully with human review

### Future Legal Awareness

This system is not a lawyer and should not claim otherwise.

But it can still surface prudent review flags:
- `recommended` for human-facing language artifacts and license-adjacent concerns
- `required-before-reuse` for artifacts that would be risky to carry over too directly
- `not-usually-needed` for behavior-bearing artifacts where the main issue is reconstruction, not wording

This is a workflow signal, not legal advice.

### Strategy Guidance

Each decision should include a short strategy note answering:
- preserve the role?
- differentiate the voice?
- keep the interface?
- review environment coupling?

This should make the blueprint more directly actionable.

### Blueprint Output

The preservation matrix should expand to include:
- path
- role
- decision
- legal review
- confidence
- strategy note
- rationale

## Non-Goals

This slice does not include:
- real legal analysis
- SPDX or license parsing
- repository license enforcement
- automatic policy decisions based on jurisdiction

## Success Criteria

After this slice:
- preservation decisions are more nuanced than the current three-bucket output
- matrix rows clearly distinguish strategy-bearing docs from workflow-bearing docs and behavior-bearing artifacts
- blueprint output is more helpful for rebuilding with a unique vision
- tests and smoke runs pass
