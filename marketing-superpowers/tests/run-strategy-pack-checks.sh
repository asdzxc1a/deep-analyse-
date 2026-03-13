#!/usr/bin/env bash

set -euo pipefail

ROOT="marketing-superpowers/strategy/account"

required_files=(
  "$ROOT/creator-profile.md"
  "$ROOT/audience-map.md"
  "$ROOT/content-pillars.md"
  "$ROOT/series-library.md"
  "$ROOT/platform-strategy.md"
  "$ROOT/first-2-week-plan.md"
  "$ROOT/production-board-weeks-1-2.md"
  "$ROOT/cold-audience-concept-board-v1.md"
  "$ROOT/cold-audience-concept-board-v2-deep-analysis.md"
  "$ROOT/scripted-shooting-boards-top-5.md"
)

for file in "${required_files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "Missing required strategy file: $file" >&2
    exit 1
  fi
done

assert_contains() {
  local file="$1"
  local pattern="$2"
  if ! rg -Fq "$pattern" "$file"; then
    echo "Missing required phrase '$pattern' in $file" >&2
    exit 1
  fi
}

assert_contains "$ROOT/creator-profile.md" "cute rebel kid"
assert_contains "$ROOT/creator-profile.md" "luxurious high-fashion"
assert_contains "$ROOT/audience-map.md" "broad viral audience"
assert_contains "$ROOT/content-pillars.md" "50%"
assert_contains "$ROOT/content-pillars.md" "Rebel-To-Luxury Transformations"
assert_contains "$ROOT/series-library.md" "chaos to couture"
assert_contains "$ROOT/platform-strategy.md" "TikTok: virality engine"
assert_contains "$ROOT/platform-strategy.md" "Instagram: identity engine"
assert_contains "$ROOT/platform-strategy.md" "YouTube: attachment and authority engine"
assert_contains "$ROOT/first-2-week-plan.md" "Week 1"
assert_contains "$ROOT/first-2-week-plan.md" "Week 2"
assert_contains "$ROOT/first-2-week-plan.md" "attitude moment"
assert_contains "$ROOT/cold-audience-concept-board-v1.md" "interrupt"
assert_contains "$ROOT/cold-audience-concept-board-v1.md" "luxury payoff"
assert_contains "$ROOT/cold-audience-concept-board-v2-deep-analysis.md" "she made couture feel alive again"
assert_contains "$ROOT/cold-audience-concept-board-v2-deep-analysis.md" "The Five Viewer Reactions That Build Empires"
assert_contains "$ROOT/cold-audience-concept-board-v2-deep-analysis.md" "The Character Must Have at Least Four Modes"
assert_contains "$ROOT/production-board-weeks-1-2.md" "Shoot Block"
assert_contains "$ROOT/production-board-weeks-1-2.md" "Board Reference"
assert_contains "$ROOT/scripted-shooting-boards-top-5.md" "Opening Line"
assert_contains "$ROOT/scripted-shooting-boards-top-5.md" "First 3 Seconds"
assert_contains "$ROOT/scripted-shooting-boards-top-5.md" "Shot List"
assert_contains "$ROOT/scripted-shooting-boards-top-5.md" "Edit Rhythm"
assert_contains "$ROOT/scripted-shooting-boards-top-5.md" "Platform Variation"

echo "Strategy pack checks passed"
