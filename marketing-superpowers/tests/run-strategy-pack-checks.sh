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

echo "Strategy pack checks passed"
