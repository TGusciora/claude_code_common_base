---
title: Minimize Serialization at Server/Client Boundary
impact: HIGH
impactDescription: reduces payload size and parsing time
tags: server, serialization, ssr, payload
---

## Minimize Serialization at Server/Client Boundary

Only pass fields that the client actually uses when returning data from server to client.

**Incorrect (serializes all 50 fields):**

```vue
<script setup lang="ts">
const { data: user } = await useAsyncData('user', () => fetchUser())
// user has 50 fields but template only uses name
</script>

<template>
  <div>{{ user?.name }}</div>
</template>
```

**Correct (serializes only needed fields):**

```vue
<script setup lang="ts">
const { data: userName } = await useAsyncData('userName', async () => {
  const user = await fetchUser()
  return user.name // Only return what's needed
})
</script>

<template>
  <div>{{ userName }}</div>
</template>
```

For complex objects, use `pick` to select specific fields:

```typescript
const { data: user } = await useAsyncData('user', async () => {
  const fullUser = await fetchUser()
  return {
    id: fullUser.id,
    name: fullUser.name,
    avatar: fullUser.avatar
  }
})
```
