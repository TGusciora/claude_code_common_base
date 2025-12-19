# Skill Development Best Practices

This document covers proven practices for writing effective, maintainable skills.

## Writing Effective Descriptions

The `description` field in frontmatter is crucial for skill activation and discoverability.

### DO: Include Trigger Keywords

Keywords in the description help the skill activate appropriately.

```yaml
# Good
description: Guide for creating React components with TypeScript, MUI v7 styling, hooks patterns, and testing with Jest

# Better - front-loads important terms
description: React TypeScript component development guide covering MUI v7 styling, hooks patterns, state management, and Jest testing
```

### DON'T: Be Vague

```yaml
# Too generic - won't activate appropriately
description: Frontend development guide

# Too short - misses activation opportunities
description: React guide
```

### Description Checklist

- [ ] Under 1024 characters
- [ ] Includes terms users would search for
- [ ] Front-loads most important keywords
- [ ] Uses natural language
- [ ] Covers main topics the skill addresses

## Structuring Content

### Use Scannable Formats

Users often scan rather than read. Structure content for scanning:

| Format | Use For |
|--------|---------|
| Tables | Reference data, comparisons |
| Bullet lists | Options, features, steps |
| Numbered lists | Sequential procedures |
| Code blocks | Examples, commands |
| Headers | Navigation, organization |
| Bold | Key terms, emphasis |

### Example: Well-Structured Section

```markdown
## API Endpoint Patterns

### Quick Reference

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/users | List all users |
| GET | /api/users/:id | Get specific user |
| POST | /api/users | Create user |
| PUT | /api/users/:id | Update user |
| DELETE | /api/users/:id | Delete user |

### Basic GET Endpoint

```typescript
app.get('/api/users', async (req, res) => {
  const users = await userService.findAll();
  res.json(users);
});
```

### Error Handling

All endpoints should return consistent error responses:

```typescript
{
  "error": "User not found",
  "code": "USER_NOT_FOUND",
  "status": 404
}
```
```

### Headers Hierarchy

Use consistent header depth:

```markdown
# Skill Title (H1 - only one)

## Major Sections (H2)

### Sub-sections (H3)

#### Rare - only for deep nesting (H4)
```

Avoid going deeper than H4. If you need H5+, restructure.

## Writing Examples

### Minimal But Complete

Examples should be:
- **Compilable/runnable** without modification
- **Focused** on one concept
- **Complete** with necessary imports
- **Clean** of unrelated complexity

### Bad Example

```python
# Missing imports, unclear purpose, incomplete
def process(data):
    return transform(data)
```

### Good Example

```python
from typing import List, Dict

def transform_user_data(users: List[Dict]) -> List[Dict]:
    """Convert raw user records to API response format.

    Args:
        users: List of user records from database

    Returns:
        List of user objects formatted for API response
    """
    return [
        {
            "id": user["id"],
            "name": user["full_name"],
            "email": user["email"]
        }
        for user in users
    ]
```

### Example Annotations

Use comments to highlight key points:

```python
def create_user(data: UserCreate) -> User:
    # 1. Validate input
    validated = validate_user_data(data)

    # 2. Check for duplicates
    if user_exists(validated.email):
        raise DuplicateUserError(validated.email)

    # 3. Create in database
    user = db.users.create(validated)

    # 4. Send welcome email (async, don't block)
    send_welcome_email.delay(user.id)

    return user
```

## Trigger Pattern Design

### Keywords: Be Specific

Keywords are exact substring matches (case-insensitive).

```json
// Good - specific phrases
"keywords": ["create react component", "react hooks", "typescript component"]

// Bad - too broad, will over-activate
"keywords": ["react", "component", "create"]
```

### Intent Patterns: Capture Variations

Use regex to catch different phrasings:

```json
"intentPatterns": [
  // Matches: "create a component", "add new component", "make component"
  "(create|add|make|build).*?(component|page|view)",

  // Matches: "how to use hooks", "hooks tutorial"
  "(how|what).*?hooks",

  // Matches: "component structure", "component template"
  "component.*(structure|template|pattern)"
]
```

### Pattern Tips

| Pattern | Matches | Use For |
|---------|---------|---------|
| `.*?` | Any chars (non-greedy) | Words between |
| `\s+` | Whitespace | Word boundaries |
| `(a\|b\|c)` | Alternatives | Synonyms |
| `\w+` | Word characters | Single word |

### Test Your Patterns

Use [regex101.com](https://regex101.com) to test patterns before committing.

### Path Patterns: Target Precisely

```json
"pathPatterns": [
  // All TypeScript files in components
  "src/components/**/*.tsx",

  // All test files
  "**/*.test.ts",
  "**/*.spec.ts",

  // Specific directories
  "app/routes/**/*.ts"
]
```

### Path Exclusions

Prevent false positives:

```json
"pathExclusions": [
  // Don't activate for tests when not testing
  "**/*.test.*",
  "**/*.spec.*",
  "**/test/**",
  "**/__tests__/**",

  // Don't activate for generated files
  "**/generated/**",
  "**/dist/**"
]
```

## Cross-Referencing

### Internal Links

Link to other sections within the same file:

```markdown
For error handling patterns, see [Error Handling](#error-handling).
```

### Resource Links

Link to resource files:

```markdown
> For detailed examples, see [EXAMPLES.md](resources/EXAMPLES.md)
```

### External Links

Use sparingly and prefer stable URLs:

```markdown
See the [official documentation](https://docs.example.com/stable/guide).
```

## Maintenance Practices

### Version Tracking

For significant skills, track versions:

```markdown
---
name: my-skill
description: ...
---

<!-- Version: 1.2.0 | Last Updated: 2025-01-15 -->
<!-- Changelog: Added error handling section -->
```

### Review Triggers Quarterly

- Check which triggers actually fire
- Remove triggers that never activate
- Add triggers for missed opportunities
- Update patterns for new terminology

### Keep Examples Current

- Review code examples when dependencies update
- Remove deprecated patterns
- Test that examples still work
- Update syntax for new language versions

### Prune Unused Content

- Remove sections no one references
- Archive outdated patterns
- Consolidate similar sections
- Delete orphan resource files

## Quality Checklist

Before publishing a skill:

### Content Quality
- [ ] Purpose is clear in first paragraph
- [ ] "When to Use" covers all scenarios
- [ ] Examples are minimal but complete
- [ ] No walls of text - properly formatted
- [ ] Headers create logical structure

### Technical Quality
- [ ] Code examples compile/run
- [ ] Patterns are tested
- [ ] Links work
- [ ] No TODO placeholders left

### Maintenance Quality
- [ ] All resource files linked
- [ ] Version/date tracked
- [ ] Review schedule noted
- [ ] No deprecated content

## Common Formatting Patterns

### Decision Tables

```markdown
| Condition | Action |
|-----------|--------|
| Input < 0 | Return error |
| Input = 0 | Return empty |
| Input > 0 | Process normally |
```

### Checklists

```markdown
### Pre-deploy Checklist

- [ ] Tests passing
- [ ] Linting clean
- [ ] Version bumped
- [ ] Changelog updated
- [ ] PR approved
```

### Warning Callouts

```markdown
> **Warning:** This operation cannot be undone.

> **Note:** Requires admin privileges.

> **Tip:** Use `--dry-run` to preview changes.
```

### Code Comparison

```markdown
### Before

```python
# Old pattern
result = legacy_process(data)
```

### After

```python
# New pattern
result = modern_process(data, options=opts)
```
```

## Summary

| Practice | Key Point |
|----------|-----------|
| Descriptions | Include trigger keywords, front-load important terms |
| Structure | Use scannable formats, consistent headers |
| Examples | Minimal but complete, with annotations |
| Triggers | Specific keywords, tested patterns |
| Maintenance | Regular reviews, current examples |
