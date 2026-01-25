---
title: Early Length Check for Array Comparisons
impact: LOW-MEDIUM
impactDescription: O(1) early exit for different-length arrays
tags: js, arrays, comparison, optimization
---

## Early Length Check for Array Comparisons

Check lengths first before expensive comparisons.

**Incorrect (always runs expensive comparison):**

```typescript
function hasChanges(current: string[], original: string[]) {
  return current.sort().join() !== original.sort().join()
}
```

**Correct (O(1) length check first):**

```typescript
function hasChanges(current: string[], original: string[]) {
  if (current.length !== original.length) {
    return true
  }
  // Only do expensive comparison when lengths match
  return current.some((item, i) => item !== original[i])
}
```
