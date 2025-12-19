# Skill Anti-Patterns

This document catalogs common mistakes in skill development and how to avoid them.

## Architecture Anti-Patterns

### Anti-Pattern: God Skill

**Problem:** One skill tries to cover everything.

**Symptoms:**
- SKILL.md over 1000 lines
- Triggers for unrelated topics
- Sections that never get used together
- Frequent merge conflicts
- Hard to find specific information

**Example of God Skill:**
```markdown
# Full Stack Developer Guide
## Frontend Development...
## Backend Development...
## Database Design...
## DevOps & CI/CD...
## Security...
## Testing...
## Documentation...
## Project Management...
```

**Solution:** Split into focused skills with cross-references.

```
frontend-dev/SKILL.md
backend-dev/SKILL.md
database-patterns/SKILL.md
devops-guide/SKILL.md
```

**Prevention:** If you can't describe the skill in one sentence, it's too broad.

---

### Anti-Pattern: Orphan Resources

**Problem:** Resource files exist but aren't referenced from SKILL.md.

**Symptoms:**
- Users never discover the content
- Content drifts out of sync with main skill
- Resources become outdated without notice
- Wasted maintenance effort

**Example:**
```
skill-name/
├── SKILL.md                    # No links to resources
└── resources/
    ├── OLD_PATTERNS.md         # Never referenced
    ├── ADVANCED_TOPICS.md      # Never referenced
    └── MAYBE_USEFUL.md         # Never referenced
```

**Solution:** Every resource must be linked.

```markdown
## Resource Files

| File | Content | When to Use |
|------|---------|-------------|
| [PATTERNS.md](resources/PATTERNS.md) | Reusable patterns | Implementation |
| [ADVANCED.md](resources/ADVANCED.md) | Complex scenarios | Edge cases |
```

**Prevention:** Add resource file link before creating the file.

---

### Anti-Pattern: Copy-Paste Skills

**Problem:** Same content duplicated across multiple skills.

**Symptoms:**
- Same guidance in multiple places
- Updates missed in copies
- Inconsistent versions of same advice
- Confusion about which version is authoritative

**Example:**
```
frontend-dev/SKILL.md:
## Error Handling
[50 lines of error handling guidance]

backend-dev/SKILL.md:
## Error Handling
[Same 50 lines, slightly different]

api-design/SKILL.md:
## Error Handling
[Same 50 lines, different again]
```

**Solution:** Create shared resources or cross-reference.

```
shared/ERROR_HANDLING.md
[Authoritative 50 lines]

frontend-dev/SKILL.md:
## Error Handling
See [shared error handling guide](../shared/ERROR_HANDLING.md)
```

**Prevention:** Before writing, search for existing coverage.

---

## Trigger Anti-Patterns

### Anti-Pattern: Trigger Spam

**Problem:** Skill activates too frequently on irrelevant prompts.

**Symptoms:**
- Users see skill suggestions constantly
- Skill competes with more relevant skills
- Users start ignoring suggestions
- Noise drowns out signal

**Example:**
```json
{
  "keywords": ["code", "help", "how", "create", "add"]
}
```

**Solution:** Use specific, contextual triggers.

```json
{
  "keywords": ["create react component", "react hooks pattern"],
  "intentPatterns": ["(create|add).*react.*component"]
}
```

**Prevention:** Test triggers against common prompts before deploying.

---

### Anti-Pattern: Dead Triggers

**Problem:** Triggers configured but never match real usage.

**Symptoms:**
- Skill never auto-activates
- Users must always invoke manually
- Trigger patterns sit unused
- No value from auto-suggestion system

**Example:**
```json
{
  "keywords": ["implement sophisticated architectural paradigm"],
  "intentPatterns": ["(architect|design).*enterprise.*system"]
}
```

Nobody writes prompts like that.

**Solution:** Analyze real prompts, use natural language.

```json
{
  "keywords": ["design system", "architecture"],
  "intentPatterns": ["how.*?(structure|organize|design)"]
}
```

**Prevention:** Write triggers based on actual user prompts, not imagined ones.

---

### Anti-Pattern: Context Blindness

**Problem:** Skill only uses keyword triggers, missing file context.

**Symptoms:**
- Skill activates outside its domain
- Misses context-appropriate opportunities
- Over-relies on explicit mentions
- Doesn't understand what user is working on

**Example:**
```json
{
  "promptTriggers": {
    "keywords": ["react"]
  }
}
// No file triggers at all
```

**Solution:** Add file-aware triggers.

```json
{
  "promptTriggers": {
    "keywords": ["react", "component"]
  },
  "fileTriggers": {
    "pathPatterns": ["src/components/**/*.tsx"],
    "contentPatterns": ["import.*from 'react'"]
  }
}
```

**Prevention:** Always consider: "What files indicate this skill is relevant?"

---

## Content Anti-Patterns

### Anti-Pattern: Wall of Text

**Problem:** Long paragraphs without structure.

**Symptoms:**
- Users skip over content
- Key information buried
- Hard to scan
- Looks intimidating

**Example:**
```markdown
## Error Handling

When handling errors in your application you need to consider several
factors including the type of error whether it's recoverable the user
experience implications and logging requirements. For user-facing errors
you should provide helpful messages that explain what went wrong without
exposing sensitive details. For internal errors you want detailed logging
that helps with debugging. Consider using error boundaries in React
applications to catch component errors gracefully and provide fallback
UI. Always think about the error recovery path and whether the user can
retry the operation...
```

**Solution:** Use structure, lists, and formatting.

```markdown
## Error Handling

### Key Considerations

- **Error Type**: Recoverable vs. fatal
- **User Experience**: Clear, helpful messages
- **Logging**: Detailed for debugging, safe for users
- **Recovery**: Can the user retry?

### User-Facing Errors

Show helpful messages without sensitive details:

```typescript
// Good
"Unable to save. Please try again."

// Bad
"SQL Error: duplicate key constraint violation on users.email"
```
```

---

### Anti-Pattern: Example-Free Guidance

**Problem:** Instructions without concrete examples.

**Symptoms:**
- Users unsure how to apply guidance
- Vague, abstract advice
- Implementation left to interpretation
- Same questions asked repeatedly

**Example:**
```markdown
## API Design

Use RESTful conventions. Follow best practices for naming.
Make sure your responses are consistent. Handle errors properly.
```

**Solution:** Show, don't just tell.

```markdown
## API Design

### RESTful Naming

| Resource | GET | POST | PUT | DELETE |
|----------|-----|------|-----|--------|
| Users | /users | /users | /users/:id | /users/:id |

### Response Format

```json
{
  "data": { ... },
  "meta": { "page": 1, "total": 100 }
}
```

### Error Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required"
  }
}
```
```

---

### Anti-Pattern: Outdated Examples

**Problem:** Code examples that no longer work.

**Symptoms:**
- Examples fail when copied
- Old API versions referenced
- Deprecated patterns shown
- User confusion and frustration

**Example:**
```javascript
// Written in 2019, still in skill
import React from 'react';

class MyComponent extends React.Component {
  componentWillMount() {  // Deprecated!
    this.fetchData();
  }
  ...
}
```

**Solution:** Date examples, review regularly, use current patterns.

```javascript
// Updated: 2025-01
import { useEffect, useState } from 'react';

function MyComponent() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData().then(setData);
  }, []);

  return data ? <Display data={data} /> : <Loading />;
}
```

**Prevention:** Include review dates, set quarterly review reminders.

---

### Anti-Pattern: Jargon Without Context

**Problem:** Using specialized terms without explanation.

**Symptoms:**
- Newcomers can't understand content
- Terms used inconsistently
- Assumed knowledge not verified
- Exclusionary to learners

**Example:**
```markdown
Use the BFF pattern with a CQRS approach. Ensure your
aggregates are properly bounded and your sagas handle
compensation correctly.
```

**Solution:** Define terms or link to explanations.

```markdown
Use the **BFF (Backend For Frontend)** pattern - a dedicated
backend service for each frontend type (web, mobile, etc.).

Consider **CQRS (Command Query Responsibility Segregation)**
to separate read and write operations when:
- Read and write loads differ significantly
- You need different data models for reads vs. writes

> For more on these patterns, see [Architecture Patterns](resources/PATTERNS.md)
```

---

## Hook Anti-Patterns

### Anti-Pattern: Blocking Without Escape

**Problem:** Hook blocks actions with no way to override.

**Symptoms:**
- Users stuck when rule doesn't apply
- Workarounds defeat the purpose
- Frustrated users disable the hook
- Legitimate exceptions impossible

**Example:**
```python
# Always blocks, no escape
if dangerous_pattern_detected(content):
    sys.exit(2)  # No override possible
```

**Solution:** Always provide escape hatches.

```python
if dangerous_pattern_detected(content):
    # Check for override
    if "@skip-check" in content:
        sys.exit(0)
    if os.environ.get("SKIP_DANGER_CHECK"):
        sys.exit(0)
    # Block with clear message
    print("Dangerous pattern detected. Add @skip-check to override.",
          file=sys.stderr)
    sys.exit(2)
```

---

### Anti-Pattern: Silent Failure

**Problem:** Hook fails without informing user.

**Symptoms:**
- User doesn't know why something didn't work
- No actionable feedback
- Debugging is difficult
- Appears as mysterious behavior

**Example:**
```python
try:
    validate(content)
except Exception:
    pass  # Silent failure
sys.exit(0)
```

**Solution:** Always communicate failures.

```python
try:
    validate(content)
except ValidationError as e:
    print(f"Validation failed: {e}", file=sys.stderr)
    # Exit 0 for warnings (soft enforcement)
    sys.exit(0)
except Exception as e:
    print(f"Hook error (non-blocking): {e}", file=sys.stderr)
    sys.exit(0)
```

---

### Anti-Pattern: Slow Hooks

**Problem:** Hooks that add noticeable latency.

**Symptoms:**
- Typing feels sluggish
- Operations take longer than expected
- Users notice delays
- Overall experience degrades

**Example:**
```python
def main():
    # Loads entire codebase every time
    all_files = glob.glob("**/*", recursive=True)
    for f in all_files:
        analyze(f)  # Slow!
```

**Solution:** Keep hooks fast, cache when possible.

```python
# Performance targets:
# - UserPromptSubmit: < 100ms
# - PreToolUse: < 200ms

def main():
    # Only check relevant files
    data = json.load(sys.stdin)
    file_path = data.get("tool_input", {}).get("file_path")
    if file_path:
        analyze(file_path)  # Just this file
```

---

## Anti-Pattern Summary

| Category | Anti-Pattern | Quick Fix |
|----------|--------------|-----------|
| Architecture | God Skill | Split by domain |
| Architecture | Orphan Resources | Link all resources |
| Architecture | Copy-Paste | Use shared files |
| Triggers | Trigger Spam | More specific terms |
| Triggers | Dead Triggers | Use real user language |
| Triggers | Context Blindness | Add file triggers |
| Content | Wall of Text | Add structure |
| Content | No Examples | Add code samples |
| Content | Outdated Examples | Review quarterly |
| Content | Jargon | Define or link terms |
| Hooks | No Escape | Add skip conditions |
| Hooks | Silent Failure | Output errors |
| Hooks | Slow Hooks | Optimize, cache |
