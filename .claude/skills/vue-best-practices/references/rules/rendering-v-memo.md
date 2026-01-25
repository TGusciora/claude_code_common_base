---
title: v-memo for List Optimization
impact: MEDIUM
impactDescription: skips re-rendering unchanged list items
tags: rendering, v-memo, list, optimization
---

## v-memo for List Optimization

Use v-memo to skip re-rendering unchanged list items.

**Incorrect (all items re-render on any change):**

```vue
<template>
  <div v-for="item in items" :key="item.id">
    <ExpensiveComponent :item="item" />
  </div>
</template>
```

**Correct (only changed items re-render):**

```vue
<template>
  <div
    v-for="item in items"
    :key="item.id"
    v-memo="[item.id, item.updatedAt]"
  >
    <ExpensiveComponent :item="item" />
  </div>
</template>
```

**With selection state:**

```vue
<template>
  <div
    v-for="item in items"
    :key="item.id"
    v-memo="[item.id, item === selectedItem]"
    @click="selectedItem = item"
  >
    <ItemCard :item="item" :selected="item === selectedItem" />
  </div>
</template>
```

Reference: [Vue v-memo](https://vuejs.org/api/built-in-directives.html#v-memo)
