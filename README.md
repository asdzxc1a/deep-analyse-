# Deep Analysis System

Analyze one GitHub repository at a time and produce:
- a reconstruction-grade dossier
- a clone blueprint repo
- an optional reusable analysis skill pack

The current implementation is optimized first for agent, skill, workflow, prompt, and automation repositories such as `obra/superpowers`.

## What v1 does well

The current v1 can:
- classify meaningful artifacts across docs, skills, prompts, code, scripts, CI, and tests
- generate one dossier page per meaningful artifact
- extract workflow semantics such as constraints, approval gates, review loops, escalation paths, and human/agent roles
- recover cross-artifact links between docs, prompts, tests, scripts, and implementation files
- synthesize repo-level workflow patterns from repeated operating motifs
- generate preservation guidance that distinguishes:
  - product behavior
  - workflow language
  - verification contracts
  - fixture and sample harness material
- write a clone blueprint with preservation, workflow-pattern, and reconstruction guidance

## Main outputs

`analysis-project/` includes:
- source profile
- repo map
- file-by-file analysis
- workflow / prompt / skill pages
- repo-level workflow patterns
- architecture summary
- preservation boundaries
- reconstruction plan

`clone-blueprint/` includes:
- preservation matrix
- workflow patterns
- reconstruction plan
- starter source and test directories
- differentiation notes
- migration notes

## Local setup

```bash
cd "/Users/dmytrnewaimastery/Documents/Codex app projects/deep-analysis-system"
/Users/dmytrnewaimastery/.homebrew/Cellar/python@3.12/3.12.13/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Analyze a repository

```bash
deep-analysis analyze https://github.com/obra/superpowers.git /tmp/superpowers-analysis --export-skill-pack
```

Outputs:
- `/tmp/superpowers-analysis/analysis-project`
- `/tmp/superpowers-analysis/clone-blueprint`
- `/tmp/superpowers-analysis/skill-pack`

The dossier includes:
- repo map and entry points
- one markdown page per meaningful artifact
- workflow extraction for skills, prompts, docs, and CI files
- repo-level workflow pattern synthesis
- architecture relationships and validation-aware path reporting
- preservation boundaries and reconstruction plan

## Recommended smoke test

```bash
python -m deep_analysis.cli analyze "/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers" /tmp/superpowers-v1-final-20260312 --export-skill-pack
```

Useful outputs from that run:
- `/tmp/superpowers-v1-final-20260312/analysis-project`
- `/tmp/superpowers-v1-final-20260312/clone-blueprint`
- `/tmp/superpowers-v1-final-20260312/skill-pack`

## Current limits

This is a strong heuristic v1, not a full semantic reverse-engineering engine.

Known limits:
- logic and workflow extraction are deterministic and heuristic
- prompt-template extraction can still include some instructional noise in very large prompts
- validation paths depend on explicit graph evidence
- fixture detection is still path/name based rather than semantic
- repo-level workflow patterns are grouped by deterministic families, not embedding-based clustering
