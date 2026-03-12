# Validation-Aware Architecture Design

## Goal

Separate runtime critical paths from validation critical paths so the architecture output shows both how a repo operates and how it proves correctness.

## Problem

The current architecture page exposes a single `Critical Paths` section. That is useful, but it mixes two different kinds of paths:
- runtime or operator-facing execution chains
- validation or verification chains from tests and CI to target artifacts

For reconstruction, those two path types matter differently:
- runtime paths tell you what to rebuild so the system works
- validation paths tell you what to rebuild so the system is provably correct

## Design

### 1. Add validation-aware architecture fields

Extend the architecture summary with:
- runtime critical paths
- validation paths

Keep existing `critical_paths` as the runtime-oriented list for backward compatibility if needed, but make the dossier page explicit about validation paths.

### 2. Derive validation paths deterministically

Validation paths should come from:
- `test` artifacts with outgoing edges
- `ci` artifacts with outgoing edges

Use the same longest-reachable-path logic already used for runtime critical paths, but keep these paths in a separate bucket.

### 3. Update architecture narrative

The architecture page should explicitly say that the repo has:
- execution/runtime flows
- validation/verification flows

### 4. Feed validation paths into reconstruction guidance

The reconstruction plan should reference both:
- the first runtime critical path
- the first validation path

This helps the rebuild process preserve not only behavior but also the path used to verify behavior.

## Non-Goals

This slice does not:
- build a full call graph
- infer semantic test coverage
- add probabilistic reasoning about validation completeness

## Success Criteria

After this slice:
- the architecture page includes a dedicated validation-path section
- test and CI verification chains are visible in the dossier
- reconstruction guidance references validation flow as part of rebuild order
