---
title: Hoist RegExp Creation
impact: LOW-MEDIUM
impactDescription: avoids RegExp compilation overhead
tags: js, regexp, hoisting, optimization
---

## Hoist RegExp Creation

Don't create RegExp inside reactive computations or loops.

**Incorrect (new RegExp every evaluation):**

```typescript
const highlighted = computed(() => {
  const regex = new RegExp(`(${query.value})`, 'gi')
  return text.value.replace(regex, '<mark>$1</mark>')
})
```

**Correct (memoize regex):**

```typescript
const regex = computed(() => new RegExp(`(${query.value})`, 'gi'))

const highlighted = computed(() => {
  return text.value.replace(regex.value, '<mark>$1</mark>')
})
```

**For static patterns, hoist to module level:**

```typescript
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function validateEmail(email: string) {
  return EMAIL_REGEX.test(email)
}
```
