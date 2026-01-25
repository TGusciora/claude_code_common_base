---
title: watchEffect Cleanup
impact: MEDIUM
impactDescription: prevents memory leaks and stale callbacks
tags: rerender, watchEffect, cleanup, memory-leak
---

## watchEffect Cleanup

Use cleanup functions to prevent memory leaks and stale callbacks.

**Incorrect (no cleanup):**

```typescript
watchEffect(() => {
  const interval = setInterval(() => {
    updateData(data.value)
  }, 1000)
  // Memory leak: interval never cleared
})
```

**Correct (with cleanup):**

```typescript
watchEffect((onCleanup) => {
  const interval = setInterval(() => {
    updateData(data.value)
  }, 1000)

  onCleanup(() => {
    clearInterval(interval)
  })
})
```

**With async operations:**

```typescript
watchEffect(async (onCleanup) => {
  let cancelled = false

  onCleanup(() => {
    cancelled = true
  })

  const result = await fetchData(id.value)

  if (!cancelled) {
    data.value = result
  }
})
```

**With event listeners:**

```typescript
watchEffect((onCleanup) => {
  const handler = (e: Event) => handleEvent(e)
  window.addEventListener('resize', handler)

  onCleanup(() => {
    window.removeEventListener('resize', handler)
  })
})
```
