---
title: CSS content-visibility for Long Lists
impact: MEDIUM
impactDescription: 10x faster initial render for long lists
tags: rendering, content-visibility, css, virtualization
---

## CSS content-visibility for Long Lists

Apply content-visibility to defer off-screen rendering.

```css
.list-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

```vue
<template>
  <div class="list-container">
    <div
      v-for="item in items"
      :key="item.id"
      class="list-item"
    >
      <ItemContent :item="item" />
    </div>
  </div>
</template>

<style>
.list-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
</style>
```

For 1000 items, browser skips layout/paint for ~990 off-screen items (10x faster initial render).

**With Tailwind CSS:**

```vue
<template>
  <div
    v-for="item in items"
    :key="item.id"
    class="[content-visibility:auto] [contain-intrinsic-size:0_80px]"
  >
    <ItemContent :item="item" />
  </div>
</template>
```
