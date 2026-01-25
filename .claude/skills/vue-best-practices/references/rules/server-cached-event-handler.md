---
title: Cross-Request Caching with cachedEventHandler
impact: HIGH
impactDescription: caches expensive operations across requests
tags: server, caching, nitro, event-handler
---

## Cross-Request Caching with cachedEventHandler

For expensive operations shared across requests, use cachedEventHandler.

```typescript
// server/api/expensive-data.ts
export default cachedEventHandler(async (event) => {
  // This expensive operation is cached across requests
  const data = await expensiveComputation()
  return data
}, {
  maxAge: 60 * 60, // 1 hour
  name: 'expensive-data',
  getKey: (event) => event.path
})
```

**With dynamic cache keys:**

```typescript
// server/api/user/[id].ts
export default cachedEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')
  return await fetchUserData(id)
}, {
  maxAge: 60 * 5, // 5 minutes
  name: 'user-data',
  getKey: (event) => getRouterParam(event, 'id')
})
```

Reference: [Nitro Caching](https://nitro.unjs.io/guide/cache)
