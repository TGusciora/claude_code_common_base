# CLAUDE.md - Universal Guidelines

> **Project-specific info:** See [.claude/repo_specific/CLAUDE.md](.claude/repo_specific/CLAUDE.md)

---

## 10x Delivery Mindset (TOP PRIORITY)

Before starting ANY task, ask yourself:

### 1. Seek 10x Leverage
- **What needs to be done to deliver this task 10x faster AND 10x better?**
- What tools, technology, or way of working should I embrace?
- What automation, scripts, or existing solutions can I leverage?
- Can I use parallel execution, background agents, or batch operations?
- Is there a library, MCP tool, or skill that solves this already?

### 2. Gather Information for Success
- **Define the task well before executing** - understand requirements fully
- Plan for **logging and observability** from the start
- Install/enable debugging tools, browser devtools, or monitoring addons
- If you need API keys or secrets and can't read `.env`:
  - Ask user to provide the specific values needed
  - Or test using `.env.example` with overrides
- Read relevant code, schemas, and tests before making changes

### 3. Prove Business Value
- **Every action must have verifiable impact** through logs and tests
- Write tests FIRST to prove the implementation works
- Add logging to confirm expected behavior in runtime
- If you can't verify it works, it doesn't count as done
- Prepare verification steps that maximize confidence per Claude action
- Show evidence: test output, log snippets, screenshots, or curl responses

---

## Core Principles

## Everything in local Repo
- maintain changes and scripts in local repository
- first address changes in local .claude/settings.json
- first make changes/add scripts in local .claude/ folders

### KISS (Keep It Simple, Stupid)
- Choose the simplest solution that works
- One function = one responsibility
- If it's hard to explain, it's too complex

### YAGNI (You Aren't Gonna Need It)
- Only implement what's needed NOW
- No speculative features or "just in case" code
- Delete unused code immediately - don't comment it out

### SOLID
- **S**ingle Responsibility: One reason to change per class/module
- **O**pen/Closed: Extend behavior without modifying existing code
- **L**iskov Substitution: Subtypes must be substitutable for base types
- **I**nterface Segregation: Many specific interfaces > one general interface
- **D**ependency Inversion: Depend on abstractions, not concretions

---

## Testing Guidelines

### Atomic Tests
- One test = one behavior/scenario
- Test name format: `test_<function>_<scenario>_<expected_result>`
- Each test must be independent and isolated
- No shared mutable state between tests

### Test Workflow
1. Write test BEFORE implementation (TDD preferred)
2. Run existing tests before making changes
3. Run all tests after changes
4. Never commit with failing tests

---

## Checkpoint Protocol (STRICT)

### ALWAYS ask user before:
- Any architectural decision
- Adding/removing dependencies
- Deleting or significantly refactoring code
- Modifying configuration files
- Creating new directories or major files
- Any action that cannot be easily undone

### Summarize progress:
- After completing each logical unit of work
- Before moving to next task
- When encountering blockers or decisions

---

## Task Management

Tasks are numbered sequentially (`0001_`, `0002_`, etc.) for chronological tracking.

### Starting Large Tasks
```bash
# Get next sequential number
NUM=$(.claude/scripts/next-task-number.sh)
mkdir -p dev_docs/active/${NUM}_task-name/
```

Create three files:
- `NNNN_task-name-plan.md` - Accepted implementation plan
- `NNNN_task-name-context.md` - Key files, decisions, dependencies
- `NNNN_task-name-tasks.md` - Checklist with [ ] and [x] markers

### Continuing Tasks
1. Check `dev_docs/active/` for existing work
2. Read ALL three files before proceeding
3. Update "Last Updated" timestamp in context file
4. Mark tasks complete IMMEDIATELY when done

### Completing Tasks
- Move directory to `dev_docs/archive/` when done
- Add completion summary to context file

> See [.claude/dev_docs/README.md](.claude/dev_docs/README.md) for detailed dev docs pattern documentation.

---

## Repo-Specific Guidelines

**Primary:** [.claude/repo_specific/CLAUDE.md](.claude/repo_specific/CLAUDE.md) - Project overview, architecture, setup

**Additional CLAUDE.md files** (create as needed):
- `src/CLAUDE.md` - Source code conventions
- `tests/CLAUDE.md` - Testing patterns and fixtures
- `docs/CLAUDE.md` - Documentation standards

---

## Python Standards

- Type hints required on all functions
- Format with Ruff (`ruff format` and `ruff check`)
- Virtual environment required (`.venv/`)
- Testing with pytest
- Dependencies in `requirements.txt` or `pyproject.toml`

---

## Git Commits

Use **Conventional Commits** format for all commit messages.

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Usage |
|------|-------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring, no feature change |
| `test` | Adding/updating tests |
| `chore` | Maintenance, dependencies, config |
| `perf` | Performance improvement |

### Examples

```
feat(api): add user authentication endpoint
fix(frontend): resolve null pointer in dashboard
docs(readme): update installation instructions
chore(deps): upgrade fastapi to 0.109.0
refactor(services): extract validation logic to separate module
```

### Rules

- Use imperative mood ("add" not "added")
- Keep first line under 72 characters
- Scope is optional but recommended
- Reference issues in footer: `Closes #123`

---

## Quick Reference

| Action | Ask First? |
|--------|-----------|
| Read files | No |
| Small edits (<10 lines) | No |
| New functions/classes | Yes |
| New dependencies | Yes |
| Delete code | Yes |
| Architectural changes | Yes |
| Configuration changes | Yes |
