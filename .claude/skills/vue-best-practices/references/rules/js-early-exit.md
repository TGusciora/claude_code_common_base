---
title: Early Return from Functions
impact: LOW-MEDIUM
impactDescription: skips unnecessary processing
tags: js, early-return, optimization, control-flow
---

## Early Return from Functions

Return early when result is determined.

**Incorrect (processes all items):**

```typescript
function validateUsers(users: User[]) {
  let hasError = false
  for (const user of users) {
    if (!user.email) hasError = true
  }
  return !hasError
}
```

**Correct (returns immediately):**

```typescript
function validateUsers(users: User[]) {
  for (const user of users) {
    if (!user.email) return false
  }
  return true
}
```
