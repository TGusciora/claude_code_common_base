---
title: Strategic Suspense Boundaries
impact: CRITICAL
impactDescription: improves perceived performance
tags: async, suspense, streaming, ssr
---

## Strategic Suspense Boundaries

Use Suspense to show wrapper UI faster while data loads. In Nuxt 3, components using useAsyncData automatically work with Suspense.

**Incorrect (wrapper blocked by data fetching):**

```vue
<script setup lang="ts">
const { data } = await useAsyncData('data', () => fetchData())
</script>

<template>
  <div>
    <div>Sidebar</div>
    <div>Header</div>
    <div>
      <DataDisplay :data="data" />
    </div>
    <div>Footer</div>
  </div>
</template>
```

**Correct (wrapper shows immediately, data streams in):**

```vue
<!-- Parent component -->
<template>
  <div>
    <div>Sidebar</div>
    <div>Header</div>
    <Suspense>
      <DataDisplay />
      <template #fallback>
        <Skeleton />
      </template>
    </Suspense>
    <div>Footer</div>
  </div>
</template>

<!-- DataDisplay.vue -->
<script setup lang="ts">
const { data } = await useAsyncData('data', () => fetchData())
</script>

<template>
  <div>{{ data.content }}</div>
</template>
```

Reference: [Vue Suspense](https://vuejs.org/guide/built-ins/suspense.html)
