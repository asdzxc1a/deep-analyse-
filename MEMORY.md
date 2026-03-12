# Deep Analysis System Memory

Last updated: 2026-03-11

## Purpose

This repo is a separate system inspired by `superpowers`, but aimed at deep reverse engineering of GitHub repositories so they can be understood and then rebuilt with a unique vision.

The target behavior is:
- analyze one repository at a time
- produce a reconstruction-grade dossier
- produce a clone blueprint repo
- optionally export a reusable analysis skill pack

The strongest initial focus is:
- agent repos
- skills/workflow repos
- prompt systems
- automation frameworks

## What We Decided

We chose a hybrid staged system instead of a pure static parser or a pure free-form multi-agent team.

The intended pipeline is:
1. intake or clone one source repo
2. map meaningful artifacts, entry points, and subsystems
3. run deep analysis passes on logic, workflows, architecture, and preservation boundaries
4. write an `analysis-project` dossier
5. write a `clone-blueprint`
6. optionally write a reusable `skill-pack`

We also decided the default dossier depth should be maximum depth for meaningful artifacts unless explicitly excluded.

We decided the preservation rule for clone generation is:
- preserve as much as legally possible
- rewrite human-facing language and workflow text when needed
- keep architecture and behavior where legally and strategically appropriate

## Output Contract

Each analysis run should create:

- `analysis-project/`
- `clone-blueprint/`
- optional `skill-pack/`

`analysis-project/` should contain:
- source profile
- repo map
- file-by-file analysis pages
- workflow / prompt / skill extraction pages
- architecture summary
- preservation boundaries
- reconstruction plan

`clone-blueprint/` should contain:
- preservation matrix
- reconstruction plan
- starter source layout
- starter test layout
- differentiation notes
- migration notes

## Current Implementation Status

The system is no longer just scaffold output. It now generates real dossier pages and workflow pages.

Implemented:
- richer artifact model in `src/deep_analysis/models.py`
- deterministic logic analysis in `src/deep_analysis/analysis/logic.py`
- workflow extraction for skills, docs, prompts, and CI in `src/deep_analysis/analysis/workflows.py`
- architecture synthesis in `src/deep_analysis/analysis/architecture.py`
- preservation decisions in `src/deep_analysis/analysis/preservation.py`
- real dossier writer in `src/deep_analysis/synthesis/dossier.py`
- real blueprint writer in `src/deep_analysis/synthesis/blueprint.py`
- reusable skill-pack writer in `src/deep_analysis/synthesis/skill_pack.py`
- pipeline wiring in `src/deep_analysis/pipeline.py`
- classifier fixes in `src/deep_analysis/classifier.py`

## Important Fixes Made

### 1. Scaffold dossier upgraded to real output

Originally the system mostly created folders and placeholder README files.

Now it writes:
- one markdown page per meaningful artifact
- one markdown page per workflow-bearing artifact
- repo map with meaningful artifacts
- architecture page with entry points
- preservation boundaries page
- reconstruction plan page

### 2. Workflow extraction improved

Originally the workflow extractor missed numbered markdown steps like `1. Read the repo.` and wrote shallow results.

Now it extracts:
- trigger conditions
- ordered steps
- decision gates
- human role
- agent role

It also supports:
- skills
- prompts
- docs
- CI workflow files

### 3. Classification bug fixed

Originally every file under `skills/` was being classified as a skill artifact, including JavaScript and support docs.

That is fixed now:
- `SKILL.md` -> `skill`
- `*.js` / `*.py` / `*.ts` / `*.tsx` -> `code`
- `*.sh` -> `script`
- `*prompt*.md` -> `prompt`
- other markdown/text docs -> `doc`
- GitHub workflow yaml -> `ci`

This mattered because the first real smoke run on `superpowers` exposed incorrect analysis pages like JavaScript files being labeled as skills.

## Principles We Followed

These were the working principles during design and implementation:

- one repo at a time
- maximum depth for meaningful artifacts
- strongest support first for agent and workflow repos
- deterministic coverage first, then richer interpretation
- visible outputs on disk matter, not just internal analysis objects
- prompt and skill systems must be treated as operational logic, not just documentation
- preservation decisions must be explicit before blueprint generation
- keep outputs reusable across future repos

Process principles used in this session:
- use `brainstorming` before design changes
- use TDD before implementation changes
- verify with fresh test and smoke-run evidence before claiming completion
- fix root causes rather than patching symptoms

## Verified Commands

Project setup:

```bash
cd "/Users/dmytrnewaimastery/Documents/Codex app projects/deep-analysis-system"
source .venv/bin/activate
```

Run tests:

```bash
pytest -q
```

Analyze a local repo:

```bash
python -m deep_analysis.cli analyze "/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers" /tmp/superpowers-deep-analysis-final-20260311-v2 --export-skill-pack
```

Analyze a remote repo:

```bash
python -m deep_analysis.cli analyze https://github.com/obra/superpowers.git /tmp/superpowers-deep-analysis-remote-20260311
```

## Fresh Verification Evidence

Most recent verified results:

- `pytest -q` -> `16 passed in 0.15s`
- local smoke run completed:
  `python -m deep_analysis.cli analyze "/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers" /tmp/superpowers-deep-analysis-final-20260311-v2 --export-skill-pack`
- remote smoke run completed:
  `python -m deep_analysis.cli analyze https://github.com/obra/superpowers.git /tmp/superpowers-deep-analysis-remote-20260311`

## Where The Generated Outputs Are

Primary local smoke-run outputs:

- `/tmp/superpowers-deep-analysis-final-20260311-v2/analysis-project`
- `/tmp/superpowers-deep-analysis-final-20260311-v2/clone-blueprint`
- `/tmp/superpowers-deep-analysis-final-20260311-v2/skill-pack`

Useful example pages:

- `/tmp/superpowers-deep-analysis-final-20260311-v2/analysis-project/03-file-analysis/skills-brainstorming-skill-md.md`
- `/tmp/superpowers-deep-analysis-final-20260311-v2/analysis-project/03-file-analysis/skills-brainstorming-scripts-index-js.md`
- `/tmp/superpowers-deep-analysis-final-20260311-v2/analysis-project/04-workflows-prompts-skills/skills-subagent-driven-development-implementer-prompt-md.md`
- `/tmp/superpowers-deep-analysis-final-20260311-v2/clone-blueprint/docs/preservation-matrix.md`

## Git State

Repo:
- `/Users/dmytrnewaimastery/Documents/Codex app projects/deep-analysis-system`

Branch:
- `codex/deep-analysis-system`

PR:
- `https://github.com/asdzxc1a/deep-analyse-/pull/1`

Latest pushed commit at the time of this memory:
- `0adcec2` - `Deepen dossier and workflow analysis outputs`

There is one untracked local path left intentionally untouched:
- `.superpowers/`

## Most Important Files

Core entry points:
- `src/deep_analysis/cli.py`
- `src/deep_analysis/pipeline.py`

Core analysis modules:
- `src/deep_analysis/classifier.py`
- `src/deep_analysis/cartography.py`
- `src/deep_analysis/analysis/logic.py`
- `src/deep_analysis/analysis/workflows.py`
- `src/deep_analysis/analysis/architecture.py`
- `src/deep_analysis/analysis/preservation.py`

Output writers:
- `src/deep_analysis/synthesis/dossier.py`
- `src/deep_analysis/synthesis/blueprint.py`
- `src/deep_analysis/synthesis/skill_pack.py`

Tests:
- `tests/test_classifier.py`
- `tests/test_pipeline.py`

## Known Limits Right Now

The system is meaningfully better than the first MVP, but it is still not the final form of the deep-analysis vision.

Current limitations:
- logic analysis is still heuristic and deterministic, not true semantic reverse engineering
- dependencies extraction is basic
- architecture synthesis is still subsystem-oriented, not full call-flow reconstruction
- preservation decisions are rule-based, not license-aware or strategy-aware
- dossier writing is now real, but not yet as deep as line-by-line architectural interpretation
- there is no long-lived memory or repo history database yet
- there is no interactive “rebuild with my vision” transformation engine yet

## Best Next Steps

If work resumes tomorrow, the strongest next slice is:

1. deepen logic analysis for code and script files
2. improve prompt and skill semantic extraction beyond bullet/number parsing
3. add richer architecture reconstruction from imports, references, and repo structure
4. improve preservation analysis with stronger rationale and future license awareness
5. make dossier pages more reconstruction-oriented, not just descriptive

If the goal is immediate practical value, start with:
- better code-file analysis for `*.py`, `*.js`, `*.ts`, `*.sh`
- richer prompt/skill analysis for agent repos

## How To Resume Tomorrow

Open this file first:
- `MEMORY.md`

Then re-check the repo state:

```bash
cd "/Users/dmytrnewaimastery/Documents/Codex app projects/deep-analysis-system"
git status --short --branch
source .venv/bin/activate
pytest -q
```

If the next task is to deepen the analyzer, continue from the current verified branch:
- `codex/deep-analysis-system`

If the next task is to inspect current outputs, open:
- `/tmp/superpowers-deep-analysis-final-20260311-v2/analysis-project`

## One-Line Session Handoff

We designed and implemented the first real version of the deep-analysis system, upgraded it from scaffold outputs to actual dossier/workflow/blueprint generation, fixed the major classification bug discovered on a real `superpowers` smoke run, verified it locally and against the GitHub repo, and pushed the finished upgrade to PR #1.
