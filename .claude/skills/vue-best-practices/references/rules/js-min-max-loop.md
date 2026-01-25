---
title: Use Loop for Min/Max Instead of Sort
impact: LOW-MEDIUM
impactDescription: O(n log n) -> O(n)
tags: js, sort, min-max, optimization
---

## Use Loop for Min/Max Instead of Sort

Finding min/max only requires a single pass.

**Incorrect (O(n log n)):**

```typescript
function getLatest(items: Item[]) {
  return [...items].sort((a, b) => b.date - a.date)[0]
}
```

**Correct (O(n)):**

```typescript
function getLatest(items: Item[]) {
  if (items.length === 0) return null
  return items.reduce((latest, item) =>
    item.date > latest.date ? item : latest
  )
}
```

**Alternative with explicit loop:**

```typescript
function getLatest(items: Item[]) {
  if (items.length === 0) return null

  let latest = items[0]
  for (let i = 1; i < items.length; i++) {
    if (items[i].date > latest.date) {
      latest = items[i]
    }
  }
  return latest
}
```
