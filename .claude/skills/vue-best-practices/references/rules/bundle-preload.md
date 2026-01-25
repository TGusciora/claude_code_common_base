---
title: Preload Based on User Intent
impact: CRITICAL
impactDescription: reduces perceived latency for heavy components
tags: bundle, preload, user-intent, lazy-loading
---

## Preload Based on User Intent

Preload heavy bundles before they're needed to reduce perceived latency.

**Example (preload on hover/focus):**

```vue
<script setup lang="ts">
const preload = () => {
  if (import.meta.client) {
    import('./MonacoEditor.vue')
  }
}
</script>

<template>
  <button
    @mouseenter="preload"
    @focus="preload"
    @click="openEditor"
  >
    Open Editor
  </button>
</template>
```

**Example (preload when feature flag is enabled):**

```vue
<script setup lang="ts">
const { editorEnabled } = useFeatureFlags()

watch(editorEnabled, (enabled) => {
  if (enabled && import.meta.client) {
    import('./MonacoEditor.vue')
  }
}, { immediate: true })
</script>
```
