# Hooks

Claude Code hooks for skill activation, safety validation, formatting, and audit logging.

---

## What Are Hooks?

Hooks are scripts that run at specific points in Claude's workflow:
- **UserPromptSubmit**: When user submits a prompt
- **PreToolUse**: Before a tool executes
- **PostToolUse**: After a tool completes
- **Stop**: When Claude stops responding

**Key insight:** Hooks can modify prompts, block actions, and track state.

---

## Current Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `skill-suggester.py` | UserPromptSubmit | Suggests relevant skills based on prompt |
| `safety_validator.py` | PreToolUse | Blocks destructive commands |
| `skill-validator.py` | PreToolUse | Validates skill file structure |
| `auto-format.sh` | PostToolUse | Auto-formats Python/JS/TS files |
| `audit_logger.py` | All events | Logs all actions for audit trail |

---

## Hook Details

### skill-suggester.py (UserPromptSubmit)

**Purpose:** Automatically suggests relevant skills based on user prompts and file context.

**How it works:**
1. Reads `.claude/skills/skill-rules.json`
2. Matches prompt against keywords and intent patterns
3. Matches file paths against path patterns
4. Groups matches by priority (critical, high, medium, low)
5. Outputs all matching skills in a visual block

**Output example:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SKILL ACTIVATION CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

>> RECOMMENDED SKILLS:
   -> /python-dev (keyword: python)

ACTION: Use slash command to activate skill
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### safety_validator.py (PreToolUse)

**Purpose:** Blocks destructive bash commands and sensitive file modifications.

**Blocks:**
- `rm -rf /`, `rm -rf ~`, `rm -rf *`
- Modifications to `.env`, `id_rsa`, `credentials` files
- Other dangerous patterns

**Exit codes:**
- `0` - Allow
- `2` - Block with message

---

### skill-validator.py (PreToolUse)

**Purpose:** Validates skill files follow correct structure.

**Checks:**
- YAML frontmatter (name, description)
- Required sections (Purpose, When to Use)
- File length limits
- Resource file references

**Enforcement:** Soft (warns but doesn't block)

---

### auto-format.sh (PostToolUse)

**Purpose:** Auto-formats files after Write/Edit operations.

**Formatters:**
- Python: `ruff format`
- JS/TS: `prettier` (if available)

**Runs on:** Files matching `*.py`, `*.js`, `*.ts`, `*.tsx`

---

### audit_logger.py (All Events)

**Purpose:** Logs all Claude actions for audit trail.

**Log location:** `.claude/audit_logs/YYYYMMDD_audit.jsonl`

**Logged events:**
- PreToolUse (tool name, inputs)
- PostToolUse (tool name, success/failure)
- UserPromptSubmit (prompt text)
- Stop (session end)

---

## Configuration

All hooks are configured in `.claude/settings.json`. See [CONFIG.md](./CONFIG.md) for customization options.

---

## Adding New Hooks

1. Create script in `.claude/hooks/`
2. Make executable: `chmod +x script.py`
3. Add to `.claude/settings.json` under appropriate event
4. Include `_description` for documentation

Example:
```json
{
  "_description": "My custom hook: does something useful",
  "matcher": "Write|Edit",
  "hooks": [
    {
      "type": "command",
      "command": ".claude/hooks/my-hook.py"
    }
  ]
}
```
