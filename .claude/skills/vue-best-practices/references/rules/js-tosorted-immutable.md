---
title: Use toSorted() Instead of sort()
impact: LOW-MEDIUM
impactDescription: prevents mutation bugs
tags: js, sort, immutability, arrays
---

## Use toSorted() Instead of sort()

.sort() mutates the array. Use .toSorted() for immutability.

**Incorrect (mutates original):**

```typescript
const sorted = items.sort((a, b) => a.name.localeCompare(b.name))
```

**Correct (creates new array):**

```typescript
const sorted = items.toSorted((a, b) => a.name.localeCompare(b.name))
```

**In Vue computed (immutability is critical):**

```typescript
// Incorrect: mutates reactive array
const sortedItems = computed(() =>
  items.value.sort((a, b) => a.name.localeCompare(b.name))
)

// Correct: creates new sorted array
const sortedItems = computed(() =>
  items.value.toSorted((a, b) => a.name.localeCompare(b.name))
)
```

**Fallback for older browsers:**

```typescript
const sorted = [...items].sort((a, b) => a.name.localeCompare(b.name))
```
