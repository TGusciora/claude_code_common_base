# Dev Docs Pattern

Documentation for the persistent dev docs methodology. Actual dev docs live at project root: `/dev_docs/`

---

## Directory Structure

```
PROJECT_ROOT/
├── dev_docs/              # <-- Active dev docs live here (project root)
│   ├── active/            # Work in progress
│   │   └── NNNN_task-name/
│   │       ├── NNNN_task-name-plan.md
│   │       ├── NNNN_task-name-context.md
│   │       └── NNNN_task-name-tasks.md
│   └── archive/           # Completed work
└── .claude/
    ├── dev_docs/
    │   └── README.md      # <-- This file (pattern documentation)
    └── scripts/
        └── next-task-number.sh  # Auto-numbering helper
```

---

## Naming Convention

Tasks are numbered sequentially across both `active/` and `archive/` directories:

```
NNNN_task-name
│    └─ kebab-case task description
└─ 4-digit zero-padded sequential number
```

**Examples:**
- `0001_initial-setup`
- `0002_auth-refactor`
- `0003_api-optimization`

**Get next number:**
```bash
.claude/scripts/next-task-number.sh
# Returns: 0001 (or next available number)
```

---

## Purpose

Maintain project context across Claude Code sessions and context resets.

**The Problem:** Context resets lose implementation decisions, progress, and why certain approaches were chosen.

**The Solution:** Three-file structure that captures everything needed to resume work.

---

## Three-File Structure

For each task, create in `dev_docs/active/NNNN_task-name/`:

### 1. NNNN_task-name-plan.md
Strategic implementation plan with phases, tasks, and acceptance criteria.

### 2. NNNN_task-name-context.md
Key information for resuming: SESSION PROGRESS, key files, decisions made, blockers.

### 3. NNNN_task-name-tasks.md
Checkbox checklist tracking progress through phases.

---

## When to Use

**Use for:**
- Complex multi-day tasks
- Tasks spanning multiple sessions
- Work requiring careful planning

**Skip for:**
- Simple bug fixes
- Single-file changes
- Trivial modifications

**Rule:** If it takes >2 hours or spans sessions, use dev docs.

---

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/dev-docs [task]` | Create new dev docs (auto-numbered) |
| `/dev-docs-update` | Update existing docs before context reset |

---

## Workflow

### Starting
```bash
# Get next number
NUM=$(.claude/scripts/next-task-number.sh)
mkdir -p dev_docs/active/${NUM}_task-name
```
Create the three files (-plan.md, -context.md, -tasks.md).

### During Work
- Update context.md frequently
- Check off tasks in tasks.md
- Refer to plan.md for strategy

### After Context Reset
Claude reads all three files and resumes where you left off.

### Completing
```bash
mv dev_docs/active/NNNN_task-name dev_docs/archive/
```

---

## Best Practices

1. **Update SESSION PROGRESS frequently** - not just at session end
2. **Make tasks actionable** - include file names, acceptance criteria
3. **Keep plan current** - update when scope changes

---

## Template: context.md

```markdown
# [Task Name] - Context

## SESSION PROGRESS (YYYY-MM-DD)

### Completed
- Item 1
- Item 2

### In Progress
- Current work

### Blockers
- Issues preventing progress

## Key Files
| File | Purpose |
|------|---------|
| path/to/file | Description |

## Quick Resume
1. Read this file
2. Continue with [specific action]
3. Check tasks.md for remaining work
```

---

## Template: tasks.md

```markdown
# [Task Name] - Tasks

## Phase 1: [Name]
- [x] Completed task
- [ ] Pending task
- [ ] Another task

## Phase 2: [Name]
- [ ] Task with acceptance criteria
```
