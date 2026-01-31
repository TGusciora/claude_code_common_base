---
name: continue-dev
description: Continue implementing tasks from dev_docs/active with extended thinking
argument-hint: [optional task number to override auto-selection, e.g., "0002"]
---

Resume work on active development tasks using extended thinking mode.

## Workflow

### Step 1: Find Active Task
Scan for task folders in `dev_docs/active/`:

```bash
ls -1 dev_docs/active/ | grep -E '^[0-9]{4}_' | sort | head -1
```

If `$ARGUMENTS` contains a task number, use that instead of auto-selection.

If no active tasks found, inform user:
> No active tasks in `dev_docs/active/`. Use `/dev-docs` to create a new task.

### Step 2: Read Task Documentation
Read ALL three files in the task folder:

1. `NNNN_task-name-plan.md` - Understand the strategic plan and phases
2. `NNNN_task-name-context.md` - Review current state, key files, decisions
3. `NNNN_task-name-tasks.md` - Identify incomplete tasks (not marked `[x]`)

**CRITICAL:** Take time to thoroughly understand the full context before proceeding.

### Step 2.5: Pre-Implementation Check

Before implementing, verify prerequisites exist:

1. **Backend tasks**: Check router/route registered in main application entry point
2. **Frontend CSS tasks**: Verify CSS variables exist in theme/variables file
3. **New pages**: Identify parent page needing navigation link

If prerequisites missing, create them FIRST or document as blocker in context.md.

### Step 3: Apply Extended Thinking
Before implementing, engage in deep analysis:

1. **Understand the goal** - What is this task trying to achieve?
2. **Review progress** - What has been completed? What's in progress?
3. **Identify blockers** - Are there any issues noted in context.md?
4. **Plan next steps** - Which incomplete task should be tackled first?
5. **Consider dependencies** - Are there prerequisites or related files?

### Step 4: Follow Guidelines
Always adhere to:

- **CLAUDE.md** (root) - Core principles, testing, checkpoint protocol
- **.claude/repo_specific/CLAUDE.md** - Project-specific guidelines (if exists)
- **KISS, YAGNI, SOLID** - Simplest solution, only what's needed, clean design

### Step 5: Implement
Work through incomplete tasks in order:

1. Mark current task as in-progress in tasks.md
2. Implement the task following the plan
3. Run tests after changes
4. Mark task complete when done
5. Update context.md with progress

### Step 6: Update Documentation
As you work, keep dev docs current:

### Step 6.5: Runtime Verification (REQUIRED)

Before marking ANY task complete:

1. Start the dev server
2. Navigate to feature in browser
3. Check DevTools console for errors
4. Take screenshot of working feature
5. Store screenshot in `dev_docs/active/NNNN_task/`

**Task is NOT complete until runtime verification passes.**

Use `[~]` for in-progress tasks, `[x]` only after browser verification.

**context.md updates:**
- SESSION PROGRESS section with today's date
- Key decisions made
- Files modified
- Any new blockers discovered

**tasks.md updates:**
- Mark completed tasks: `- [x] Task description`
- Add new discovered tasks if needed
- Note in-progress work

### Step 7: Checkpoint Protocol
Follow CLAUDE.md checkpoint rules - always ask before:
- Architectural decisions
- Adding/removing dependencies
- Deleting or significantly refactoring code
- Modifying configuration files

## Error Handling

- If task folder structure is incomplete, note missing files and continue with available docs
- If blocked, update context.md with blocker details and ask user for guidance
- If tests fail, fix issues before marking task complete

## Quick Resume
After context reset, run `/continue` to pick up exactly where you left off.
