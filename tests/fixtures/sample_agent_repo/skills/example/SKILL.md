---
name: example
description: Use when testing workflow analysis
---

# Example Skill

1. Read the repo.
2. Make a decision.
3. Report findings.
4. Run `scripts/start-example.sh` if you need to verify the runtime path.
5. Use `prompts/reviewer-prompt.md` before changing the implementation in `src/example.py`.

You MUST confirm assumptions before changing behavior.
You MUST preserve the operator workflow instead of bypassing it for speed.
Quality means review before launch and verification before status claims.
Wait for user approval before proceeding.
If issues are found, repeat until approved.
If the loop exceeds 3 attempts, escalate to human.

Human operator approves the next step.
Agent performs the investigation and implementation handoff.
