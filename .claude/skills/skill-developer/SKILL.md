---
name: skill-developer
description: Expert guide for creating Claude Code skills. Covers skill architecture, SKILL.md structure, hook integration, trigger patterns, best practices, anti-patterns, and first principles (KISS, YAGNI, DRY).
---

# Skill Developer

## Purpose

Guide Claude in creating well-architected, maintainable Claude Code skills that follow first principles and avoid common pitfalls. This meta-skill helps you build skills that are:

- **Focused**: One skill = one domain/problem area
- **Maintainable**: Clear structure, progressive disclosure
- **Reliable**: Multiple trigger types, no single points of failure
- **Effective**: Activates when needed, stays quiet when not

## When to Use This Skill

- Creating a new skill from scratch
- Reviewing or improving existing skills
- Debugging skill activation issues
- Writing or updating skill-rules.json configuration
- Understanding skill architecture patterns
- Learning first principles of skill design

## Quick Reference

### Skill File Anatomy

| Section | Required | Purpose |
|---------|----------|---------|
| YAML Frontmatter | Yes | `name` and `description` for identification |
| Purpose | Yes | Why this skill exists (1-2 paragraphs) |
| When to Use | Yes | Activation scenarios (bullet list) |
| Quick Reference | Recommended | Key info for fast lookup |
| Core Content | Yes | Main guidance, examples, patterns |
| Resource Files | If >400 lines | Links to detailed resources |

### The 500-Line Rule

Main skill files stay under 500 lines. Details live in resource files.

**Why?**
- Claude loads main skill first, resources on-demand
- Focused content improves comprehension
- Easier to maintain and update

**When to split:**
- SKILL.md exceeds 400 lines
- A section could stand alone
- Content changes at different rates

### Trigger Types

| Type | Matches | Use When |
|------|---------|----------|
| `keywords` | Exact substring in prompt | User explicitly mentions topic |
| `intentPatterns` | Regex against prompt | User implies intent without keywords |
| `pathPatterns` | Glob against file paths | File context indicates domain |
| `contentPatterns` | Regex against file content | Code patterns indicate domain |

### Enforcement Levels

| Level | Behavior | Use For |
|-------|----------|---------|
| `suggest` | Advisory, never blocks | Domain skills, guidance |
| `warn` | Warning message, doesn't block | Soft guardrails |
| `block` | Prevents action until resolved | Critical safety rules |

## Core Concepts

### First Principles Foundation

Every skill should embody these principles:

**KISS (Keep It Simple, Stupid)**
- One skill = one domain/problem area
- If you can't explain it in one sentence, split it
- Prefer shallow hierarchies over deep nesting

**YAGNI (You Aren't Gonna Need It)**
- Start minimal, expand based on real needs
- Don't add "just in case" guidance
- Delete unused content immediately

**DRY (Don't Repeat Yourself)**
- Cross-reference instead of duplicating
- Use shared resource files for common patterns
- Exception: Critical safety info CAN be repeated

**Single Responsibility**
- One trigger pattern = one activation reason
- Resource files should be independently useful
- Avoid "god skills" that try to do everything

> For detailed coverage, see [FIRST_PRINCIPLES.md](resources/FIRST_PRINCIPLES.md)

### Avoiding Single Points of Failure

Don't put everything in SKILL.md. Distribute across:

```
skill-name/
├── SKILL.md           # Entry point, <500 lines
└── resources/
    ├── TOPIC_ONE.md   # Deep dive on topic
    └── TOPIC_TWO.md   # Deep dive on topic
```

Use multiple trigger types:
- Keywords alone miss context-based opportunities
- Path patterns alone miss prompt-based requests
- Combine for resilience

> For architectural patterns, see [SKILL_ARCHITECTURE.md](resources/SKILL_ARCHITECTURE.md)

## Creating a New Skill

### Step 1: Define the Problem

Before writing, answer:

- [ ] What specific problem does this skill solve?
- [ ] Who is the target user?
- [ ] When should this skill activate?
- [ ] When should it NOT activate?
- [ ] What existing skills might overlap?

### Step 2: Choose the Skill Type

| Type | When to Use | Enforcement |
|------|-------------|-------------|
| `domain` | Technology/area expertise | `suggest` |
| `guardrail` | Standards enforcement | `warn` or `block` |
| `workflow` | Multi-step processes | `suggest` |

### Step 3: Design the Structure

**Small skill (<300 lines):**
```
skill-name/
└── SKILL.md
```

**Comprehensive skill (300-500 lines with depth):**
```
skill-name/
├── SKILL.md
└── resources/
    ├── DETAILED_TOPIC.md
    └── EXAMPLES.md
```

### Step 4: Write the SKILL.md

Start with the template:

```markdown
---
name: my-skill-name
description: Brief description including trigger keywords
---

# My Skill Title

## Purpose
[One paragraph: What problem does this skill solve?]

## When to Use This Skill
- [Scenario 1]
- [Scenario 2]

## Quick Reference
[Table or bullets of key info]

## [Main Content Sections]
[Your guidance here]

## Resource Files (if applicable)
| File | Purpose |
|------|---------|
| RESOURCE.md | Description |
```

### Step 5: Configure Triggers

Add entry to `.claude/skills/skill-rules.json`:

```json
{
  "my-skill-name": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "medium",
    "description": "Same as SKILL.md description",
    "promptTriggers": {
      "keywords": ["keyword1", "keyword2"],
      "intentPatterns": ["(create|add).*?thing"]
    },
    "fileTriggers": {
      "pathPatterns": ["src/feature/**/*.ts"],
      "pathExclusions": ["**/*.test.ts"]
    }
  }
}
```

### Step 6: Test Activation

1. **Keyword test**: Use trigger keywords in a prompt
2. **Intent test**: Describe intent without keywords
3. **File test**: Open matching files, ask related questions
4. **Negative test**: Verify no false positives

## Common Tasks

### Adding a Resource File

1. Create file in `resources/` directory
2. Use UPPERCASE_SNAKE.md naming
3. Add reference in SKILL.md Resource Files table
4. Cross-link from relevant sections

### Debugging Activation Issues

**Skill never activates:**
- Check keywords are in skill-rules.json
- Verify regex patterns are valid
- Test patterns at regex101.com
- Check pathPatterns match actual file paths

**Skill activates too often:**
- Make keywords more specific
- Add pathExclusions for irrelevant files
- Narrow intentPatterns regex

**Skill conflicts with another:**
- Check priority settings
- Make triggers more specific
- Consider merging related skills

### Reviewing a Skill

Use this checklist:

- [ ] SKILL.md under 500 lines?
- [ ] Has Purpose section?
- [ ] Has When to Use section?
- [ ] All resource files referenced?
- [ ] Triggers configured in skill-rules.json?
- [ ] Keywords are specific enough?
- [ ] Examples are minimal but complete?
- [ ] No orphan resource files?

> For detailed best practices, see [BEST_PRACTICES.md](resources/BEST_PRACTICES.md)
> For common mistakes, see [ANTI_PATTERNS.md](resources/ANTI_PATTERNS.md)

## Skill Types Reference

### Domain Skills

Skills representing technology or domain expertise.

**Characteristics:**
- Type: `domain`
- Enforcement: `suggest`
- Provide guidance, examples, patterns
- Never block operations

**Examples:**
- backend-dev-guidelines
- frontend-dev-guidelines
- database-patterns

### Guardrail Skills

Skills enforcing standards or preventing mistakes.

**Characteristics:**
- Type: `guardrail`
- Enforcement: `warn` or `block`
- Check code against rules
- Provide escape hatches

**Examples:**
- security-standards
- code-review-checklist
- api-conventions

### Workflow Skills

Skills guiding multi-step processes.

**Characteristics:**
- Type: `workflow`
- Enforcement: `suggest`
- Step-by-step guidance
- Decision trees

**Examples:**
- skill-developer (this skill)
- deployment-guide
- incident-response

## Hook Integration

Skills can be enhanced with hooks for automation.

### UserPromptSubmit Hook

Suggests relevant skills based on prompt content.

```python
# Reads skill-rules.json
# Matches prompt against triggers
# Outputs suggestion to stdout
# Always exits 0 (advisory only)
```

### PreToolUse Hook

Validates operations and warns about issues.

```python
# Intercepts Write/Edit to skill files
# Checks structure and content
# Outputs warnings to stderr
# Always exits 0 (soft enforcement)
```

> For hook implementation details, see the hooks in `.claude/hooks/`

## Resource Files

| File | Content | When to Reference |
|------|---------|-------------------|
| [FIRST_PRINCIPLES.md](resources/FIRST_PRINCIPLES.md) | KISS, YAGNI, DRY, SRP | Architecture decisions |
| [SKILL_ARCHITECTURE.md](resources/SKILL_ARCHITECTURE.md) | Structural patterns, SPOF avoidance | Designing skill structure |
| [BEST_PRACTICES.md](resources/BEST_PRACTICES.md) | Guidelines and examples | Writing skill content |
| [ANTI_PATTERNS.md](resources/ANTI_PATTERNS.md) | Common mistakes to avoid | Review and debugging |
| [TEMPLATES.md](resources/TEMPLATES.md) | Starter templates | Creating new skills |

## Quick Commands

| Command | Purpose |
|---------|---------|
| `/skill-dev` | Invoke this skill manually |

## Related Files

- `.claude/skills/skill-rules.json` - Trigger configuration
- `.claude/hooks/skill-suggester.py` - Auto-suggestion hook
- `.claude/hooks/skill-validator.py` - Validation hook
- `.claude/commands/skill-dev.md` - Slash command definition
