# Hooks Configuration Guide

This guide explains how to configure and customize the hooks system.

## Current Configuration

The hooks are configured in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "_description": "Safety gate: blocks destructive bash commands",
        "matcher": "Bash|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/safety_validator.py"
          }
        ]
      },
      {
        "_description": "Block sensitive files with detailed error message",
        "matcher": "Read|Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(jq -r '.tool_input.file_path // empty'); echo \"$FILE\" | grep -qE '(\\.env|secrets|credentials)' && { echo \"BLOCKED: Access denied to sensitive file: $FILE\" >&2; exit 2; } || exit 0"
          }
        ]
      },
      {
        "_description": "Audit trail: logs all PreToolUse events",
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/audit_logger.py"
          }
        ]
      },
      {
        "_description": "Skill validator: soft enforcement warnings for skill files",
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/skill-validator.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "_description": "Auto-format files after Write/Edit (Ruff for Python, Prettier for JS/TS)",
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/auto-format.sh"
          }
        ]
      },
      {
        "_description": "Audit trail: logs all PostToolUse events",
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/audit_logger.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "_description": "Notification sound",
        "hooks": [
          {
            "type": "command",
            "command": "for i in 1 2; do afplay /System/Library/Sounds/Funk.aiff; done"
          }
        ]
      },
      {
        "_description": "Audit trail: logs all Stop events",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/audit_logger.py"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "_description": "Skill suggester: analyzes prompts to suggest relevant skills",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/skill-suggester.py"
          }
        ]
      },
      {
        "_description": "Audit trail: logs all user prompt submissions",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/audit_logger.py"
          }
        ]
      }
    ]
  }
}
```

---

## Hook Customization

### skill-suggester.py

**Customize skill detection** by editing `.claude/skills/skill-rules.json`:

```json
{
  "skills": {
    "my-skill": {
      "type": "domain",
      "enforcement": "suggest",
      "priority": "high",
      "description": "What this skill does",
      "promptTriggers": {
        "keywords": ["keyword1", "keyword2"],
        "intentPatterns": ["regex.*pattern"]
      },
      "fileTriggers": {
        "pathPatterns": ["**/*.py"],
        "pathExclusions": ["**/.venv/**"]
      }
    }
  }
}
```

**Priority levels:**
- `critical` - Always show first, marked as required
- `high` - Recommended skills
- `medium` - Suggested skills
- `low` - Optional skills

---

### safety_validator.py

**Add blocked patterns** by editing the script:

```python
DANGEROUS_PATTERNS = [
    r"rm\s+-rf\s+/",
    r"rm\s+-rf\s+~",
    # Add your patterns here
]

SENSITIVE_FILES = [
    ".env",
    "id_rsa",
    # Add your patterns here
]
```

---

### auto-format.sh

**Customize formatters** by editing the script:

```bash
# For Python files
if [[ "$file" == *.py ]]; then
    ruff format "$file" 2>/dev/null
fi

# For JS/TS files
if [[ "$file" == *.js || "$file" == *.ts || "$file" == *.tsx ]]; then
    npx prettier --write "$file" 2>/dev/null
fi
```

---

### audit_logger.py

**Change log location:**

```python
# Default: .claude/audit_logs/YYYYMMDD_audit.jsonl
LOG_DIR = Path(__file__).parent.parent / "audit_logs"

# Custom location:
LOG_DIR = Path("/var/log/claude-audit")
```

---

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `CLAUDE_PROJECT_DIR` | Project root directory | Auto-detected |
| `SKIP_AUDIT_LOG` | Disable audit logging | Not set |

---

## Hook Execution Order

Hooks run in the order specified in `settings.json`:

**PreToolUse order:**
1. safety_validator.py (can block)
2. sensitive file blocker (can block)
3. audit_logger.py (logs)
4. skill-validator.py (warns)

**PostToolUse order:**
1. auto-format.sh (formats)
2. audit_logger.py (logs)

---

## Selective Hook Enabling

### Minimal Setup (Skill Suggestion Only)

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "_description": "Skill suggester",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/skill-suggester.py"
          }
        ]
      }
    ]
  }
}
```

### Safety Only (No Formatting)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "_description": "Safety gate",
        "matcher": "Bash|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/safety_validator.py"
          }
        ]
      }
    ]
  }
}
```

---

## Troubleshooting

### Hook Not Executing

1. **Check registration:** Verify hook is in `.claude/settings.json`
2. **Check permissions:** Run `chmod +x .claude/hooks/*.py .claude/hooks/*.sh`
3. **Check syntax:** Run `python3 -m py_compile .claude/hooks/hook.py`

### Hook Blocking Unexpectedly

1. **Check exit codes:**
   - `0` = Allow
   - `2` = Block
2. **Add debug output:** `echo "DEBUG: $variable" >&2`
3. **Check stderr:** Hook messages go to stderr

### Performance Issues

1. **Audit logging:** Disable with `SKIP_AUDIT_LOG=1`
2. **Formatting:** Remove auto-format.sh from PostToolUse
3. **Skill matching:** Reduce patterns in skill-rules.json

---

## Adding New Hooks

### Python Hook Template

```python
#!/usr/bin/env python3
"""My custom hook."""

import json
import sys

def main() -> None:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # Your logic here
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Exit 0 = allow, Exit 2 = block
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Shell Hook Template

```bash
#!/bin/bash
set -e

# Read JSON input
INPUT=$(cat)

# Parse with jq
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Your logic here

# Exit 0 = allow, Exit 2 = block
exit 0
```

---

## See Also

- [README.md](./README.md) - Hooks overview
- [../skills/skill-rules.json](../skills/skill-rules.json) - Skill trigger configuration
- [../settings.json](../settings.json) - Full settings reference
