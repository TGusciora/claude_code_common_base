---
title: Batch DOM CSS Changes
impact: LOW-MEDIUM
impactDescription: reduces browser reflows
tags: js, dom, css, reflow
---

## Batch DOM CSS Changes

Group multiple CSS changes together via classes to minimize browser reflows.

**Incorrect (multiple reflows):**

```typescript
function updateStyles(el: HTMLElement) {
  el.style.width = '100px'
  el.style.height = '200px'
  el.style.backgroundColor = 'blue'
}
```

**Correct (toggle class - single reflow):**

```typescript
function updateStyles(el: HTMLElement) {
  el.classList.add('highlighted-box')
}
```

**In Vue, prefer class bindings:**

```vue
<template>
  <div :class="{ 'highlighted-box': isHighlighted }">
    Content
  </div>
</template>
```
