---
title: Use Set/Map for O(1) Lookups
impact: LOW-MEDIUM
impactDescription: O(n) -> O(1) per lookup
tags: js, set, map, lookup, performance
---

## Use Set/Map for O(1) Lookups

Convert arrays to Set/Map for repeated membership checks.

**Incorrect (O(n) per check):**

```typescript
const allowedIds = ['a', 'b', 'c']
items.filter(item => allowedIds.includes(item.id))
```

**Correct (O(1) per check):**

```typescript
const allowedIds = new Set(['a', 'b', 'c'])
items.filter(item => allowedIds.has(item.id))
```

**In Vue computed:**

```typescript
const allowedIdsSet = computed(() => new Set(props.allowedIds))

const filteredItems = computed(() =>
  items.value.filter(item => allowedIdsSet.value.has(item.id))
)
```
