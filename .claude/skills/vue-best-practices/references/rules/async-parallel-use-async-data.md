---
title: Parallel useAsyncData/useFetch
impact: CRITICAL
impactDescription: 2-10x improvement
tags: async, parallelization, nuxt, useFetch, useAsyncData
---

## Parallel useAsyncData/useFetch

In Nuxt 3, use Promise.all to parallelize multiple useAsyncData or useFetch calls instead of awaiting them sequentially.

**Incorrect (sequential execution, 3 round trips):**

```typescript
<script setup lang="ts">
const { data: user } = await useAsyncData('user', () => fetchUser())
const { data: posts } = await useAsyncData('posts', () => fetchPosts())
const { data: comments } = await useAsyncData('comments', () => fetchComments())
</script>
```

**Correct (parallel execution, 1 round trip):**

```typescript
<script setup lang="ts">
const [{ data: user }, { data: posts }, { data: comments }] = await Promise.all([
  useAsyncData('user', () => fetchUser()),
  useAsyncData('posts', () => fetchPosts()),
  useAsyncData('comments', () => fetchComments())
])
</script>
```

Reference: [Nuxt useAsyncData](https://nuxt.com/docs/api/composables/use-async-data)
