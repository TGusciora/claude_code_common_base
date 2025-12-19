# First Principles for Skill Development

This document covers the foundational thinking that should guide every skill design decision.

## KISS (Keep It Simple, Stupid)

### What It Means for Skills

Simplicity is the ultimate sophistication. A skill should do one thing well rather than many things poorly.

**Core Tenets:**
- One skill = one domain/problem area
- Prefer shallow hierarchies over deep nesting
- If you can't explain the skill in one sentence, split it
- Every section should serve a clear, immediate purpose

### Application Checklist

Before finalizing a skill, ask:

- [ ] Can someone understand this skill in 30 seconds?
- [ ] Does every section serve a clear purpose?
- [ ] Are examples minimal but complete?
- [ ] Could any section be removed without loss?
- [ ] Is the structure intuitive?

### KISS Violations

**Too Complex:**
```markdown
## Database Operations
### SQL Queries
#### SELECT Statements
##### Basic SELECT
###### Column Selection
```

**Simple:**
```markdown
## SQL Queries

### SELECT Basics
[Content with examples]
```

### The Simplicity Test

If explaining your skill structure takes longer than explaining what the skill does, it's too complex.

## YAGNI (You Aren't Gonna Need It)

### What It Means for Skills

Don't add content anticipating future needs. Add content when actual need emerges.

**Core Tenets:**
- Only implement what's needed NOW
- No speculative features or "just in case" content
- Delete unused sections immediately
- Start minimal, expand based on real usage

### Red Flags

Watch for these YAGNI violations:

- Resource files with no references in SKILL.md
- Sections copied from other skills "because they might help"
- Triggers that never fire
- Examples for edge cases no one encounters
- "Advanced" sections before basics are solid

### The YAGNI Decision Framework

When tempted to add content:

```
Is this needed RIGHT NOW?
├── Yes → Add it
└── No → Is there a concrete use case coming soon?
    ├── Yes, with specific timeline → Add to TODO, implement when needed
    └── No, "might be useful" → DON'T add it
```

### Practical Application

**YAGNI Violation:**
```markdown
## Future Considerations
This section covers potential future enhancements...

## Advanced Patterns
These patterns may be useful someday...
```

**YAGNI Compliant:**
```markdown
<!-- Add advanced patterns when basic patterns prove insufficient -->
```

Or better: just don't include the section at all.

## DRY (Don't Repeat Yourself)

### What It Means for Skills

Every piece of knowledge should have a single, authoritative representation.

**Core Tenets:**
- Cross-reference instead of duplicating
- Use skill-rules.json for shared trigger patterns
- Create shared resource files for common patterns
- One source of truth per concept

### Cross-Referencing Patterns

**Instead of duplicating:**
```markdown
## Error Handling
[50 lines of error handling guidance]

## API Endpoints
### Error Handling
[Same 50 lines repeated]
```

**Cross-reference:**
```markdown
## Error Handling
[50 lines of error handling guidance]

## API Endpoints
For error handling patterns, see [Error Handling](#error-handling).
```

### When DRY Doesn't Apply

**Exception: Critical Safety Information**

Some information is so important it should be repeated:
- Security warnings
- Data loss prevention
- Irreversible operation warnings

Single points of failure are worse than DRY violations for critical safety content.

### Shared Resource Files

For patterns used across multiple skills:

```
.claude/skills/
├── shared/
│   └── ERROR_HANDLING.md    # Shared by multiple skills
├── backend-dev/
│   └── SKILL.md             # References shared/ERROR_HANDLING.md
└── frontend-dev/
    └── SKILL.md             # References shared/ERROR_HANDLING.md
```

## Single Responsibility Principle

### What It Means for Skills

A skill should have one reason to change. Each component should do one thing.

**Core Tenets:**
- One trigger pattern = one activation reason
- Resource files should be independently useful
- Avoid "god skills" that try to cover everything
- Each section should address one topic

### Applying SRP to Skills

**Skill Level:**
- A skill covers one domain (e.g., "Python testing" not "Python everything")
- Changes in one area shouldn't require changes in unrelated areas

**Section Level:**
- Each section addresses one topic
- Sections can be read independently when possible

**Trigger Level:**
- Each trigger has a clear activation scenario
- Don't bundle unrelated triggers

### SRP Violations

**God Skill:**
```markdown
# Full Stack Development Guide
## Frontend...
## Backend...
## Database...
## DevOps...
## Testing...
## Security...
```

**Focused Skills:**
```
frontend-dev/SKILL.md
backend-dev/SKILL.md
database-patterns/SKILL.md
devops-guide/SKILL.md
```

## Progressive Disclosure

### The 500-Line Rule

Main skill file stays under 500 lines. Details live in resource files.

**Why This Matters:**
1. Claude loads main skill first
2. Resources loaded on-demand
3. Reduced cognitive load
4. Easier maintenance
5. Faster initial skill comprehension

### When to Split Content

| Condition | Action |
|-----------|--------|
| SKILL.md > 400 lines | Plan resource files |
| SKILL.md > 500 lines | Must split |
| Section > 100 lines | Consider extracting |
| Content changes separately | Separate files |
| Content is reference-heavy | Resource file |

### Progressive Disclosure Pattern

**SKILL.md (Layer 1):**
```markdown
## Error Handling
Handle errors consistently using try/catch with proper logging.

> For detailed patterns, see [ERROR_HANDLING.md](resources/ERROR_HANDLING.md)
```

**resources/ERROR_HANDLING.md (Layer 2):**
```markdown
# Error Handling Patterns

## Basic Pattern
[Detailed content]

## Advanced Patterns
[Detailed content]

## Edge Cases
[Detailed content]
```

### Summary

| Principle | Core Question |
|-----------|--------------|
| KISS | Is this the simplest solution? |
| YAGNI | Do we need this NOW? |
| DRY | Is this duplicated elsewhere? |
| SRP | Does this have one responsibility? |
| Progressive | Is this the right layer for this content? |

Apply these principles consistently, and your skills will be maintainable, focused, and effective.
