---
title: Defer Non-Critical Third-Party Libraries
impact: CRITICAL
impactDescription: removes blocking scripts from initial bundle
tags: bundle, third-party, analytics, lazy-loading
---

## Defer Non-Critical Third-Party Libraries

Analytics, logging, and error tracking don't block user interaction. Load them after hydration.

**Incorrect (blocks initial bundle):**

```vue
<script setup lang="ts">
import { Analytics } from '@vercel/analytics/vue'
</script>

<template>
  <div>
    <slot />
    <Analytics />
  </div>
</template>
```

**Correct (loads after hydration):**

```vue
<script setup lang="ts">
const Analytics = defineAsyncComponent(() =>
  import('@vercel/analytics/vue').then(m => m.Analytics)
)
</script>

<template>
  <div>
    <slot />
    <ClientOnly>
      <Analytics />
    </ClientOnly>
  </div>
</template>
```
