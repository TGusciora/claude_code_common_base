---
title: Computed for Derived State
impact: MEDIUM
impactDescription: avoids redundant calculations and watcher overhead
tags: rerender, computed, derived-state, optimization
---

## Computed for Derived State

Use computed instead of watchers for derived values.

**Incorrect (watching and updating):**

```typescript
const firstName = ref('John')
const lastName = ref('Doe')
const fullName = ref('')

watch([firstName, lastName], ([first, last]) => {
  fullName.value = `${first} ${last}`
}, { immediate: true })
```

**Correct (computed property):**

```typescript
const firstName = ref('John')
const lastName = ref('Doe')
const fullName = computed(() => `${firstName.value} ${lastName.value}`)
```

**Computed with caching:**

```typescript
// Computed values are cached and only recalculated when dependencies change
const expensiveComputed = computed(() => {
  return items.value
    .filter(item => item.active)
    .map(item => transform(item))
    .sort((a, b) => a.priority - b.priority)
})
```

Reference: [Vue Computed](https://vuejs.org/guide/essentials/computed.html)
