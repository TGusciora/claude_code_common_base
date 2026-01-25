---
title: Functional Components for Stateless UI
impact: MEDIUM
impactDescription: lower memory footprint for simple components
tags: rendering, functional, stateless, performance
---

## Functional Components for Stateless UI

Use simple script setup components for stateless presentation - Vue 3's compiler optimizes them automatically.

**Simple stateless component:**

```vue
<!-- IconButton.vue -->
<script setup lang="ts">
defineProps<{
  icon: string
  label: string
}>()

const emit = defineEmits<{
  click: []
}>()
</script>

<template>
  <button @click="emit('click')" :aria-label="label">
    <Icon :name="icon" />
  </button>
</template>
```

**Using render functions for maximum control:**

```typescript
// Pure functional component with h()
import { h, FunctionalComponent } from 'vue'

interface Props {
  level: 1 | 2 | 3 | 4 | 5 | 6
}

const Heading: FunctionalComponent<Props> = (props, { slots }) => {
  return h(`h${props.level}`, slots.default?.())
}

Heading.props = ['level']

export default Heading
```
