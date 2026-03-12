# Reconstruction-Oriented Dossiers Design

## Goal

Make dossier pages more useful for rebuilding a repository with a unique vision, not just understanding what exists today.

This slice focuses on turning the current analysis output into a stronger reconstruction guide by making each page answer:
- what role this artifact plays
- what must be preserved
- what can change
- how to rebuild it in a new system
- what to implement first

## Current Problem

The current dossier is much better than the first scaffold, but many pages are still mostly descriptive:
- file analysis explains what a file looks like
- workflow pages explain what a process contains
- reconstruction plan is still high-level and generic

That means the dossier helps with understanding, but still leaves too much interpretation work for the rebuild phase.

## Chosen Approach

Keep the existing analyzer outputs, but synthesize them into more reconstruction-oriented pages.

Instead of inventing a new analysis pass, the dossier writer will combine:
- logic findings
- workflow findings
- architecture relationships
- preservation decisions

to generate reconstruction guidance directly on the page.

## Design

### File Analysis Pages

Each file analysis page should gain sections that make rebuilding easier:
- `System Role`
- `Preserve In Rebuild`
- `Safe To Change`
- `Rebuild Strategy`
- `Suggested First Slice`

These should be deterministic and derived from the existing findings.

Examples:
- code/script files should emphasize behavior, interfaces, orchestration, and implementation flexibility
- workflow files should emphasize operator flow, approval gates, and wording changes
- strategy-bearing docs should emphasize intentional differentiation

### Workflow Pages

Workflow pages should gain a small reconstruction section:
- `Rebuild Guidance`

This should summarize:
- what part of the workflow is structural
- what part should be rewritten
- where human approval or escalation must remain

### Reconstruction Plan

The dossier-level reconstruction plan should become more actionable:
- identify the first build slices
- prioritize executable or operator-facing entrypoints
- group work by rebuild dependency instead of only by artifact count

### Clone Blueprint Linkage

The dossier should more explicitly explain how to use the preservation matrix and architecture page together when rebuilding.

## Non-Goals

This slice does not include:
- new analysis models
- a rebuild code generator
- cross-repo reconstruction templates
- UI changes

## Success Criteria

After this slice:
- file pages tell the reader what to preserve, what can change, and how to rebuild
- workflow pages include reconstruction guidance
- the reconstruction plan becomes implementation-oriented instead of generic
- the `superpowers` dossier feels more like a rebuild manual than an analysis dump
- tests and smoke runs pass
