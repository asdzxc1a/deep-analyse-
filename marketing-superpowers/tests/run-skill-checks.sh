#!/usr/bin/env bash

set -euo pipefail

ROOT="marketing-superpowers"

required_files=(
  "$ROOT/README.md"
  "$ROOT/doctrine/fashion-creator-doctrine.md"
  "$ROOT/skills/creator-diagnosis/SKILL.md"
  "$ROOT/skills/creator-content-planning/SKILL.md"
  "$ROOT/skills/contrast-message-architecture/SKILL.md"
  "$ROOT/skills/viral-content-review/SKILL.md"
  "$ROOT/skills/posting-readiness-check/SKILL.md"
  "$ROOT/skills/content-postmortem/SKILL.md"
  "$ROOT/prompts/instagram-reviewer-prompt.md"
  "$ROOT/prompts/tiktok-reviewer-prompt.md"
  "$ROOT/prompts/youtube-reviewer-prompt.md"
  "$ROOT/examples/content-pillar-example.md"
  "$ROOT/examples/postmortem-example.md"
  "$ROOT/examples/weekly-plan-example.md"
  "$ROOT/tests/prompts/creator-diagnosis.txt"
  "$ROOT/tests/prompts/creator-content-planning.txt"
  "$ROOT/tests/prompts/viral-content-review.txt"
  "$ROOT/tests/prompts/posting-readiness.txt"
  "$ROOT/tests/test-skill-coverage.md"
)

for file in "${required_files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "Missing required file: $file" >&2
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

assert_contains "$ROOT/skills/creator-diagnosis/SKILL.md" "random posting"
assert_contains "$ROOT/skills/creator-content-planning/SKILL.md" "weekly content system"
assert_contains "$ROOT/skills/contrast-message-architecture/SKILL.md" "tomboy/high-fashion contrast"
assert_contains "$ROOT/skills/viral-content-review/SKILL.md" "shareability"
assert_contains "$ROOT/skills/posting-readiness-check/SKILL.md" "publish readiness"
assert_contains "$ROOT/skills/content-postmortem/SKILL.md" "rewatches"
assert_contains "$ROOT/skills/content-postmortem/SKILL.md" "what to stop"
assert_contains "$ROOT/prompts/tiktok-reviewer-prompt.md" "immediate hook"
assert_contains "$ROOT/prompts/instagram-reviewer-prompt.md" "recognizability"
assert_contains "$ROOT/prompts/youtube-reviewer-prompt.md" "character depth"

echo "Skill checks passed"
