---
title: Stale-While-Revalidate Pattern
impact: MEDIUM-HIGH
impactDescription: improves perceived performance with cached data
tags: client, swr, caching, revalidation
---

## Stale-While-Revalidate Pattern

Configure useFetch for SWR-like behavior to show cached data immediately.

```typescript
const { data, refresh } = await useFetch('/api/data', {
  // Return cached data immediately
  getCachedData(key) {
    return nuxtApp.payload.data[key] || nuxtApp.static.data[key]
  },
  // Revalidate in background
  dedupe: 'defer'
})

// Trigger background revalidation
onMounted(() => {
  refresh()
})
```

**With useAsyncData:**

```typescript
const { data, refresh } = await useAsyncData('user', () => fetchUser(), {
  getCachedData(key) {
    const cached = nuxtApp.payload.data[key]
    if (!cached) return null

    // Check if cache is stale (older than 5 minutes)
    const expiresAt = cached._expires
    if (expiresAt && Date.now() > expiresAt) {
      return null
    }
    return cached
  }
})
```
