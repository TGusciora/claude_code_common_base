---
title: v-once for Static Content
impact: MEDIUM
impactDescription: skips re-rendering of static content
tags: rendering, v-once, static, optimization
---

## v-once for Static Content

Use v-once for content that never changes after initial render.

**Incorrect (re-evaluated every render):**

```vue
<template>
  <div>
    <h1>{{ appTitle }}</h1>
    <p>{{ staticDescription }}</p>
  </div>
</template>
```

**Correct (rendered once):**

```vue
<template>
  <div>
    <h1 v-once>{{ appTitle }}</h1>
    <p v-once>{{ staticDescription }}</p>
  </div>
</template>
```

**For larger static sections:**

```vue
<template>
  <div v-once>
    <h1>{{ appTitle }}</h1>
    <p>{{ staticDescription }}</p>
    <img :src="logo" />
  </div>
</template>
```

Reference: [Vue v-once](https://vuejs.org/api/built-in-directives.html#v-once)
