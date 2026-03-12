# Test And Fixture Preservation Design

## Goal

Make preservation analysis distinguish production artifacts from verification artifacts and test fixtures so the clone blueprint preserves contracts without over-preserving harness-specific material.

## Problem

The current preservation layer treats tests like ordinary behavior-bearing implementation and treats fixture-like docs the same as operator-facing references.

That causes two problems:
- tests are described as if their exact harness shape should be preserved, when what really matters is the verification contract
- fixtures and test-support artifacts are described too generically, when they often need adaptation rather than direct preservation

For reconstruction, we need sharper guidance:
- preserve what the test proves
- adapt how the test proves it
- treat fixture and sample data as supporting test context, not core product behavior

## Design

### 1. Add test-aware artifact roles

Split today’s broad implementation bucket into more specific preservation roles:
- production behavior-bearing implementation
- contract-bearing verification
- test-support fixture or reference artifact
- environment-coupled operations
- human-facing workflow system
- human-facing workflow reference
- strategy-bearing language

### 2. Add more precise preservation decisions

Introduce decisions that separate contract preservation from harness preservation.

New decision vocabulary:
- `preserve-core-behavior`
- `preserve-verification-contract`
- `adapt-test-fixture`
- `preserve-with-review`
- `rewrite-equivalent`
- `rewrite-with-differentiation`

Intent:
- production code keeps `preserve-core-behavior`
- tests become `preserve-verification-contract`
- fixtures become `adapt-test-fixture`

### 3. Detect fixtures deterministically

Use path-based heuristics for v1:
- paths containing `/fixtures/`
- names containing `fixture`, `snapshot`, `golden`, or `sample`
- fixture-like docs or support files inside `tests/`

This remains heuristic but is good enough to make preservation guidance materially more accurate.

### 4. Improve blueprint wording

The preservation matrix and reconstruction plan should make the difference explicit:
- preserve behavior for product/runtime artifacts
- preserve verification intent for tests
- adapt fixture content to the rebuilt system instead of carrying it over blindly

## Non-Goals

This slice does not:
- redesign artifact classification broadly
- add legal reasoning for fixture licenses
- infer semantic test coverage beyond current graph links

## Success Criteria

After this slice:
- tests no longer receive the same preservation guidance as production code
- fixture artifacts receive adaptation-oriented guidance
- the matrix and blueprint make the contract-vs-harness distinction explicit
- smoke-run output on `superpowers` reads more like reconstruction guidance and less like uniform heuristics
