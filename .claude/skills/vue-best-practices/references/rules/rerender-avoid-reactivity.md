---
title: Avoid Unnecessary Reactivity
impact: MEDIUM
impactDescription: reduces memory and CPU overhead
tags: rerender, reactivity, performance, static
---

## Avoid Unnecessary Reactivity

Don't make everything reactive—use plain objects when reactivity isn't needed.

**Incorrect (unnecessary reactivity):**

```typescript
// Static config doesn't need reactivity
const config = reactive({
  apiUrl: '/api',
  timeout: 5000
})

// Constants don't need reactivity
const COLORS = ref(['red', 'green', 'blue'])
```

**Correct (plain objects for static data):**

```typescript
// Plain object for static config
const config = {
  apiUrl: '/api',
  timeout: 5000
} as const

// Plain array for constants
const COLORS = ['red', 'green', 'blue'] as const
```

**Mark reactive properties as readonly when not mutated:**

```typescript
// If props won't be mutated, use readonly
const props = defineProps<{ items: Item[] }>()
const readonlyItems = readonly(props.items)
```
