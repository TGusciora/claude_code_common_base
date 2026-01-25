---
title: Conditional Module Loading
impact: CRITICAL
impactDescription: reduces initial bundle by deferring non-critical code
tags: bundle, dynamic-import, lazy-loading
---

## Conditional Module Loading

Load large data or modules only when a feature is activated.

**Example (lazy-load animation frames):**

```vue
<script setup lang="ts">
const enabled = ref(false)
const frames = ref<Frame[] | null>(null)

watch(enabled, async (isEnabled) => {
  if (isEnabled && !frames.value && import.meta.client) {
    const mod = await import('./animation-frames')
    frames.value = mod.frames
  }
})
</script>

<template>
  <Skeleton v-if="!frames" />
  <Canvas v-else :frames="frames" />
</template>
```

The `import.meta.client` check prevents bundling this module for SSR, optimizing server bundle size.
