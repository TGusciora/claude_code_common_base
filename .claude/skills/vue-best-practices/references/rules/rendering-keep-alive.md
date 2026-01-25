---
title: KeepAlive for Expensive Components
impact: MEDIUM
impactDescription: preserves component state and avoids re-initialization
tags: rendering, KeepAlive, caching, state
---

## KeepAlive for Expensive Components

Use KeepAlive to cache component state when toggling visibility.

**Incorrect (component destroyed and recreated):**

```vue
<template>
  <component :is="currentTab" />
</template>
```

**Correct (component state preserved):**

```vue
<template>
  <KeepAlive :max="10">
    <component :is="currentTab" />
  </KeepAlive>
</template>
```

**With include/exclude:**

```vue
<template>
  <KeepAlive :include="['Dashboard', 'Settings']">
    <component :is="currentTab" />
  </KeepAlive>
</template>
```

**With lifecycle hooks:**

```vue
<script setup lang="ts">
onActivated(() => {
  // Called when component is activated from cache
  refreshData()
})

onDeactivated(() => {
  // Called when component is cached
  pauseUpdates()
})
</script>
```

Reference: [Vue KeepAlive](https://vuejs.org/guide/built-ins/keep-alive.html)
