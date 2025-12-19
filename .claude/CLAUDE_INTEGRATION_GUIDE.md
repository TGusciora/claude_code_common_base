# Claude Integration Guide

**FOR CLAUDE CODE:** When a user asks you to integrate components from this repository into their project, follow these instructions carefully.

---

## Overview

This repository contains Claude Code infrastructure components. Your role is to:

1. **Ask clarifying questions** about their project structure
2. **Copy the appropriate files**
3. **Customize configurations** for their setup
4. **Verify the integration** works correctly

**Key Principle:** ALWAYS ask before assuming project structure. What works for one project won't work for another.

---

## Repository Structure

### Folder Tree

```
.claude/
├── settings.json              # Claude Code settings (hooks, permissions, model)
├── CLAUDE_INTEGRATION_GUIDE.md # This file - integration instructions for Claude
│
├── agents/                    # Specialized AI agents for complex tasks
├── audit_logs/                # Operation audit logs (auto-generated)
├── commands/                  # Slash commands (/command-name)
├── dev_docs/                  # Development documentation templates
├── hooks/                     # Event-triggered automation scripts
├── repo_specific/             # Project-specific Claude guidelines
└── skills/                    # Contextual knowledge modules
```

### File Reference

#### Root Files

| File | Purpose |
|------|---------|
| `settings.json` | Master config: hooks, permissions, model preferences, deny patterns |
| `CLAUDE_INTEGRATION_GUIDE.md` | This guide - tells Claude how to integrate components |

#### `/agents/` - Specialized Task Agents

Standalone agents for complex, multi-step tasks. Copy as-is, no config needed.

| Agent | Purpose |
|-------|---------|
| `api-tester.md` | API endpoint testing and validation |
| `code-architecture-reviewer.md` | Reviews codebase architecture and suggests improvements |
| `code-refactor-master.md` | Performs systematic code refactoring |
| `dependency-analyzer.md` | Analyzes and audits project dependencies |
| `documentation-architect.md` | Creates comprehensive documentation |
| `error-debugger.md` | Debugs errors with systematic approach |
| `performance-profiler.md` | Identifies performance bottlenecks |
| `plan-reviewer.md` | Reviews implementation plans |
| `refactor-planner.md` | Plans refactoring strategies |
| `test-writer.md` | Writes comprehensive test suites |
| `web-research-specialist.md` | Conducts web research with citations |

#### `/hooks/` - Event-Triggered Automation

Scripts triggered by Claude Code events. Require `chmod +x` and settings.json config.

| Hook | Event | Purpose |
|------|-------|---------|
| `safety_validator.py` | PreToolUse | Blocks destructive commands (rm -rf, DROP, etc.) |
| `skill-suggester.py` | UserPromptSubmit | Suggests relevant skills based on prompt |
| `skill-validator.py` | PreToolUse | Validates skill file structure on edit |
| `auto-format.sh` | PostToolUse | Auto-formats code after edits (Ruff/Prettier) |
| `audit_logger.py` | All events | Logs all operations to audit_logs/ |
| `notification-sound.sh` | PostToolUse | Plays sound on task completion |

#### `/commands/` - Slash Commands

Custom slash commands invoked via `/command-name`.

| Command | Purpose |
|---------|---------|
| `dev-docs.md` | Creates dev_docs structure for new tasks |
| `dev-docs-update.md` | Updates existing dev_docs with progress |
| `python-dev.md` | Activates Python development guidelines |
| `skill-dev.md` | Activates skill development mode |

#### `/skills/` - Knowledge Modules

Contextual skills auto-activated by file patterns or keywords.

| Skill | Tech Requirements | Purpose |
|-------|------------------|---------|
| `skill-developer/` | None (meta) | Teaches how to create new skills |
| `python-dev/` | Python 3.10+, pytest, Ruff | Python backend development best practices |

**Skill Structure:**
```
skills/
├── skill-rules.json           # Activation rules (paths, keywords)
├── README.md                  # Skills documentation
└── [skill-name]/
    ├── SKILL.md               # Main skill instructions
    └── resources/             # Supporting reference docs
        ├── PATTERNS.md
        ├── ANTI_PATTERNS.md
        └── ...
```

#### `/repo_specific/` - Project Guidelines

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project-specific architecture, tech stack, conventions |

#### `/dev_docs/` - Task Documentation

| File | Purpose |
|------|---------|
| `README.md` | Template for active/archive task documentation |

#### `/audit_logs/` - Operation Logs

Auto-generated JSONL files tracking Claude operations (created by `audit_logger.py` hook).

---

## Tech Stack Compatibility Check

**CRITICAL:** Before integrating a skill, verify the user's tech stack matches the skill requirements.

### Backend Skills

**python-dev requires:**
- Python 3.10+
- pytest for testing
- Type hints
- Ruff for formatting/linting

**Before integrating, ask:**
"Do you use Python for backend development?"

**If NO:**
```
The python-dev skill is designed specifically for Python. I can:
1. Help you create a similar skill adapted for [their stack] using this as a template
2. Extract the framework-agnostic patterns (TDD, SOLID principles, etc.)
3. Skip this skill if not relevant

Which would you prefer?
```

### Frontend Skills (Future)

**When adding frontend skills, ask:**
"Do you use React for frontend?" "What component library?"

### Skills That Are Tech-Agnostic

These work for ANY tech stack:
- **skill-developer** - Meta-skill, no tech requirements

---

## General Integration Pattern

When user says: **"Add [component] to my project"**

1. Identify component type (skill/hook/agent/command)
2. **CHECK TECH STACK COMPATIBILITY**
3. Ask about their project structure
4. Copy files OR adapt for their stack
5. Customize for their setup
6. Verify integration
7. Provide next steps

---

## Integrating Skills

### Step-by-Step Process

**When user requests a skill**:

#### 1. Understand Their Project

**ASK THESE QUESTIONS:**
- "What's your project structure? Single app, monorepo, or multi-service?"
- "Where is your [backend/frontend] code located?"
- "What frameworks/technologies do you use?"

#### 2. Copy the Skill

```bash
cp -r .claude/skills/[skill-name] TARGET_PROJECT/.claude/skills/
```

#### 3. Handle skill-rules.json

**Check if it exists:**
```bash
ls TARGET_PROJECT/.claude/skills/skill-rules.json
```

**If NO (doesn't exist):**
- Copy the template
- Remove skills user doesn't want
- Customize for their project

**If YES (exists):**
- Read their current skill-rules.json
- Add the new skill entry
- Merge carefully to avoid breaking existing skills

#### 4. Customize Path Patterns

**CRITICAL:** Update `pathPatterns` in skill-rules.json to match THEIR structure:

**Example - User has monorepo:**
```json
{
  "python-dev": {
    "fileTriggers": {
      "pathPatterns": [
        "packages/api/src/**/*.py",
        "services/*/src/**/*.py"
      ]
    }
  }
}
```

**Example - User has single backend:**
```json
{
  "python-dev": {
    "fileTriggers": {
      "pathPatterns": [
        "src/**/*.py",
        "backend/**/*.py"
      ]
    }
  }
}
```

#### 5. Verify Integration

```bash
# Check skill was copied
ls -la TARGET_PROJECT/.claude/skills/[skill-name]

# Validate skill-rules.json syntax
cat TARGET_PROJECT/.claude/skills/skill-rules.json | jq .
```

**Tell user:** "Try editing a file in [their-path] and the skill should activate."

---

### Skill-Specific Notes

#### python-dev
- **Tech Requirements:** Python 3.10+, pytest, type hints, Ruff
- **Ask:** "Do you use Python?" "Where's your Python code?"
- **Customize:** pathPatterns for their src directory
- **Example paths:** `src/`, `backend/`, `api/`, `services/*/`

#### skill-developer
- **Tech Requirements:** None!
- **Copy as-is** - meta-skill, fully generic, teaches skill creation for ANY tech stack

---

## Adapting Skills for Different Tech Stacks

When user's tech stack differs from skill requirements:

### Option 1: Adapt Existing Skill (Recommended)

**When to use:** User wants similar guidelines but for different tech

**Process:**
1. Copy the skill as a starting point
2. Identify what needs changing (framework-specific code)
3. Keep what transfers (principles, patterns)
4. Replace examples systematically
5. Update skill name and triggers

### Option 2: Extract Framework-Agnostic Patterns

**When to use:** Stacks are very different, but core principles apply

The following always transfer:
- **Architecture:** Layered architecture, separation of concerns
- **Practices:** Error handling, testing strategies, SOLID principles
- **Organization:** File structure patterns

### What Usually Transfers Across Tech Stacks

**Always Transfer:**
- Layered architecture patterns
- Separation of concerns
- File organization strategies
- Testing strategies
- SOLID principles
- Performance optimization principles

**Framework-Specific (Don't Transfer):**
- Import statements
- ORM syntax
- Framework middleware patterns
- Routing implementations

---

## Integrating Hooks

### Current Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `safety_validator.py` | PreToolUse | Blocks destructive commands |
| `skill-suggester.py` | UserPromptSubmit | Suggests relevant skills |
| `skill-validator.py` | PreToolUse | Validates skill file structure |
| `auto-format.sh` | PostToolUse | Auto-formats files |
| `audit_logger.py` | All events | Logs operations |

### Adding Hooks to settings.json

**NEVER copy settings.json directly!**

Instead, **extract and merge** the sections they need:

1. Read their existing settings.json
2. Add the hook configurations they want
3. Preserve their existing config

**Example merge:**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
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

---

## Integrating Agents

**Agents are STANDALONE** - easiest to integrate!

### Standard Agent Integration

```bash
cp .claude/agents/[agent-name].md TARGET_PROJECT/.claude/agents/
```

**That's it!** Agents work immediately, no configuration needed.

### Check for Hardcoded Paths

Some agents may reference paths. **Before copying, read the agent file and check for:**
- Hardcoded project paths
- Screenshot paths
- Service URLs

**All current agents are generic** - copy as-is.

---

## Integrating Slash Commands

```bash
cp .claude/commands/[command].md TARGET_PROJECT/.claude/commands/
```

### Customize Paths

Commands may reference dev docs paths. **Check and update:**

**dev-docs and dev-docs-update:**
- Look for `dev_docs/active/` path references
- Ask: "Where do you want dev documentation stored?"
- Update paths in the command files

---

## Common Patterns & Best Practices

### Pattern: Asking About Project Structure

**DON'T assume:**
- "I'll add this for your api service"
- "Configuring for your backend directory"

**DO ask:**
- "What's your project structure? Monorepo or single app?"
- "Where is your backend code located?"
- "Do you use workspaces or have multiple services?"

### Pattern: Customizing skill-rules.json

**User has monorepo with workspaces:**
```json
{
  "pathPatterns": [
    "packages/*/src/**/*.py",
    "apps/*/src/**/*.py"
  ]
}
```

**User has simple structure:**
```json
{
  "pathPatterns": [
    "src/**/*.py",
    "backend/**/*.py"
  ]
}
```

---

## Verification Checklist

After integration, **verify these items:**

```bash
# 1. Hooks are executable
ls -la .claude/hooks/*.sh .claude/hooks/*.py
# Should show: -rwxr-xr-x

# 2. skill-rules.json is valid JSON
cat .claude/skills/skill-rules.json | jq .
# Should parse without errors

# 3. Settings.json is valid JSON
cat .claude/settings.json | jq .
# Should parse without errors

# 4. Python hooks have dependencies
python3 -c "import json, sys, re"
# Should not error
```

**Then ask user to test:**
- "Try editing a file in [relevant-path] - the skill should activate"
- "Try asking me a question about [topic] - I should suggest the skill"

---

## Common Mistakes to Avoid

### DON'T: Copy settings.json as-is
**Why:** May reference non-existent paths or services
**DO:** Extract only the sections they need

### DON'T: Keep example paths
**Why:** User's paths are different
**DO:** Ask about their actual structure and update

### DON'T: Skip making hooks executable
**Why:** Hooks won't run without execute permission
**DO:** Always `chmod +x` after copying

### DON'T: Assume monorepo structure
**Why:** Most projects are single-service
**DO:** Ask first, then customize

### DON'T: Add all skills at once
**Why:** Overwhelming and may not all be relevant
**DO:** Ask which skills are relevant to their work

---

## Example Integration Conversations

### Example 1: Adding Python Skill

**User:** "Add the python-dev skill to my project"

**Claude should respond:**
```
I'll add the python-dev skill. First, I need to understand your project:

1. Where is your Python code located? (e.g., src/, backend/, api/)
2. Do you use pytest for testing?
3. Is this a monorepo or single application?
```

**User:** "Code is in src/, yes we use pytest, single app"

**Claude should:**
1. Copy the skill directory
2. Update skill-rules.json with pathPattern: `"src/**/*.py"`
3. Verify it's copied correctly
4. Respond:
```
Added python-dev skill!

Configuration:
- Skill triggers when editing .py files in src/
- Activated by keywords like "python", "pytest", "tdd"

Try it: Edit a Python file and you should see the skill suggestion.
```

### Example 2: Tech Stack Mismatch

**User:** "Add the python-dev skill to my Node.js project"

**Claude should:**
```
The python-dev skill is designed for Python development. Since you're using Node.js, I have options:

Option 1 (Recommended): Create a node-dev skill using python-dev as a template:
- Keep: TDD practices, SOLID principles, file organization
- Adapt: Testing framework (Jest instead of pytest), linting (ESLint instead of Ruff)

Option 2: Extract only the framework-agnostic patterns for your reference.

Option 3: Skip this skill.

Which would you prefer?
```

---

## Quick Reference Tables

### What Needs Customization?

| Component | Tech Requirements | Customization | What to Ask |
|-----------|------------------|--------------|-------------|
| **skill-developer** | None | None | Copy as-is |
| **python-dev** | Python/pytest | Paths | "Use Python?" "Where's src?" |
| **safety_validator** | None | None | Copy as-is |
| **skill-suggester** | None | None | Copy as-is |
| **auto-format** | Ruff/Prettier | None | Works if tools installed |
| **All agents** | Minimal | Check paths | Copy as-is |
| **All commands** | Paths | dev_docs path | "Where for dev docs?" |

### When to Recommend Skipping

| Component | Skip If... |
|-----------|-----------|
| **python-dev** | Not using Python |
| **auto-format** | Don't have Ruff/Prettier installed |

---

## Final Tips for Claude

**When user says "add everything":**
- Start with essentials: skill-suggester hook + relevant skill
- Don't overwhelm them with all components
- Ask what they actually need

**When something doesn't work:**
- Check verification checklist
- Verify paths match their structure
- Test hooks manually
- Check for JSON syntax errors

**When user is unsure:**
- Recommend starting with skill-suggester hook
- Add python-dev skill (if using Python)
- Add more later as needed

**Always explain what you're doing:**
- Show the commands you're running
- Explain why you're asking questions
- Provide clear next steps after integration

---

**Remember:** Your job is to help users integrate components for THEIR specific project structure.
