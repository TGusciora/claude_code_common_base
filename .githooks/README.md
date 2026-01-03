# Git Hooks

Version-controlled git hooks for this repository.

## Setup

Run once after cloning:

```bash
git config core.hooksPath .githooks
```

## Hooks

| Hook | Purpose |
|------|---------|
| `pre-commit` | Runs ruff format and check on staged Python files |

## Pre-commit Behavior

1. Auto-formats Python files with `ruff format`
2. Auto-fixes linting issues with `ruff check --fix`
3. Re-stages auto-fixed files
4. Blocks commit if unfixable errors remain

## Requirements

- [ruff](https://docs.astral.sh/ruff/) must be installed
