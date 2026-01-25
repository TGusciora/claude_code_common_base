---
title: Hybrid Rendering with routeRules
impact: HIGH
impactDescription: optimal rendering strategy per route
tags: server, ssr, isr, ssg, hybrid
---

## Hybrid Rendering with routeRules

Use different rendering modes for different routes to optimize performance.

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    // Static generation at build time
    '/': { prerender: true },
    '/about': { prerender: true },

    // Client-side rendering only
    '/admin/**': { ssr: false },

    // ISR with 1 hour revalidation
    '/blog/**': { isr: 60 * 60 },

    // SSR with edge caching
    '/api/**': { cache: { maxAge: 60 } },

    // SWR pattern
    '/products/**': {
      swr: true,
      cache: {
        maxAge: 60,
        staleMaxAge: 60 * 60
      }
    }
  }
})
```

Reference: [Nuxt Hybrid Rendering](https://nuxt.com/docs/guide/concepts/rendering#hybrid-rendering)
