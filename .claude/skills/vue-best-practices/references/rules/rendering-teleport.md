---
title: Teleport for Modals
impact: MEDIUM
impactDescription: avoids z-index and overflow issues
tags: rendering, Teleport, modal, portal
---

## Teleport for Modals

Use Teleport to render modals at document root, avoiding z-index and overflow issues.

```vue
<script setup lang="ts">
const showModal = ref(false)
</script>

<template>
  <button @click="showModal = true">Open Modal</button>

  <Teleport to="body">
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <slot />
        <button @click="showModal = false">Close</button>
      </div>
    </div>
  </Teleport>
</template>
```

**With conditional teleport:**

```vue
<template>
  <Teleport to="body" :disabled="inline">
    <Modal :open="isOpen" />
  </Teleport>
</template>
```

**Target specific container:**

```vue
<!-- In app.vue -->
<div id="modal-container"></div>

<!-- In component -->
<Teleport to="#modal-container">
  <Modal />
</Teleport>
```

Reference: [Vue Teleport](https://vuejs.org/guide/built-ins/teleport.html)
