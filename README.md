# Deep Analysis System

Analyze one GitHub repository at a time and produce:
- a reconstruction-grade dossier
- a clone blueprint repo
- an optional reusable analysis skill pack

The current implementation is optimized first for agent, skill, workflow, prompt, and automation repositories such as `obra/superpowers`.

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
- workflow extraction for skills, docs, and CI files
- preservation boundaries and reconstruction plan
