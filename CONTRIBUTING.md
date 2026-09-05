# Contributing to ECHO

ECHO is research software for sequential experiment selection. Keep changes small, testable, and honest about results.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Use `python -m echo` or `echolab`. The Unix command `echo` is a shell builtin.

## What belongs here

- Policies, worlds, metrics, and evaluation that do not leak ground truth to the agent
- Reports and tables filled from `summary.json`, never invented by hand
- Tests for new acquisition, environments, or evaluation paths
- Plugin examples (`examples/`) that register a world or a score and can be imported by `--plugin`

Do not add LLM agents, unpublished numerical claims, or a manuscript draft with a title page and abstract.

## Pull requests

1. Branch from `main` (or the active feature branch you were asked to use).
2. Run `pytest` before you push.
3. Point reviewers at the config, the `results/*/summary.json`, and the report if the change is experimental.
4. If you add a world or acquisition, register it in a plugin file and add a test that the name appears in `python -m echo list`.
