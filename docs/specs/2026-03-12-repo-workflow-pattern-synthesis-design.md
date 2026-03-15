# Repo Workflow Pattern Synthesis Design

## Goal

Teach the system to synthesize reusable operating patterns across multiple workflow-bearing artifacts, not just list per-file reusable labels.

## Problem

The current workflow analysis is useful at the artifact level:
- each skill, prompt, doc, or CI file gets triggers, steps, constraints, approval gates, review loops, escalation paths, and reusable patterns

But the system still misses the repo-level operating language:
- recurring approval-gate structures
- shared review-loop behavior
- repeated escalation design
- common human/agent handoff contracts
- patterns that appear across more than one workflow artifact

That means the dossier is still strong at “what each file does” and weaker at “what style of operating system this repo repeats.”

## Design

### 1. Add repo-level workflow pattern synthesis

Build a deterministic synthesis layer on top of existing workflow findings.

For v1, each repo-level pattern should include:
- a stable pattern name
- a short summary
- evidence artifacts that exhibit the pattern
- a reconstruction note describing how to preserve the operating style

### 2. Base synthesis on repeated semantics

Patterns should only be emitted when they are supported by more than one workflow-bearing artifact.

Initial deterministic pattern families:
- human approval gate
- iterative review loop
- human escalation path
- human-agent handoff
- guardrailed workflow

Each pattern is synthesized from repeated workflow-finding evidence, not from speculative NLP inference.

### 3. Surface patterns in the dossier

Add a repo-level workflow-patterns page under the workflow section so the analysis-project explicitly captures the repeated operating motifs of the source repo.

The workflow index should link to this page.

### 4. Feed patterns into reconstruction outputs

The reconstruction plan and clone blueprint should reference the synthesized patterns so rebuild work preserves the repo’s operating style, not just its artifact inventory.

## Non-Goals

This slice does not:
- add embedding-based clustering
- infer patterns from code architecture alone
- perform cross-repo pattern mining
- redesign the entire workflow analysis data model

## Success Criteria

After this slice:
- repos like `superpowers` produce repo-level workflow patterns with evidence
- the dossier includes a dedicated pattern-synthesis page
- the blueprint carries those patterns into rebuild guidance
- tests prove pattern synthesis only triggers on repeated, cross-artifact evidence
