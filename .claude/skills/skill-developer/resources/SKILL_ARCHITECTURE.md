# Skill Architecture Patterns

This document covers structural patterns for organizing skills, avoiding single points of failure, and making architectural decisions.

## Core Components

### 1. SKILL.md (Required)

The entry point for every skill. Must include:

| Section | Required | Purpose |
|---------|----------|---------|
| YAML Frontmatter | Yes | `name` and `description` fields |
| Purpose | Yes | Why this skill exists |
| When to Use | Yes | Activation scenarios |
| Quick Reference | Recommended | Key info for fast lookup |
| Core Content | Yes | Main guidance |
| Resource Files | If using | Links to detailed resources |

**Frontmatter Format:**
```yaml
---
name: skill-name-in-kebab-case
description: Concise description including trigger keywords for topic1, topic2, topic3
---
```

**Description Guidelines:**
- Under 1024 characters
- Include words users would use to search
- Front-load the most important keywords
- Use natural language, not keyword stuffing

### 2. Resources Directory (Optional)

For skills exceeding 400 lines or needing deep dives.

```
skill-name/
├── SKILL.md              # Entry point
└── resources/
    ├── TOPIC_ONE.md      # Deep dive
    ├── TOPIC_TWO.md      # Deep dive
    └── EXAMPLES.md       # Extended examples
```

**Resource File Naming:**
- Use UPPERCASE_SNAKE_CASE.md
- Name should describe content
- Keep names short but descriptive

### 3. skill-rules.json Entry (Required for Auto-Activation)

Configures when skill activates without explicit invocation.

```json
{
  "skill-name": {
    "type": "domain|guardrail|workflow",
    "enforcement": "suggest|warn|block",
    "priority": "low|medium|high|critical",
    "description": "Same as SKILL.md description",
    "promptTriggers": { ... },
    "fileTriggers": { ... }
  }
}
```

## Avoiding Single Points of Failure

### Problem: Monolithic SKILL.md

If all content lives in one file:
- File corruption loses everything
- Large files are hard to maintain
- Changes to one topic affect the whole file
- Merge conflicts become common

### Solution: Distributed Architecture

```
skill-name/
├── SKILL.md              # Overview, quick reference, links
└── resources/
    ├── CORE_CONCEPTS.md  # Foundational knowledge
    ├── PATTERNS.md       # Reusable patterns
    ├── EXAMPLES.md       # Extended examples
    └── TROUBLESHOOTING.md # Problem-solving
```

**Benefits:**
- Each file can be updated independently
- Partial failures don't lose everything
- Easier to review and maintain
- Better git history per topic

### Problem: Single Trigger Type

Relying only on keywords means:
- Missing context-based opportunities
- No file-aware activation
- Brittle to wording changes

### Solution: Multi-Trigger Strategy

```json
{
  "skill-name": {
    "promptTriggers": {
      "keywords": ["explicit", "terms"],
      "intentPatterns": ["(implicit|inferred).*?patterns"]
    },
    "fileTriggers": {
      "pathPatterns": ["src/domain/**/*.ts"],
      "contentPatterns": ["import.*DomainLib"]
    }
  }
}
```

**Benefits:**
- Multiple paths to activation
- Context-aware suggestions
- Resilient to prompt variations

### Problem: Orphan Resources

Resource files not linked from SKILL.md:
- Users never discover the content
- Content drifts out of sync
- Maintenance burden without benefit

### Solution: Mandatory Linking

Every resource file MUST be:
1. Listed in SKILL.md Resource Files table
2. Cross-referenced from relevant sections
3. Kept in sync with main skill

## Structural Patterns

### Pattern 1: Basic Skill

For focused, simple skills under 300 lines.

```
skill-name/
└── SKILL.md
```

**Use When:**
- Single, focused topic
- Content fits comfortably in one file
- No need for deep dives
- Minimal reference material

### Pattern 2: Skill with Resources

For comprehensive skills needing depth.

```
skill-name/
├── SKILL.md
└── resources/
    ├── DETAILED_GUIDE.md
    ├── EXAMPLES.md
    └── TROUBLESHOOTING.md
```

**Use When:**
- Multiple sub-topics
- Extensive examples needed
- Reference material required
- Content exceeds 400 lines

### Pattern 3: Domain Skill

For technology or area expertise.

```json
{
  "backend-dev": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "medium"
  }
}
```

**Characteristics:**
- Provides guidance and patterns
- Never blocks operations
- Activates on relevant context
- Advisory only

### Pattern 4: Guardrail Skill

For standards enforcement.

```json
{
  "security-check": {
    "type": "guardrail",
    "enforcement": "warn",
    "priority": "high",
    "skipConditions": {
      "fileMarkers": ["@skip-security"],
      "envOverride": "SKIP_SECURITY_CHECK"
    }
  }
}
```

**Characteristics:**
- Checks code against rules
- Provides escape hatches
- Can warn or block
- Must have skip conditions

### Pattern 5: Workflow Skill

For multi-step processes.

```
deployment-guide/
├── SKILL.md
└── resources/
    ├── PRE_DEPLOY_CHECKLIST.md
    ├── DEPLOY_STEPS.md
    └── ROLLBACK_PROCEDURES.md
```

**Characteristics:**
- Step-by-step guidance
- Decision trees
- Checklists
- Never blocks (suggest only)

## File Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Skill directory | kebab-case | `skill-developer` |
| Main skill file | SKILL.md | `SKILL.md` |
| Resource files | UPPERCASE_SNAKE.md | `BEST_PRACTICES.md` |
| Rules config | skill-rules.json | `skill-rules.json` |

## Directory Placement

```
.claude/
├── skills/                     # All skills live here
│   ├── skill-rules.json        # Global trigger config
│   ├── skill-developer/        # This skill
│   │   ├── SKILL.md
│   │   └── resources/
│   ├── backend-dev/            # Another skill
│   │   └── SKILL.md
│   └── shared/                 # Shared resources (optional)
│       └── COMMON_PATTERNS.md
├── commands/                   # Slash commands
│   └── skill-dev.md
└── hooks/                      # Automation hooks
    ├── skill-suggester.py
    └── skill-validator.py
```

## Architecture Decision Framework

When designing a skill, work through these decisions:

### 1. Scope Decision

```
How many distinct topics does this skill cover?
├── 1 topic → Single SKILL.md
├── 2-3 related topics → SKILL.md + optional resources
└── 4+ topics or unrelated → Consider splitting into multiple skills
```

### 2. Depth Decision

```
How much detail is needed?
├── Quick reference only → Minimal SKILL.md
├── Moderate depth → Full SKILL.md (<500 lines)
└── Deep dives needed → SKILL.md + resources
```

### 3. Trigger Decision

```
How should this skill activate?
├── Explicit requests only → Keywords only
├── Context-aware → Keywords + intentPatterns
└── File-aware → Add pathPatterns and contentPatterns
```

### 4. Enforcement Decision

```
What happens when skill activates?
├── Provide guidance → "suggest"
├── Warn about issues → "warn"
└── Block dangerous actions → "block" (use sparingly)
```

## Summary Checklist

Before finalizing skill architecture:

- [ ] SKILL.md under 500 lines
- [ ] All resource files referenced in SKILL.md
- [ ] Multiple trigger types configured
- [ ] Appropriate enforcement level
- [ ] Escape hatches for guardrails
- [ ] Clear naming conventions followed
- [ ] No orphan files
- [ ] No circular dependencies
