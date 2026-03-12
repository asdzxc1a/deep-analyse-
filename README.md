# Deep Analysis System

Analyze one GitHub repository at a time and produce:
- a reconstruction-grade dossier
- a clone blueprint repo
- an optional reusable analysis skill pack

## Local setup

```bash
cd "/Users/dmytrnewaimastery/Documents/Codex app projects/deep-analysis-system"
/Users/dmytrnewaimastery/.homebrew/Cellar/python@3.12/3.12.13/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```
