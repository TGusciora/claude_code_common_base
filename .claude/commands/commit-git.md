---
name: commit-git
description: Commit staged changes with conventional commit message and push to remote
argument-hint: Optional commit message override (leave empty for auto-generated suggestion)
---

Analyze all changes, create logical commits using Conventional Commits format, and optionally push.

## Workflow

### Step 1: Investigate Current State
Run these commands in parallel to understand all changes:

```bash
git status
git diff
git diff --staged
git log --oneline -10
```

Also list untracked files:
```bash
git ls-files --others --exclude-standard
```

### Step 2: Analyze and Group Changes
Review all changes (modified, staged, untracked) and determine logical groupings:

**Single commit if:**
- All changes relate to one feature/fix/task
- Changes are in related files (same module/component)
- Small scope (< 5-10 files with related changes)

**Multiple commits if:**
- Changes span unrelated features or fixes
- Mix of documentation, code, and config changes
- Independent bug fixes alongside new features
- Changes to different modules/components that are unrelated

### Step 3: Present Commit Plan
Present the proposed commit structure to user:

```
## Proposed Commits

### Commit 1: <type>(<scope>): <description>
Files:
- path/to/file1
- path/to/file2

### Commit 2: <type>(<scope>): <description>
Files:
- path/to/file3
```

Use AskUserQuestion tool with options:
- "Proceed with plan" - execute commits as proposed
- "Single commit" - combine all into one commit
- "Edit plan" - let user modify the grouping

### Step 4: Execute Commits
For each commit in the plan:

1. Stage the files for that commit:
```bash
git add <file1> <file2> ...
```

2. Create the commit:
```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <description>

[optional body if needed]

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

3. Verify success before proceeding to next commit

### Step 5: Ask About Push
After all commits are created, ask user:

Use AskUserQuestion tool:
- "Push to remote" - execute `git push`
- "Don't push" - leave commits local

If push requested:
```bash
git push
```

### Step 6: Report Summary
Show final summary:
- Number of commits created
- Commit hashes and messages
- Push status (pushed/local only)
- Any warnings or notes

## Conventional Commits Reference

**Format:**
```
<type>(<scope>): <description>
```

**Types:**
| Type | Usage |
|------|-------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring |
| `test` | Adding/updating tests |
| `chore` | Maintenance, dependencies |
| `perf` | Performance improvement |

## Grouping Heuristics

| Pattern | Suggested Split |
|---------|-----------------|
| `.md` files + code files | Separate `docs` and `feat`/`fix` commits |
| Config + implementation | Separate `chore` and `feat` commits |
| Multiple bug fixes | Separate `fix` commits per issue |
| Test + implementation | Can be single commit or split |
| New command + docs update | Single `feat` commit (related) |

## Rules
- Use imperative mood ("add" not "added")
- Keep first line under 72 characters
- Scope is optional but recommended
- Always include Claude co-author footer
- Never commit secrets or sensitive files
- Run pre-commit hooks (linting) automatically

## Error Handling
- If no changes: Inform user, nothing to commit
- If commit fails: Show error, stop execution
- If push fails: Note commits succeeded locally
- If pre-commit hook fails: Show linting errors, fix before retry
