---
title: ClientOnly for Browser-Specific Content
impact: MEDIUM-HIGH
impactDescription: prevents SSR errors and hydration mismatches
tags: client, ssr, hydration, browser
---

## ClientOnly for Browser-Specific Content

Use ClientOnly wrapper for content that should only render on the client.

```vue
<template>
  <div>
    <ServerContent />
    <ClientOnly>
      <BrowserOnlyWidget />
      <template #fallback>
        <Skeleton />
      </template>
    </ClientOnly>
  </div>
</template>
```

**Common use cases:**

```vue
<template>
  <!-- Browser-specific APIs -->
  <ClientOnly>
    <GeolocationMap />
  </ClientOnly>

  <!-- localStorage-dependent content -->
  <ClientOnly>
    <UserPreferences />
  </ClientOnly>

  <!-- Canvas/WebGL components -->
  <ClientOnly>
    <ThreeJSScene />
  </ClientOnly>
</template>
```

Reference: [Nuxt ClientOnly](https://nuxt.com/docs/api/components/client-only)
