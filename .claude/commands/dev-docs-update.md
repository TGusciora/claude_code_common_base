---
name: dev-docs-update
description: Update dev documentation before context compaction
argument-hint: Optional - specific context or tasks to focus on (leave empty for comprehensive update)
---

We're approaching context limits. Please update the development documentation to ensure seamless continuation after context reset.

## CRITICAL: Preserve History, Update Status

**NEVER delete existing context, progress, or task history from dev_docs files.**

When updating dev_docs:
1. **PRESERVE all existing context and progress entries** - they represent session history
2. **APPEND new context/progress** at the top of history sections with timestamps
3. **UPDATE task statuses freely** - mark `[x]`, `[~]`, change priorities, reorder
4. **For deferred tasks**: Update status to "Deferred" with reason, don't delete
5. **For cancelled tasks**: Use strikethrough `~~task~~` and add note "Decided to remove: [reason]"
6. **UPDATE status fields** (Last Updated, Status) at the top

**What you CAN do:**
- Update task checkboxes and statuses
- Reorder/reprioritize tasks
- Add new tasks anywhere
- Strikethrough cancelled items (with reason)

**What you CANNOT do:**
- Delete previous session progress entries
- Delete context/decisions from earlier sessions
- Remove tasks without marking them cancelled with reason

## Required Updates

### 1. Update Active Task Documentation
For each task in `dev_docs/active/`:

**Update `[task-name]-context.md`**:
- APPEND a new "Session Progress" section with timestamp at the TOP of session history
- Include: current state, decisions made, files modified, blockers, next steps
- Update "Last Updated" timestamp at document top
- DO NOT delete previous session progress entries

**Update `[task-name]-tasks.md`**:
- Mark completed tasks as `[x]` (change `[ ]` to `[x]`)
- Mark in-progress tasks as `[~]`
- Add new tasks/phases as needed
- Reorder/reprioritize tasks as needed
- For deferred tasks: add "(Deferred: reason)" and move to backlog section
- For cancelled tasks: use `~~strikethrough~~` with "(Cancelled: reason)"
- Update completion summary and notes sections
- Update "Last Updated" and "Status" at document top

### 2. Capture Session Context
APPEND to context file any relevant information about:
- Complex problems solved
- Architectural decisions made
- Tricky bugs found and fixed
- Integration points discovered
- Testing approaches used
- Performance optimizations made

### 3. Update Memory (if applicable)
- Store any new patterns or solutions in project memory/documentation
- Update entity relationships discovered
- Add observations about system behavior

### 4. Document Unfinished Work
APPEND notes about:
- What was being worked on when context limit approached
- Exact state of any partially completed features
- Commands that need to be run on restart
- Any temporary workarounds that need permanent fixes

### 5. Create Handoff Notes
If switching to a new conversation, APPEND:
- Exact file and line being edited
- The goal of current changes
- Any uncommitted changes that need attention
- Test commands to verify work

## Additional Context: $ARGUMENTS

**Priority**: Focus on capturing information that would be hard to rediscover or reconstruct from code alone.

## Examples

### Adding a New Phase
```markdown
## Existing phases stay here...

## Phase G: New Issues (2026-01-31)
- [ ] Task item 1
- [ ] Task item 2
```

### Cancelling a Task (with reason)
```markdown
- ~~[ ] Implement feature X~~ (Cancelled: superseded by new approach in Phase G)
```

### Deferring a Task
```markdown
- [ ] Nice-to-have optimization (Deferred: not blocking MVP, revisit post-launch)
```

### Session Progress (append at top)
```markdown
## Session Progress

### 2026-01-31 14:30 - Session 12
- Completed: A.1, A.2
- In progress: B.1
- Blocked: C.1 (waiting for API spec)

### 2026-01-30 10:00 - Session 11  ← Previous entry stays
- Completed: Initial setup
```
