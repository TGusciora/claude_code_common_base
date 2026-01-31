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

## Coding Guidelines

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

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

### Task Completion Rule

A task is **NOT complete** until ALL of the following are verified:

1. ✅ All unit tests pass
2. ✅ Feature accessible in running app (not just in tests)
3. ✅ No console errors in browser DevTools
4. ✅ Integration Verification Checklist completed in tasks.md
5. ✅ Screenshot evidence stored in dev_docs folder (if UI task)

**Markers:**
- Use `[~]` for in-progress tasks
- Use `[x]` only after runtime verification passes

**Why:** Tests alone don't prove integration. A task with passing tests can still have missing router registration, undefined CSS variables, or orphaned pages that only appear at runtime.

---

## Context Management (Auto-Handoff)

Claude Code has limited context window. When approaching limits, proactively save state to enable seamless resume.

### Monitor Context Usage
- Run `/context` periodically during long sessions to check usage percentage
- Watch for context warnings in statusline (if enabled)
- At **60-70% usage**, begin proactive handoff

### At 60-70% Context Usage - PROACTIVE HANDOFF

**CRITICAL:** Before compaction triggers automatically, save your work:

1. **Update dev_docs** - Run `/dev-docs-update` or manually update:
   - `NNNN-context.md`: Add session progress section with timestamp
   - `NNNN-tasks.md`: Mark `[x]` completed items, `[~]` in-progress

2. **Use this session progress template** in context.md:
   ```markdown
   ## Session Progress - YYYY-MM-DD HH:MM

   ### Completed This Session
   - [List of completed work]

   ### Files Modified
   - [List of changed files with brief description]

   ### Key Decisions Made
   - [Important architectural or implementation decisions]

   ### Next Steps (Resume Here)
   - [Immediate next actions - be specific]

   ### Blockers/Notes
   - [Any issues or important context for next session]
   ```

3. **Recommend clear to user**: "Context at X%. Recommend `/clear` and `/continue-dev` to resume with fresh context."

### Resume After Context Reset
- Use `/continue-dev` - it reads all task files and resumes work seamlessly
- Check for `.last_session` marker in task directory for session end info
- Continue from "Next Steps" in last session progress entry

### Why This Matters
- **Compaction is lossy** - Claude forgets files and may repeat corrected mistakes
- **External state files are better** - dev_docs survive context resets perfectly
- **"Compound, don't compact"** - Save to files, clear completely, resume with full signal

---

## Repo-Specific Guidelines

**Primary:** [.claude/repo_specific/CLAUDE.md](.claude/repo_specific/CLAUDE.md) - Project overview, architecture, setup

**Additional CLAUDE.md files** (create as needed):
- `src/CLAUDE.md` - Source code conventions
- `tests/CLAUDE.md` - Testing patterns and fixtures
- `docs/CLAUDE.md` - Documentation standards

---

## .claude/ Directory Structure

| Directory | Purpose |
|-----------|---------|
| `agents/` | Custom subagent definitions (code-reviewer, error-debugger, test-writer, etc.) |
| `commands/` | Slash commands (`/commit`, `/dev-docs`, `/discovery`, `/ralph`) |
| `skills/` | Skill definitions (python-dev, k8s-dev, frontend-design, vue/react-best-practices) |
| `hooks/` | Pre/post hook configurations for tool calls |
| `scripts/` | Helper scripts (discovery_agent, ralph, next-task-number) |
| `repo_specific/` | Project-specific docs and conventions |
| `dev_docs/` | Dev docs templates and README |
| `plans/` | Auto-generated plan files (gitignored) |
| `audit_logs/` | Session audit logs (gitignored) |

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
