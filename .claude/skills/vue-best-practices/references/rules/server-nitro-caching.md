---
title: Nitro Caching with routeRules
impact: HIGH
impactDescription: dramatically reduces server response time
tags: server, nitro, caching, routeRules
---

## Nitro Caching with routeRules

Use Nuxt's routeRules to cache API responses and pages.

**nuxt.config.ts:**

```typescript
export default defineNuxtConfig({
  routeRules: {
    // Cache API responses for 1 hour
    '/api/products/**': { cache: { maxAge: 60 * 60 } },

    // Cache static pages for 1 day
    '/about': { cache: { maxAge: 60 * 60 * 24 } },

    // SWR: serve stale while revalidating
    '/api/stats': {
      cache: {
        maxAge: 60,
        staleMaxAge: 60 * 60
      }
    }
  }
})
```

Reference: [Nuxt Route Rules](https://nuxt.com/docs/guide/concepts/rendering#route-rules)
