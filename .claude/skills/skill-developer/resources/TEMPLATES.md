# Skill Templates

Copy-paste templates for creating new skills. Choose the template that matches your needs.

## Basic Skill Template

Use for simple, focused skills under 300 lines.

```markdown
---
name: my-skill-name
description: Brief description including trigger keywords for topic1, topic2, topic3
---

# My Skill Title

## Purpose

[One paragraph explaining what problem this skill solves and who it helps.]

## When to Use This Skill

- [Scenario 1: When user is doing X]
- [Scenario 2: When user needs Y]
- [Scenario 3: When working with Z]

## Quick Reference

| Pattern | Example | Use When |
|---------|---------|----------|
| Pattern 1 | `code example` | Situation A |
| Pattern 2 | `code example` | Situation B |

## [Main Topic 1]

### Key Points

- Point 1
- Point 2
- Point 3

### Example

```language
// Code example with comments explaining key parts
```

## [Main Topic 2]

[Content...]

## Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Mistake 1 | What goes wrong | How to fix it |
| Mistake 2 | What goes wrong | How to fix it |
```

---

## Skill with Resources Template

Use for comprehensive skills that would exceed 400 lines.

```markdown
---
name: comprehensive-skill
description: Detailed guide for domain covering topic1, topic2, topic3, best practices, troubleshooting
---

# Comprehensive Skill Title

## Purpose

[One paragraph explaining the skill's purpose.]

## When to Use This Skill

- [Scenario 1]
- [Scenario 2]
- [Scenario 3]
- [Scenario 4]

## Quick Reference

### Key Commands

| Command | Description |
|---------|-------------|
| `cmd1` | What it does |
| `cmd2` | What it does |

### Key Patterns

```language
// Most common pattern users need
```

## Core Concepts

### Concept 1

[Summary in 2-3 paragraphs max]

> For detailed examples and edge cases, see [CONCEPT_ONE.md](resources/CONCEPT_ONE.md)

### Concept 2

[Summary in 2-3 paragraphs max]

> For detailed examples and edge cases, see [CONCEPT_TWO.md](resources/CONCEPT_TWO.md)

## Common Tasks

### Task 1: [Name]

1. Step one
2. Step two
3. Step three

### Task 2: [Name]

1. Step one
2. Step two
3. Step three

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Problem 1 | Why it happens | How to fix |
| Problem 2 | Why it happens | How to fix |

> For more troubleshooting, see [TROUBLESHOOTING.md](resources/TROUBLESHOOTING.md)

## Resource Files

| File | Content | When to Use |
|------|---------|-------------|
| [CONCEPT_ONE.md](resources/CONCEPT_ONE.md) | Detailed coverage of concept 1 | Deep dive needed |
| [CONCEPT_TWO.md](resources/CONCEPT_TWO.md) | Detailed coverage of concept 2 | Deep dive needed |
| [TROUBLESHOOTING.md](resources/TROUBLESHOOTING.md) | Extended problem-solving | Debugging |
```

---

## Guardrail Skill Template

Use for skills that enforce standards or prevent mistakes.

```markdown
---
name: my-guardrail
description: Enforces standards for [area] to prevent [problems]. Checks for [specific things].
---

# My Guardrail

## Purpose

Prevent [specific problem] by checking [what it checks] when [when it activates].

## What This Guardrail Checks

- [ ] Check 1: [What it verifies]
- [ ] Check 2: [What it verifies]
- [ ] Check 3: [What it verifies]

## Why These Rules Exist

### Rule 1: [Name]

**Prevents:** [What bad thing it prevents]

**Example of violation:**
```language
// Bad code that violates the rule
```

**Correct approach:**
```language
// Good code that follows the rule
```

### Rule 2: [Name]

[Same structure...]

## How to Comply

### Quick Checklist

Before committing, ensure:

- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

### Step-by-Step

1. [First thing to do]
2. [Second thing to do]
3. [Third thing to do]

## Bypassing This Guardrail

When necessary (and you understand the risks), you can bypass this guardrail:

### Option 1: File Marker

Add this comment to the file:
```language
// @skip-guardrail-name
```

### Option 2: Environment Variable

```bash
export SKIP_MY_GUARDRAIL=1
```

### Option 3: Acknowledge and Proceed

When prompted, explicitly acknowledge the warning and proceed.

> **Warning:** Only bypass when you understand the implications.
```

---

## skill-rules.json Entry Template

Add to `.claude/skills/skill-rules.json`:

```json
{
  "my-skill-name": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "medium",
    "description": "Same description as in SKILL.md frontmatter",
    "promptTriggers": {
      "keywords": [
        "specific keyword",
        "another keyword",
        "phrase trigger"
      ],
      "intentPatterns": [
        "(create|add|make).*?thing",
        "how.*?(to|do).*?something",
        "thing.*(pattern|example|guide)"
      ]
    },
    "fileTriggers": {
      "pathPatterns": [
        "src/domain/**/*.ts",
        "app/feature/**/*.tsx"
      ],
      "pathExclusions": [
        "**/*.test.ts",
        "**/*.spec.ts",
        "**/test/**"
      ],
      "contentPatterns": [
        "import.*from 'library'",
        "class.*extends.*Base"
      ]
    }
  }
}
```

### Guardrail Entry Template

```json
{
  "my-guardrail": {
    "type": "guardrail",
    "enforcement": "warn",
    "priority": "high",
    "description": "Enforces [rules] to prevent [problems]",
    "promptTriggers": {
      "keywords": ["security", "validation"]
    },
    "fileTriggers": {
      "pathPatterns": ["src/**/*.ts"],
      "contentPatterns": ["pattern-to-check"]
    },
    "skipConditions": {
      "fileMarkers": ["@skip-my-guardrail"],
      "envOverride": "SKIP_MY_GUARDRAIL"
    },
    "blockMessage": "Warning: [Issue detected]. [How to resolve]. Add @skip-my-guardrail to bypass."
  }
}
```

---

## Resource File Template

Use for resource files in the `resources/` directory:

```markdown
# [Topic Name]

Detailed coverage of [topic] for the [parent skill name] skill.

## Overview

[1-2 paragraphs introducing the topic and its importance]

## [Section 1]

### [Subsection]

[Detailed content with examples]

```language
// Example code
```

### [Subsection]

[More content...]

## [Section 2]

[Content...]

## Examples

### Example 1: [Scenario Name]

**Context:** [When you would use this]

```language
// Full, working example
```

**Key Points:**
- Point 1
- Point 2

### Example 2: [Scenario Name]

[Same structure...]

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Issue 1 | Why | Fix |
| Issue 2 | Why | Fix |

## See Also

- [Related Resource](RELATED.md)
- [Main Skill](../SKILL.md)
```

---

## Slash Command Template

Create in `.claude/commands/`:

```markdown
Activate the [skill-name] skill to help with [task].

Read the skill file at `.claude/skills/[skill-name]/SKILL.md` and apply its guidance.

If the user is:
- [Doing X]: Guide them through [process]
- [Doing Y]: Help with [task]
- [Asking about Z]: Explain [concepts]

Always reference resource files when deeper guidance is needed:
- `.claude/skills/[skill-name]/resources/[RESOURCE1].md`
- `.claude/skills/[skill-name]/resources/[RESOURCE2].md`
```

---

## Quick Start Checklist

When creating a new skill:

1. [ ] Choose appropriate template (basic, comprehensive, guardrail)
2. [ ] Fill in frontmatter with name and description
3. [ ] Write Purpose and When to Use sections
4. [ ] Add Quick Reference section
5. [ ] Write main content with examples
6. [ ] Create resource files if needed (comprehensive template)
7. [ ] Add entry to skill-rules.json
8. [ ] Test keyword triggers
9. [ ] Test intent pattern triggers
10. [ ] Test file triggers
11. [ ] Verify no false positives
12. [ ] Check line count (under 500 for SKILL.md)

---

## Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Skill directory | kebab-case | `my-skill-name` |
| Main file | SKILL.md | `SKILL.md` |
| Resource files | UPPERCASE_SNAKE.md | `BEST_PRACTICES.md` |
| Commands | kebab-case.md | `skill-dev.md` |
| Rules file | skill-rules.json | `skill-rules.json` |
