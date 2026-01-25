---
title: Composables for Reusable Logic
impact: LOW
impactDescription: promotes code reuse and testability
tags: advanced, composables, reusability, patterns
---

## Composables for Reusable Logic

Extract reusable logic into composables.

```typescript
// composables/useCounter.ts
export function useCounter(initial = 0) {
  const count = ref(initial)

  const increment = () => count.value++
  const decrement = () => count.value--
  const reset = () => count.value = initial

  return { count, increment, decrement, reset }
}

// Usage
const { count, increment } = useCounter(10)
```

**With async operations:**

```typescript
// composables/useApi.ts
export function useApi<T>(url: string) {
  const data = ref<T | null>(null)
  const error = ref<Error | null>(null)
  const loading = ref(false)

  const execute = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await fetch(url)
      data.value = await response.json()
    } catch (e) {
      error.value = e as Error
    } finally {
      loading.value = false
    }
  }

  return { data, error, loading, execute }
}
```

Reference: [Vue Composables](https://vuejs.org/guide/reusability/composables.html)
