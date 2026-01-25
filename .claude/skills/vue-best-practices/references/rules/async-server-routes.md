---
title: Prevent Waterfall Chains in Server Routes
impact: CRITICAL
impactDescription: 2-5x improvement in API response time
tags: async, nitro, server, api-routes
---

## Prevent Waterfall Chains in Server Routes

In Nuxt server routes (API routes), start independent operations immediately.

**Incorrect (config waits for auth, data waits for both):**

```typescript
// server/api/dashboard.ts
export default defineEventHandler(async (event) => {
  const session = await auth(event)
  const config = await fetchConfig()
  const data = await fetchData(session.user.id)
  return { data, config }
})
```

**Correct (auth and config start immediately):**

```typescript
// server/api/dashboard.ts
export default defineEventHandler(async (event) => {
  const sessionPromise = auth(event)
  const configPromise = fetchConfig()

  const session = await sessionPromise
  const [config, data] = await Promise.all([
    configPromise,
    fetchData(session.user.id)
  ])

  return { data, config }
})
```
