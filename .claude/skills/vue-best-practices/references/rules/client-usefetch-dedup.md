---
title: useFetch Deduplication
impact: MEDIUM-HIGH
impactDescription: eliminates duplicate network requests
tags: client, useFetch, deduplication, caching
---

## useFetch Deduplication

useFetch automatically deduplicates requests with the same key.

**Incorrect (multiple components, multiple requests):**

```vue
<script setup lang="ts">
// ComponentA.vue
const response = await fetch('/api/user')
const user = await response.json()
</script>

<!-- Same fetch in ComponentB.vue creates duplicate request -->
```

**Correct (multiple components, one request):**

```vue
<script setup lang="ts">
// ComponentA.vue
const { data: user } = await useFetch('/api/user')

// ComponentB.vue - same key, request is deduplicated
const { data: user } = await useFetch('/api/user')
</script>
```

**With custom key for deduplication:**

```typescript
const { data } = await useFetch('/api/items', {
  key: `items-${categoryId}`,
  query: { category: categoryId }
})
```

Reference: [Nuxt useFetch](https://nuxt.com/docs/api/composables/use-fetch)
