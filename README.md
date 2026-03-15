# Deep Analysis System

Analyze one GitHub repository at a time and produce:
- a reconstruction-grade dossier
- a clone blueprint repo
- an optional reusable analysis skill pack

The current implementation is optimized first for agent, skill, workflow, prompt, and automation repositories such as `obra/superpowers`.

## What v2 adds

The system now supports an optional translation mode that upgrades a reconstruction run into a target-aware rebuild contract.

Translation mode adds:
- repo doctrine extraction
- role-system and handoff extraction
- artifact-equivalence mapping
- target-domain translation planning
- target-aware blueprint docs for a rebuilt system

The initial target-aware path is designed for cases like:
- source repo: `superpowers`
- target domain: `marketing`
- output: a marketing-native version that preserves rigor, approvals, review loops, and verification discipline

## What v1 still does well

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

In translation mode, the dossier also includes:
- `10-doctrine/README.md`
- `11-role-system/README.md`
- `12-domain-translation/README.md`
- `13-artifact-equivalence/README.md`

In translation mode, the blueprint also includes:
- `docs/domain-translation-map.md`
- `docs/role-system.md`
- `docs/target-doctrine.md`
- `docs/marketing-capability-map.md`

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

## Translation mode

Use translation mode when you want the system to propose how the source repo should become a system in a new domain.

Example:

```bash
python -m deep_analysis.cli analyze \
  https://github.com/obra/superpowers.git \
  /tmp/superpowers-marketing \
  --export-skill-pack \
  --target-domain marketing \
  --vision-file tests/fixtures/marketing_vision.md
```

That run will:
- analyze the source repo as before
- extract source doctrine and role system
- map source artifacts into target-domain equivalents
- generate a target-aware domain-translation plan
- build a marketing-oriented blueprint scaffold

Useful translation outputs:
- `/tmp/superpowers-marketing/analysis-project/10-doctrine/README.md`
- `/tmp/superpowers-marketing/analysis-project/11-role-system/README.md`
- `/tmp/superpowers-marketing/analysis-project/12-domain-translation/README.md`
- `/tmp/superpowers-marketing/analysis-project/13-artifact-equivalence/README.md`
- `/tmp/superpowers-marketing/clone-blueprint/docs/domain-translation-map.md`
- `/tmp/superpowers-marketing/clone-blueprint/docs/marketing-capability-map.md`

## Recommended smoke test

```bash
python -m deep_analysis.cli analyze "/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers" /tmp/superpowers-v1-final-20260312 --export-skill-pack
```

Recommended translation smoke test:

```bash
python -m deep_analysis.cli analyze "/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers" /tmp/superpowers-domain-translation-v2 --export-skill-pack --target-domain marketing --vision-file tests/fixtures/marketing_vision.md
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
- domain translation is deterministic and rule-based, not model-inferred
- translation mode is strongest today for agent/workflow repos and the `marketing` target domain
