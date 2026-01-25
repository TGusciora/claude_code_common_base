---
title: Cache Repeated Function Calls
impact: LOW-MEDIUM
impactDescription: avoids redundant computation
tags: js, cache, memoization, performance
---

## Cache Repeated Function Calls

Use a Map to cache function results.

**Incorrect (redundant computation):**

```typescript
function processItems(items: Item[]) {
  return items.map(item => ({
    ...item,
    slug: slugify(item.name) // Called repeatedly for same names
  }))
}
```

**Correct (cached results):**

```typescript
const slugCache = new Map<string, string>()

function getCachedSlug(text: string): string {
  if (!slugCache.has(text)) {
    slugCache.set(text, slugify(text))
  }
  return slugCache.get(text)!
}

function processItems(items: Item[]) {
  return items.map(item => ({
    ...item,
    slug: getCachedSlug(item.name)
  }))
}
```
