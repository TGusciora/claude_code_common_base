---
title: shallowRef for Large Objects
impact: MEDIUM
impactDescription: reduces reactivity overhead for large data structures
tags: rerender, shallowRef, reactivity, performance
---

## shallowRef for Large Objects

Use shallowRef when you only need reactivity on the top level, not deep properties.

**Incorrect (deep reactivity for large list):**

```typescript
const items = ref<Item[]>([]) // Tracks every nested property

function updateItems(newItems: Item[]) {
  items.value = newItems // Vue recursively makes all properties reactive
}
```

**Correct (shallow reactivity):**

```typescript
const items = shallowRef<Item[]>([]) // Only tracks assignment

function updateItems(newItems: Item[]) {
  items.value = newItems // Only triggers when entire array is replaced
}

// For updating, replace the entire array
function addItem(item: Item) {
  items.value = [...items.value, item]
}
```

**For large objects:**

```typescript
const config = shallowRef<Config>({})
const bigData = shallowRef<BigDataStructure>(null)
```

Reference: [Vue shallowRef](https://vuejs.org/api/reactivity-advanced.html#shallowref)
