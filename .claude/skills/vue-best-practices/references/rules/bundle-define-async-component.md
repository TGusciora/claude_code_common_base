---
title: defineAsyncComponent for Heavy Components
impact: CRITICAL
impactDescription: directly affects TTI and LCP
tags: bundle, async-component, code-splitting, lazy-loading
---

## defineAsyncComponent for Heavy Components

Use `defineAsyncComponent` to lazy-load large components not needed on initial render.

**Incorrect (Monaco bundles with main chunk ~300KB):**

```vue
<script setup lang="ts">
import MonacoEditor from './MonacoEditor.vue'
</script>

<template>
  <MonacoEditor :value="code" />
</template>
```

**Correct (Monaco loads on demand):**

```vue
<script setup lang="ts">
const MonacoEditor = defineAsyncComponent(() =>
  import('./MonacoEditor.vue')
)
</script>

<template>
  <ClientOnly>
    <MonacoEditor :value="code" />
  </ClientOnly>
</template>
```

**With loading and error states:**

```typescript
const MonacoEditor = defineAsyncComponent({
  loader: () => import('./MonacoEditor.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorDisplay,
  delay: 200,
  timeout: 10000
})
```

Reference: [Vue Async Components](https://vuejs.org/guide/components/async.html)
