# Deep Analysis System Memory

Last updated: 2026-03-12

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

## What The System Can Do So Far

Today, the system can already do these things in a useful way:

- analyze one repo at a time from a local path or GitHub URL
- classify meaningful artifacts across skills, prompts, docs, CI, code, and shell scripts
- classify meaningful artifacts across skills, prompts, docs, CI, code, shell scripts, and tests
- generate a real `analysis-project` dossier instead of placeholder folders
- generate a real `clone-blueprint` repo skeleton with preservation guidance
- export a reusable `skill-pack`
- produce file-by-file analysis pages for meaningful artifacts
- extract workflow steps, trigger conditions, and decision gates
- extract prompt and skill semantics such as:
  - hard constraints
  - approval gates
  - review loops
  - escalation paths
  - reusable operating patterns
- analyze Python, JavaScript, and shell files with file-type-specific logic extraction
- reconstruct local architecture relationships from:
  - workflow command references
  - shell invocations
  - local JS imports/requires
  - local Python imports
  - explicit path references in docs, prompts, and skills
  - explicit validation links from tests to implementation artifacts
- generate architecture pages with:
  - meaningful subsystem summaries
  - entrypoints
  - relationship summaries
  - critical paths
- generate preservation matrices with:
  - role-aware decisions
  - strategy notes
  - legal-review flags
  - confidence labels
  - contract-vs-harness guidance for tests and fixtures
- generate reconstruction-oriented dossier pages with:
  - system-role framing
  - preserve/change boundaries
  - rebuild strategy guidance
  - suggested first implementation slices
- generate workflow pages with rebuild guidance instead of only extracted semantics
- generate dossier-level reconstruction plans that prioritize:
  - entrypoints
  - workflow layer recovery
  - architecture-guided build order
  - preservation-aware carryover rules
- generate connected-artifact sections in file dossiers that show:
  - what drives an artifact
  - what the artifact drives
  - what validates it
- synthesize repo-level workflow patterns across multiple artifacts, including:
  - guardrailed workflows
  - human approval gates
  - iterative review loops
  - human escalation paths
  - human-agent handoffs
- carry repo-level workflow patterns into the dossier and clone blueprint
- extract actionable prompt steps from prompt templates whose real instructions live inside fenced blocks
- expose validation-aware architecture output when tests or CI form explicit proof-of-correctness paths

In practical terms, it is already good for:
- understanding repos like `superpowers`
- locating the main operating rules of a prompt/skill system
- mapping executable glue between scripts, code, and workflows
- producing a starting blueprint for rebuilding the system with your own vision
- showing which artifacts should be differentiated, rewritten, preserved, or reviewed before reuse

It is not finished yet, but it is already beyond MVP scaffolding and can produce genuinely useful analysis outputs.

## V2 Domain Translation Status

V2 is now the current top-level capability.

The system can now move from:
- reconstruction system

to:
- reconstruction plus domain-translation system

This means it can analyze a source repo like `superpowers` and produce a target-aware rebuild contract for a new domain such as marketing.

Implemented v2 capabilities:
- doctrine extraction
- role-system and handoff extraction
- artifact equivalence mapping
- target-domain translation planning
- target-aware dossier sections
- target-aware blueprint docs and marketing scaffold placeholders

Design and implementation docs:
- `docs/specs/2026-03-12-domain-translation-v2-design.md`
- `docs/plans/2026-03-12-domain-translation-v2.md`

Current translation-mode CLI:

```bash
python -m deep_analysis.cli analyze \
  https://github.com/obra/superpowers.git \
  /tmp/superpowers-marketing \
  --export-skill-pack \
  --target-domain marketing \
  --vision-file tests/fixtures/marketing_vision.md
```

Translation-mode outputs:
- `analysis-project/10-doctrine/README.md`
- `analysis-project/11-role-system/README.md`
- `analysis-project/12-domain-translation/README.md`
- `analysis-project/13-artifact-equivalence/README.md`
- `clone-blueprint/docs/domain-translation-map.md`
- `clone-blueprint/docs/role-system.md`
- `clone-blueprint/docs/target-doctrine.md`
- `clone-blueprint/docs/marketing-capability-map.md`

Current recommendation after v2:
- deepen target-domain mapping quality for more domains beyond `marketing`
- improve role-to-capability translation so target blueprints feel less generic
- strengthen artifact-equivalence rules for large prompt libraries and multi-agent repo families

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
- file-type-specific code and script analysis for Python, JavaScript, and shell artifacts
- graph-backed architecture reconstruction from local references, workflow invocations, and script/code links
- cross-artifact architecture linking for docs, prompts, skills, tests, and implementation files
- semantic extraction for prompt and skill constraints, approval gates, loops, escalation paths, and reusable patterns
- prompt-template step extraction for fenced-block prompt bodies
- repo-level workflow pattern synthesis from repeated cross-file semantics
- richer preservation analysis with artifact roles, strategy notes, legal-review flags, and confidence labels
- test- and fixture-aware preservation guidance for verification contracts and harness material
- reconstruction-oriented dossier synthesis for artifact pages, workflow pages, and rebuild ordering
- validation-aware architecture output and reconstruction guidance

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

### 4. Code and script logic analysis deepened

Originally code and shell artifacts were summarized from their first line or first heading, which made the dossier read like indexing.

That is now improved with per-type structural analysis:
- Python files extract imports, classes, functions, and `__main__` entrypoints
- JavaScript files extract requires/imports, defined functions, export markers, and runtime startup cues
- shell scripts extract commands, environment-variable assumptions, runtime command flow, and operational side effects

This also includes a shell parsing fix discovered during smoke testing:
- ignore control-flow tokens like `while` and `case`
- ignore case labels like `--flag)`
- ignore shell terminators like `;;`
- prioritize real commands over shell builtins in the dossier

### 5. Architecture reconstruction deepened

Originally the architecture page mostly listed subsystem counts and entrypoints.

That is now improved with deterministic architecture reconstruction:
- cartography records local graph edges from workflow commands, shell invocations, and local JS imports
- architecture summaries now include relationship summaries
- architecture summaries now include critical paths
- executable scripts can be promoted into entrypoints when they clearly orchestrate runtime behavior
- component counts now reflect meaningful artifacts instead of raw repository noise

### 6. Prompt and skill semantic extraction deepened

Originally workflow pages mainly captured triggers, steps, and a shallow set of decision gates.

That is now improved with explicit semantic extraction:
- hard constraints
- approval gates
- review loops
- escalation paths
- reusable operating patterns

This also includes a semantic parsing fix discovered during smoke testing:
- ignore fenced code and diagram blocks during workflow semantic extraction
- keep DOT and code examples from polluting approval gates and review loops

### 7. Preservation analysis deepened

Originally preservation analysis mostly used three generic buckets with short rationales.

That is now improved with:
- role-aware artifact classification
- richer decision categories
- strategy notes for rebuild behavior
- legal-review workflow flags
- heuristic confidence labels
- a more actionable preservation matrix in the clone blueprint

Current decision vocabulary:
- `rewrite-with-differentiation`
- `rewrite-equivalent`
- `preserve-core-behavior`
- `preserve-verification-contract`
- `adapt-test-fixture`
- `preserve-with-review`

Important boundary:
- the system still does not provide legal advice
- the legal-review field is a workflow signal for cautious reuse, not a legal conclusion

### 11. Test and fixture preservation became smarter

Originally preservation analysis treated tests too much like production code and fixtures too much like ordinary support docs.

That is now improved with:
- `contract-bearing verification` as a separate preservation role for tests
- `test-support fixture` as a separate preservation role for fixtures and sample reference artifacts
- `preserve-verification-contract` for tests
- `adapt-test-fixture` for fixture material
- blueprint guidance that explicitly separates preserving assertions/contracts from preserving harness details

This matters because the blueprint now tells you:
- preserve what a test proves
- allow the rebuilt harness and assertion style to change
- adapt fixture content to the new system instead of carrying it over blindly

### 12. Prompt-template step extraction improved

Originally prompt pages became thin when the real prompt instructions lived inside fenced blocks.

That is now improved with prompt-aware fenced-block extraction:
- prompt files can read natural-language template content from fenced sections
- numbered steps inside prompt bodies are now extracted
- imperative prompt guidance becomes visible in the dossier
- non-prompt fenced-block filtering still protects skills/docs from diagram and code noise

This matters because prompt dossier pages now capture the actual operating instructions of prompt templates, not just the framing text around them.

### 13. Validation-aware architecture output added

Originally the architecture page only exposed one critical-path bucket, which mixed runtime and proof-of-correctness concerns.

That is now improved with:
- dedicated validation-path support in the architecture model
- a `Validation Paths` section in the dossier architecture page
- reconstruction guidance that references both runtime and validation flow

This matters because rebuild order can now account for how the system proves correctness, not just how it executes.

### 8. Dossier pages became reconstruction-oriented

Originally dossier pages were informative, but still mostly descriptive.

That is now improved with reconstruction-oriented synthesis:
- artifact pages explicitly describe system role
- artifact pages separate preserve-vs-change boundaries
- artifact pages provide a rebuild strategy instead of only a summary
- artifact pages propose a suggested first slice for implementation
- workflow pages include rebuild guidance tied to constraints, approvals, loops, and escalation behavior
- the reconstruction plan now starts from entrypoints, then workflow layer, then architecture-guided dependency order, then preservation enforcement

This matters because the dossier now answers:
- what this artifact does
- what must survive in the rebuild
- what is safe to rewrite
- how to rebuild it first
- what order to tackle the system in

### 9. Cross-artifact architecture links deepened

Originally the architecture graph was strongest for code and shell orchestration, but much weaker for docs, prompts, skills, and tests.

That is now improved with:
- first-class test artifact classification
- Python import linking for local modules
- explicit path-reference linking from docs, prompts, and skills
- markdown command linking to local scripts and code targets
- dossier connected-artifact sections showing incoming, outgoing, and validation relationships

This also includes a fixture-safety fix discovered during verification:
- ignore compiled files under `__pycache__/` so sample repo test fixtures do not get misclassified as real test artifacts

### 10. Repo-level workflow pattern synthesis added

Originally workflow analysis stopped at the individual file level, even when the same operating patterns repeated across the repo.

That is now improved with deterministic repo-level pattern synthesis:
- repeated hard-constraint behavior becomes `guardrailed workflow`
- repeated approval structures become `human approval gate`
- repeated review cycles become `iterative review loop`
- repeated escalation behavior becomes `human escalation path`
- repeated role separation becomes `human-agent handoff`

These patterns are now written into:
- `analysis-project/04-workflows-prompts-skills/repo-patterns.md`
- `clone-blueprint/docs/workflow-patterns.md`
- the dossier reconstruction plan

This matters because the system now captures the source repo's operating style, not just its individual workflow files.

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
- treat smoke-run output quality issues as real bugs, not just polish
- improve architecture pages only when the smoke-run output becomes materially more useful for reconstruction
- improve workflow pages only when extracted semantics reflect real operating rules rather than diagram noise
- keep preservation decisions explicit about uncertainty instead of pretending heuristics are legal certainty

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

Analyze the deeper code/script logic slice:

```bash
python -m deep_analysis.cli analyze "/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers" /tmp/superpowers-code-logic-20260312-v4 --export-skill-pack
```

Analyze the architecture reconstruction slice:

```bash
python -m deep_analysis.cli analyze "/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers" /tmp/superpowers-architecture-20260312-v2 --export-skill-pack
```

Analyze the prompt/skill semantics slice:

```bash
python -m deep_analysis.cli analyze "/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers" /tmp/superpowers-semantics-20260312-v2 --export-skill-pack
```

Analyze the preservation-analysis slice:

```bash
python -m deep_analysis.cli analyze "/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers" /tmp/superpowers-preservation-20260312 --export-skill-pack
```

Analyze the reconstruction-oriented dossier slice:

```bash
python -m deep_analysis.cli analyze "/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers" /tmp/superpowers-rebuild-dossiers-20260312 --export-skill-pack
```

Analyze the cross-artifact architecture-linking slice:

```bash
python -m deep_analysis.cli analyze "/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers" /tmp/superpowers-cross-links-20260312 --export-skill-pack
```

Analyze the repo-level workflow-pattern slice:

```bash
python -m deep_analysis.cli analyze "/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers" /tmp/superpowers-workflow-patterns-20260312 --export-skill-pack
```

Analyze the smarter test-and-fixture-preservation slice:

```bash
python -m deep_analysis.cli analyze "/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers" /tmp/superpowers-test-preservation-20260312 --export-skill-pack
```

Analyze the prompt-template step-extraction slice:

```bash
python -m deep_analysis.cli analyze "/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers" /tmp/superpowers-prompt-templates-20260312 --export-skill-pack
```

Analyze the final v1 slice:

```bash
python -m deep_analysis.cli analyze "/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers" /tmp/superpowers-v1-final-20260312 --export-skill-pack
```

## Fresh Verification Evidence

Most recent verified results:

- `pytest -q` -> `25 passed in 0.20s`
- local smoke run completed:
  `python -m deep_analysis.cli analyze "/Users/dmytrnewaimastery/Documents/Codex app projects/superpowers" /tmp/superpowers-v1-final-20260312 --export-skill-pack`
- remote smoke run completed:
  `python -m deep_analysis.cli analyze https://github.com/obra/superpowers.git /tmp/superpowers-deep-analysis-remote-20260311`

## Where The Generated Outputs Are

Primary local smoke-run outputs:

- `/tmp/superpowers-v1-final-20260312/analysis-project`
- `/tmp/superpowers-v1-final-20260312/clone-blueprint`
- `/tmp/superpowers-v1-final-20260312/skill-pack`

Useful example pages:

- `/tmp/superpowers-v1-final-20260312/analysis-project/05-architecture/README.md`
- `/tmp/superpowers-v1-final-20260312/analysis-project/04-workflows-prompts-skills/skills-subagent-driven-development-implementer-prompt-md.md`
- `/tmp/superpowers-v1-final-20260312/clone-blueprint/docs/preservation-matrix.md`

## Git State

Repo:
- `/Users/dmytrnewaimastery/Documents/Codex app projects/deep-analysis-system`

Branch:
- `codex/deep-analysis-system`

PR:
- `https://github.com/asdzxc1a/deep-analyse-/pull/1`

Latest pushed commit before this memory revision:
- `4ee296f` - `Extract steps from prompt templates`

There is one untracked local path left intentionally untouched:
- `.superpowers/`

## Resume After Restart

If you restart Codex and want to continue from this exact point, use this repo and this memory file first:

- repo: `/Users/dmytrnewaimastery/Documents/Codex app projects/deep-analysis-system`
- memory file: `MEMORY.md`

Recommended restart prompt:

```text
Open /Users/dmytrnewaimastery/Documents/Codex app projects/deep-analysis-system/MEMORY.md and continue from there.
```

If you want to resume the current development frontier specifically, use:

```text
Open /Users/dmytrnewaimastery/Documents/Codex app projects/deep-analysis-system/MEMORY.md, inspect the latest state, and continue with the next recommended stage.
```

Current status:
- v1 is complete and usable

Future enhancement frontier:
- improve repo-level pattern clustering beyond deterministic families

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
- dependencies extraction is better for code and shell files, but still not semantic dependency tracing
- architecture synthesis now reconstructs local graph edges, but it is still not a full call graph or semantic runtime model
- cross-artifact links are now stronger, but still mostly limited to explicit path, command, and import evidence
- workflow semantics are much stronger, but reusable pattern extraction is still label-based rather than cross-repo mining
- repo-level pattern synthesis is now useful, but it still groups by deterministic families rather than deeper semantic equivalence
- preservation decisions are much stronger, but still heuristic rather than truly license-aware or policy-aware
- test/fixture preservation is now clearer, but fixture detection is still path/name heuristic rather than semantic
- prompt-template extraction is stronger, but it still uses heuristics and may include some instructional noise from large prompt templates
- validation-aware architecture output is present, but some repos will still show `Validation Paths: None` when the graph lacks explicit proof chains
- dossier writing is now real, but not yet as deep as line-by-line architectural interpretation
- there is no long-lived memory or repo history database yet
- there is no interactive “rebuild with my vision” transformation engine yet

## Best Next Steps

If work resumes later for optional enhancement work, the strongest next slices are:

1. improve repo-level pattern clustering beyond deterministic families
2. refine fixture detection beyond path/name heuristics
3. reduce instructional noise in very large prompt templates
4. increase explicit validation-link discovery in repos whose tests don’t reference targets directly
5. consider language-specific parsers only if heuristics stop producing useful output

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
- `/tmp/superpowers-v1-final-20260312/analysis-project`

## One-Line Session Handoff

We designed and implemented the first real version of the deep-analysis system, upgraded it from scaffold outputs to actual dossier/workflow/blueprint generation, fixed the major classification bug discovered on a real `superpowers` smoke run, deepened code and script logic analysis, added graph-backed architecture reconstruction, deepened prompt and skill semantic extraction, upgraded preservation analysis with richer decision categories, strategy notes, legal-review flags, and confidence labels, made dossier pages reconstruction-oriented with preserve/change boundaries, rebuild strategy, suggested first slices, and architecture-aware rebuild ordering, deepened cross-artifact architecture links so docs, prompts, skills, and tests can participate in the system graph, added repo-level workflow pattern synthesis so repeated operating motifs are captured in the dossier and blueprint, made preservation guidance smarter for tests and fixtures so contracts and harness material are treated differently, improved prompt-template extraction so fenced prompt bodies contribute real operational steps to the dossier, added validation-aware architecture output and reconstruction guidance, verified it locally with 25 passing tests, and brought the repo to a coherent, usable v1 on the current PR branch.

## Marketing-Superpowers Worktree Status

There is now a separate feature worktree for the first vertical built on top of the deep-analysis-system research:

- worktree: `/Users/dmytrnewaimastery/.config/superpowers/worktrees/deep-analysis-system/codex-fashion-creator-growth-system`
- branch: `codex/fashion-creator-growth-system`

This worktree contains `marketing-superpowers/`, which is the first practical domain build that uses the reconstruction and translation work as a foundation.

Current status in that worktree:
- creator-growth vertical exists
- doctrine, six core skills, prompts, examples, and deterministic checks exist
- live strategy pack for the fashion creator account exists
- cold-audience concept board exists
- scripted shooting boards exist
- the 2-week production board now maps directly to scripted boards and shoot blocks

Most important files in the worktree:
- `marketing-superpowers/doctrine/fashion-creator-doctrine.md`
- `marketing-superpowers/strategy/live-fashion-creator-strategy-spec.md`
- `marketing-superpowers/strategy/account/creator-profile.md`
- `marketing-superpowers/strategy/account/content-pillars.md`
- `marketing-superpowers/strategy/account/series-library.md`
- `marketing-superpowers/strategy/account/platform-strategy.md`
- `marketing-superpowers/strategy/account/first-2-week-plan.md`
- `marketing-superpowers/strategy/account/cold-audience-concept-board-v1.md`
- `marketing-superpowers/strategy/account/production-board-weeks-1-2.md`
- `marketing-superpowers/strategy/account/scripted-shooting-boards-top-5.md`
- `marketing-superpowers/tests/run-skill-checks.sh`
- `marketing-superpowers/tests/run-strategy-pack-checks.sh`

Latest creator-system slice:
- `docs/specs/2026-03-12-scripted-shooting-boards-design.md`
- `docs/plans/2026-03-12-scripted-shooting-boards.md`

Verified commands in the worktree:

```bash
cd "/Users/dmytrnewaimastery/.config/superpowers/worktrees/deep-analysis-system/codex-fashion-creator-growth-system"
source .venv/bin/activate
pytest -q
bash marketing-superpowers/tests/run-skill-checks.sh
bash marketing-superpowers/tests/run-strategy-pack-checks.sh
```

Current best restart prompt for the creator work:

```text
Open /Users/dmytrnewaimastery/.config/superpowers/worktrees/deep-analysis-system/codex-fashion-creator-growth-system/MEMORY.md and continue from the marketing-superpowers worktree state.
```
