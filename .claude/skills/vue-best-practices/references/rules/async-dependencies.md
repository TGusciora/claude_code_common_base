---
title: Dependency-Based Parallelization
impact: CRITICAL
impactDescription: reduces total latency by parallelizing independent work
tags: async, parallelization, promises, dependencies
---

## Dependency-Based Parallelization

For operations with partial dependencies, start independent operations immediately.

**Incorrect (config waits for auth unnecessarily):**

```typescript
<script setup lang="ts">
const { data: session } = await useAsyncData('session', () => auth())
const { data: config } = await useAsyncData('config', () => fetchConfig())
const { data: userData } = await useAsyncData('userData', () => fetchUserData(session.value.id))
</script>
```

**Correct (config and auth run in parallel):**

```typescript
<script setup lang="ts">
// Start both immediately
const sessionPromise = useAsyncData('session', () => auth())
const configPromise = useAsyncData('config', () => fetchConfig())

// Wait for session first since userData depends on it
const { data: session } = await sessionPromise

// Now fetch userData in parallel with config
const [{ data: config }, { data: userData }] = await Promise.all([
  configPromise,
  useAsyncData('userData', () => fetchUserData(session.value!.id))
])
</script>
```
