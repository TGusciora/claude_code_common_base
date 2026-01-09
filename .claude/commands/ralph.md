---
description: Start the Ralph self-continuing agent for dev_docs tasks
argument-hint: [iterations|--dry-run|--status|--cleanup]
---

Ralph is a test-driven, self-continuing agent that automates work on `dev_docs/active/` tasks through an iterative loop.

## Quick Start (Terminal Required)

**IMPORTANT: Run Ralph from terminal, not IDE (VS Code/Cursor)**

The shell script uses `--dangerously-skip-permissions` which is required for Ralph's autonomous operation. When run from IDE, Claude Code uses `.claude/settings.json` which has permission restrictions that interrupt Ralph's workflow.

```bash
# Open a terminal and run:
.claude/scripts/ralph/ralph.sh

# Run with custom iterations
.claude/scripts/ralph/ralph.sh 10
```

## Key Features

### Test-First Development
Ralph follows a strict test-first approach:
1. **Define** - Business goals and acceptance criteria
2. **Test** - Write tests before implementation
3. **Implement** - Write code to pass tests
4. **Verify & Fix** - Run tests, fix failures, repeat until green

### Smart Task Selection
Ralph can select multiple tasks per iteration based on:
- **Priority** - Highest priority first
- **Expertise** - Tasks matching his strengths
- **Logical grouping** - Related tasks done together
- **Complexity** - Balance scope with completion

| Selection | When Used |
|-----------|-----------|
| 1 task | Complex, deep focus needed |
| 2-3 tasks | Simple, related items |
| 1 phase | Tightly coupled tasks |
| 2 phases | Small, sequential phases |

### Test Failure Handling
Ralph **fixes test failures and continues** - he doesn't stop!

```
TEST FAILS → ANALYZE → FIX → RE-TEST → (repeat until green)
```

- Reads error messages and stack traces
- Fixes the implementation (not the test)
- Re-runs until all tests pass
- Only stops after 3+ failed fix attempts on same issue

### Git Worktree Isolation

```
PROJECT ROOT                         WORKTREE (inside project)
    |                                    |
    |                               worktrees/ralph-worktree-0001/
    |                                    |
main branch                      ralph/0001_task-name branch
-----------                      --------------------------
    |                                    |
Protected from                    All changes here:
Ralph's changes                   - File edits
    |                             - Tests written
    |                             - Bug fixes
    |                             - Commits
    |                                    |
    +-------- MERGE WHEN READY ----------+
                  (you review)
```

## Commands (Run from Terminal)

All commands must be run from a **terminal** (not IDE) to ensure `--dangerously-skip-permissions` is used:

```bash
# Run Ralph (default 20 iterations)
.claude/scripts/ralph/ralph.sh

# Run with specific iterations
.claude/scripts/ralph/ralph.sh 10

# Dry run - preview what would happen
.claude/scripts/ralph/ralph.sh --dry-run

# Check current status
.claude/scripts/ralph/ralph.sh --status

# Cleanup worktree and branch
.claude/scripts/ralph/ralph.sh --cleanup
```

## After Ralph Completes

When Ralph outputs `<ralph>ALL_TASKS_DONE</ralph>`:

```bash
# Review changes on the branch
git log main..ralph/NNNN_task-name
git diff main..ralph/NNNN_task-name

# Review test results
cd worktrees/ralph-worktree-NNNN && pytest

# If happy, merge to main
git checkout main
git merge ralph/NNNN_task-name

# Or create a PR for code review
gh pr create --base main --head ralph/NNNN_task-name

# Clean up
git worktree remove worktrees/ralph-worktree-NNNN
git branch -D ralph/NNNN_task-name
```

## Ralph's Workflow

### 1. Startup Checklist
- Verify worktree location (`worktrees/ralph-worktree-NNNN/`)
- Confirm on feature branch (`ralph/NNNN_task-name`)
- Read progress file and task docs
- Run baseline tests

### 2. Task Selection
- Review all incomplete `[ ]` items
- Select optimal batch based on priority/expertise/grouping
- Declare selection and rationale

### 3. Test-First Cycle (per task)
```
DEFINE → TEST → IMPLEMENT → VERIFY & FIX
```
- Define business goals and acceptance criteria
- Write tests that initially FAIL
- Implement to make tests PASS
- If tests fail: **FIX and re-run** (don't stop!)

### 4. Document & Commit
- Update tasks.md (mark `[x]`)
- Update context.md (session progress)
- Append to ralph_progress.txt
- Commit with conventional message

## Safety Features

1. **Worktree Isolation**: All changes on feature branch in `worktrees/`
2. **Path-Restricted Tools**: Write/Edit only in worktree directory
3. **Safety Hooks Active**: safety_validator.py blocks dangerous ops
4. **Iteration Limit**: Maximum 20 iterations (configurable)
5. **Test-Driven**: Tasks only complete when tests pass

## Progress Tracking

Ralph tracks progress in `dev_docs/active/NNNN_task/ralph_progress.txt`:

```json
{
  "timestamp": "...",
  "session": "...",
  "items_selected": 3,
  "items_completed": 3,
  "tests_written": 5,
  "tests_passed": 5,
  "regression_passed": true,
  "commit": "abc1234"
}
```

## Completion Markers

| Marker | Meaning |
|--------|---------|
| `<ralph>TASK_ITEM_DONE</ralph>` | Selected tasks done, more remain |
| `<ralph>ALL_TASKS_DONE</ralph>` | All tasks complete, ready for merge |
| `<ralph>ERROR_STOP</ralph>` | Truly unrecoverable error (NOT for test failures!) |

## Troubleshooting

**No active tasks found**
Create a task first: `/dev-docs`

**Test failures**
Ralph automatically attempts to fix them. Check progress file for fix history.

**ERROR_STOP marker**
Only used for truly unrecoverable issues:
- External dependencies unavailable
- Permission errors that can't be resolved
- After 3+ failed fix attempts on same issue

**Permission errors / Ralph stops for approval**
If Ralph keeps stopping to ask for permission, you're likely running from IDE instead of terminal.
- **Solution**: Run `.claude/scripts/ralph/ralph.sh` from a terminal window
- The shell script uses `--dangerously-skip-permissions` for autonomous operation
- IDE environments (VS Code, Cursor) use `.claude/settings.json` which has permission restrictions
- Safety hooks (`safety_validator.py`) still run to block dangerous operations

**Worktree conflicts**
Clean up with: `.claude/scripts/ralph/ralph.sh --cleanup`

## Prerequisites

- Active task in `dev_docs/active/` (create with `/dev-docs`)
- Task must have three-file structure:
  - `*-plan.md`
  - `*-context.md`
  - `*-tasks.md` (with `[ ]` checkboxes)

## Configuration

- **Default iterations**: 20
- **Worktree location**: `worktrees/ralph-worktree-NNNN/`
- **Branch naming**: `ralph/NNNN_task-name`
- **Progress file**: Per-task at `dev_docs/active/NNNN_task/ralph_progress.txt`
