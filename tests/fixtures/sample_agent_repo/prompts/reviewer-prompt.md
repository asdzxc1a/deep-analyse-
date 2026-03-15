# Reviewer Prompt

Use when reviewing a generated spec before implementation.

1. Read the spec.
2. List missing requirements.
3. Wait for user approval before marking the review complete.
4. Confirm `src/example.py` still matches the expectations captured in `tests/test_example.py`.

You MUST identify any requirement gaps before approving the document.
NEVER skip the review loop because the task looks simple.
The reviewer owns approval and protects the quality bar for this repo.
If issues are found, repeat until approved.
If the loop exceeds 3 iterations, escalate to the human operator.

Human reviewer approves or rejects the recommendation.
Agent executes the review workflow and reports the outcome.
