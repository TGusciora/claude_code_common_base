# Vue Best Practices - Complete Document

**Version 1.0.0**
Vue/Nuxt Community
January 2026

> **Note:**
> This document is mainly for agents and LLMs to follow when maintaining, generating, or refactoring Vue 3 and Nuxt 3 codebases.

---

## Abstract

Comprehensive performance optimization guide for Vue 3 and Nuxt 3 applications, designed for AI agents and LLMs. Contains 40+ rules across 8 categories, prioritized by impact from critical (eliminating waterfalls, reducing bundle size) to incremental (advanced patterns). Each rule includes detailed explanations, real-world examples comparing incorrect vs. correct implementations, and specific impact metrics to guide automated refactoring and code generation.

---

## Table of Contents

1. [Eliminating Waterfalls](#1-eliminating-waterfalls) — **CRITICAL**
   - 1.1 [Parallel useAsyncData/useFetch](#11)
   - 1.2 [Dependency-Based Parallelization](#12)
   - 1.3 [Prevent Waterfall Chains in Server Routes](#13)
   - 1.4 [Promise.all() for Independent Operations](#14)
   - 1.5 [Strategic Suspense Boundaries](#15)
2. [Bundle Size Optimization](#2-bundle-size-optimization) — **CRITICAL**
   - 2.1 [Avoid Barrel File Imports](#21)
   - 2.2 [Conditional Module Loading](#22)
   - 2.3 [Defer Non-Critical Third-Party Libraries](#23)
   - 2.4 [defineAsyncComponent for Heavy Components](#24)
   - 2.5 [Preload Based on User Intent](#25)
3. [Server-Side Performance](#3-server-side-performance) — **HIGH**
   - 3.1 [Nitro Caching with routeRules](#31)
   - 3.2 [Minimize Serialization at Server/Client Boundary](#32)
   - 3.3 [Hybrid Rendering with routeRules](#33)
   - 3.4 [Cross-Request Caching with cachedEventHandler](#34)
4. [Client-Side Data Fetching](#4-client-side-data-fetching) — **MEDIUM-HIGH**
   - 4.1 [useFetch Deduplication](#41)
   - 4.2 [ClientOnly for Browser-Specific Content](#42)
   - 4.3 [Stale-While-Revalidate Pattern](#43)
5. [Re-render Optimization](#5-re-render-optimization) — **MEDIUM**
   - 5.1 [shallowRef for Large Objects](#51)
   - 5.2 [Computed for Derived State](#52)
   - 5.3 [Narrow Watch Dependencies](#53)
   - 5.4 [watchEffect Cleanup](#54)
   - 5.5 [Avoid Unnecessary Reactivity](#55)
   - 5.6 [toRaw for Read-Only Access](#56)
6. [Rendering Performance](#6-rendering-performance) — **MEDIUM**
   - 6.1 [v-once for Static Content](#61)
   - 6.2 [v-memo for List Optimization](#62)
   - 6.3 [KeepAlive for Expensive Components](#63)
   - 6.4 [Teleport for Modals](#64)
   - 6.5 [CSS content-visibility for Long Lists](#65)
   - 6.6 [Functional Components for Stateless UI](#66)
   - 6.7 [Use Explicit Conditional Rendering](#67)
7. [JavaScript Performance](#7-javascript-performance) — **LOW-MEDIUM**
   - 7.1 [Batch DOM CSS Changes](#71)
   - 7.2 [Build Index Maps for Repeated Lookups](#72)
   - 7.3 [Cache Property Access in Loops](#73)
   - 7.4 [Cache Repeated Function Calls](#74)
   - 7.5 [Cache Storage API Calls](#75)
   - 7.6 [Combine Multiple Array Iterations](#76)
   - 7.7 [Early Length Check for Array Comparisons](#77)
   - 7.8 [Early Return from Functions](#78)
   - 7.9 [Hoist RegExp Creation](#79)
   - 7.10 [Use Loop for Min/Max Instead of Sort](#710)
   - 7.11 [Use Set/Map for O(1) Lookups](#711)
   - 7.12 [Use toSorted() Instead of sort()](#712)
8. [Advanced Patterns](#8-advanced-patterns) — **LOW**
   - 8.1 [Composables for Reusable Logic](#81)
   - 8.2 [provide/inject for Dependency Injection](#82)
   - 8.3 [VueUse for Common Utilities](#83)

---

## 1. Eliminating Waterfalls

**Impact: CRITICAL**

Waterfalls are the #1 performance killer. Each sequential await adds full network latency. Eliminating them yields the largest gains.

### 1.1 Parallel useAsyncData/useFetch

In Nuxt 3, use Promise.all to parallelize multiple useAsyncData or useFetch calls instead of awaiting them sequentially.

**Incorrect: sequential execution, 3 round trips**

```typescript
<script setup lang="ts">
const { data: user } = await useAsyncData('user', () => fetchUser())
const { data: posts } = await useAsyncData('posts', () => fetchPosts())
const { data: comments } = await useAsyncData('comments', () => fetchComments())
</script>
```

**Correct: parallel execution, 1 round trip**

```typescript
<script setup lang="ts">
const [{ data: user }, { data: posts }, { data: comments }] = await Promise.all([
  useAsyncData('user', () => fetchUser()),
  useAsyncData('posts', () => fetchPosts()),
  useAsyncData('comments', () => fetchComments())
])
</script>
```

### 1.2 Dependency-Based Parallelization

For operations with partial dependencies, start independent operations immediately.

**Incorrect: config waits for auth unnecessarily**

```typescript
<script setup lang="ts">
const { data: session } = await useAsyncData('session', () => auth())
const { data: config } = await useAsyncData('config', () => fetchConfig())
const { data: userData } = await useAsyncData('userData', () => fetchUserData(session.value.id))
</script>
```

**Correct: config and auth run in parallel**

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

### 1.3 Prevent Waterfall Chains in Server Routes

In Nuxt server routes (API routes), start independent operations immediately.

**Incorrect: config waits for auth, data waits for both**

```typescript
// server/api/dashboard.ts
export default defineEventHandler(async (event) => {
  const session = await auth(event)
  const config = await fetchConfig()
  const data = await fetchData(session.user.id)
  return { data, config }
})
```

**Correct: auth and config start immediately**

```typescript
// server/api/dashboard.ts
export default defineEventHandler(async (event) => {
  const sessionPromise = auth(event)
  const configPromise = fetchConfig()

  const session = await sessionPromise
  const [config, data] = await Promise.all([
    configPromise,
    fetchData(session.user.id)
  ])

  return { data, config }
})
```

### 1.4 Promise.all() for Independent Operations

When async operations have no interdependencies, execute them concurrently.

**Incorrect: sequential execution, 3 round trips**

```typescript
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()
```

**Correct: parallel execution, 1 round trip**

```typescript
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
])
```

### 1.5 Strategic Suspense Boundaries

Use Suspense to show wrapper UI faster while data loads. In Nuxt 3, components using useAsyncData automatically work with Suspense.

**Incorrect: wrapper blocked by data fetching**

```vue
<script setup lang="ts">
const { data } = await useAsyncData('data', () => fetchData())
</script>

<template>
  <div>
    <div>Sidebar</div>
    <div>Header</div>
    <div>
      <DataDisplay :data="data" />
    </div>
    <div>Footer</div>
  </div>
</template>
```

**Correct: wrapper shows immediately, data streams in**

```vue
<!-- Parent component -->
<template>
  <div>
    <div>Sidebar</div>
    <div>Header</div>
    <Suspense>
      <DataDisplay />
      <template #fallback>
        <Skeleton />
      </template>
    </Suspense>
    <div>Footer</div>
  </div>
</template>

<!-- DataDisplay.vue -->
<script setup lang="ts">
const { data } = await useAsyncData('data', () => fetchData())
</script>

<template>
  <div>{{ data.content }}</div>
</template>
```

---

## 2. Bundle Size Optimization

**Impact: CRITICAL**

Reducing initial bundle size improves Time to Interactive and Largest Contentful Paint.

### 2.1 Avoid Barrel File Imports

Import directly from source files instead of barrel files to avoid loading unused modules.

**Incorrect: imports entire library**

```typescript
import { Check, X, Menu } from 'lucide-vue-next'
// Loads 1,500+ modules

import { Button, TextField } from '@headlessui/vue'
// Loads entire component library
```

**Correct: imports only what you need**

```typescript
import Check from 'lucide-vue-next/dist/esm/icons/check'
import X from 'lucide-vue-next/dist/esm/icons/x'
import Menu from 'lucide-vue-next/dist/esm/icons/menu'
// Loads only 3 modules

import Button from '@headlessui/vue/dist/components/button/button'
// Loads only what you use
```

**Nuxt optimization:**

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  vite: {
    optimizeDeps: {
      include: ['lucide-vue-next']
    }
  }
})
```

### 2.2 Conditional Module Loading

Load large data or modules only when a feature is activated.

**Example: lazy-load animation frames**

```vue
<script setup lang="ts">
const enabled = ref(false)
const frames = ref<Frame[] | null>(null)

watch(enabled, async (isEnabled) => {
  if (isEnabled && !frames.value && import.meta.client) {
    const mod = await import('./animation-frames')
    frames.value = mod.frames
  }
})
</script>

<template>
  <Skeleton v-if="!frames" />
  <Canvas v-else :frames="frames" />
</template>
```

### 2.3 Defer Non-Critical Third-Party Libraries

Analytics, logging, and error tracking don't block user interaction. Load them after hydration.

**Incorrect: blocks initial bundle**

```vue
<script setup lang="ts">
import { Analytics } from '@vercel/analytics/vue'
</script>

<template>
  <div>
    <slot />
    <Analytics />
  </div>
</template>
```

**Correct: loads after hydration**

```vue
<script setup lang="ts">
const Analytics = defineAsyncComponent(() =>
  import('@vercel/analytics/vue').then(m => m.Analytics)
)
</script>

<template>
  <div>
    <slot />
    <ClientOnly>
      <Analytics />
    </ClientOnly>
  </div>
</template>
```

### 2.4 defineAsyncComponent for Heavy Components

Use `defineAsyncComponent` to lazy-load large components not needed on initial render.

**Incorrect: Monaco bundles with main chunk ~300KB**

```vue
<script setup lang="ts">
import MonacoEditor from './MonacoEditor.vue'
</script>

<template>
  <MonacoEditor :value="code" />
</template>
```

**Correct: Monaco loads on demand**

```vue
<script setup lang="ts">
const MonacoEditor = defineAsyncComponent(() =>
  import('./MonacoEditor.vue')
)
</script>

<template>
  <ClientOnly>
    <MonacoEditor :value="code" />
  </ClientOnly>
</template>
```

**With loading and error states:**

```typescript
const MonacoEditor = defineAsyncComponent({
  loader: () => import('./MonacoEditor.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorDisplay,
  delay: 200,
  timeout: 10000
})
```

### 2.5 Preload Based on User Intent

Preload heavy bundles before they're needed to reduce perceived latency.

**Example: preload on hover/focus**

```vue
<script setup lang="ts">
const preload = () => {
  if (import.meta.client) {
    import('./MonacoEditor.vue')
  }
}
</script>

<template>
  <button
    @mouseenter="preload"
    @focus="preload"
    @click="openEditor"
  >
    Open Editor
  </button>
</template>
```

---

## 3. Server-Side Performance

**Impact: HIGH**

Optimizing Nuxt SSR and Nitro caching eliminates server-side waterfalls and reduces response times.

### 3.1 Nitro Caching with routeRules

Use Nuxt's routeRules to cache API responses and pages.

**nuxt.config.ts:**

```typescript
export default defineNuxtConfig({
  routeRules: {
    // Cache API responses for 1 hour
    '/api/products/**': { cache: { maxAge: 60 * 60 } },

    // Cache static pages for 1 day
    '/about': { cache: { maxAge: 60 * 60 * 24 } },

    // SWR: serve stale while revalidating
    '/api/stats': {
      cache: {
        maxAge: 60,
        staleMaxAge: 60 * 60
      }
    }
  }
})
```

### 3.2 Minimize Serialization at Server/Client Boundary

Only pass fields that the client actually uses when returning data from server to client.

**Incorrect: serializes all 50 fields**

```vue
<script setup lang="ts">
const { data: user } = await useAsyncData('user', () => fetchUser())
// user has 50 fields but template only uses name
</script>

<template>
  <div>{{ user?.name }}</div>
</template>
```

**Correct: serializes only needed fields**

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

### 3.3 Hybrid Rendering with routeRules

Use different rendering modes for different routes.

```typescript
export default defineNuxtConfig({
  routeRules: {
    // Static generation at build time
    '/': { prerender: true },
    '/about': { prerender: true },

    // Client-side rendering only
    '/admin/**': { ssr: false },

    // ISR with 1 hour revalidation
    '/blog/**': { isr: 60 * 60 },

    // SSR with edge runtime
    '/api/**': { cache: { maxAge: 60 } }
  }
})
```

### 3.4 Cross-Request Caching with cachedEventHandler

For expensive operations shared across requests, use cachedEventHandler.

```typescript
// server/api/expensive-data.ts
export default cachedEventHandler(async (event) => {
  // This expensive operation is cached across requests
  const data = await expensiveComputation()
  return data
}, {
  maxAge: 60 * 60, // 1 hour
  name: 'expensive-data',
  getKey: (event) => event.path
})
```

---

## 4. Client-Side Data Fetching

**Impact: MEDIUM-HIGH**

Automatic deduplication and efficient data fetching patterns reduce redundant network requests.

### 4.1 useFetch Deduplication

useFetch automatically deduplicates requests with the same key.

**Incorrect: multiple components, multiple requests**

```vue
<script setup lang="ts">
// ComponentA.vue
const response = await fetch('/api/user')
const user = await response.json()
</script>

<!-- Same fetch in ComponentB.vue creates duplicate request -->
```

**Correct: multiple components, one request**

```vue
<script setup lang="ts">
// ComponentA.vue
const { data: user } = await useFetch('/api/user')

// ComponentB.vue - same key, request is deduplicated
const { data: user } = await useFetch('/api/user')
</script>
```

### 4.2 ClientOnly for Browser-Specific Content

Use ClientOnly wrapper for content that should only render on the client.

```vue
<template>
  <div>
    <ServerContent />
    <ClientOnly>
      <BrowserOnlyWidget />
      <template #fallback>
        <Skeleton />
      </template>
    </ClientOnly>
  </div>
</template>
```

### 4.3 Stale-While-Revalidate Pattern

Configure useFetch for SWR-like behavior.

```typescript
const { data, refresh } = await useFetch('/api/data', {
  // Return cached data immediately
  getCachedData(key) {
    return nuxtApp.payload.data[key] || nuxtApp.static.data[key]
  },
  // Revalidate in background
  dedupe: 'defer'
})

// Trigger background revalidation
onMounted(() => {
  refresh()
})
```

---

## 5. Re-render Optimization

**Impact: MEDIUM**

Reducing unnecessary reactivity overhead minimizes wasted computation and improves UI responsiveness.

### 5.1 shallowRef for Large Objects

Use shallowRef when you only need reactivity on the top level, not deep properties.

**Incorrect: deep reactivity for large list**

```typescript
const items = ref<Item[]>([]) // Tracks every nested property

function updateItems(newItems: Item[]) {
  items.value = newItems // Vue recursively makes all properties reactive
}
```

**Correct: shallow reactivity**

```typescript
const items = shallowRef<Item[]>([]) // Only tracks assignment

function updateItems(newItems: Item[]) {
  items.value = newItems // Only triggers when entire array is replaced
}

// For large objects
const config = shallowRef<Config>({})
```

### 5.2 Computed for Derived State

Use computed instead of watchers for derived values.

**Incorrect: watching and updating**

```typescript
const firstName = ref('John')
const lastName = ref('Doe')
const fullName = ref('')

watch([firstName, lastName], ([first, last]) => {
  fullName.value = `${first} ${last}`
}, { immediate: true })
```

**Correct: computed property**

```typescript
const firstName = ref('John')
const lastName = ref('Doe')
const fullName = computed(() => `${firstName.value} ${lastName.value}`)
```

### 5.3 Narrow Watch Dependencies

Watch specific properties instead of entire objects.

**Incorrect: re-runs on any user field change**

```typescript
watch(user, (newUser) => {
  console.log('User changed:', newUser.id)
})
```

**Correct: re-runs only when id changes**

```typescript
watch(() => user.value.id, (newId) => {
  console.log('User ID changed:', newId)
})
```

### 5.4 watchEffect Cleanup

Use cleanup functions to prevent memory leaks and stale callbacks.

**Incorrect: no cleanup**

```typescript
watchEffect(() => {
  const interval = setInterval(() => {
    updateData(data.value)
  }, 1000)
  // Memory leak: interval never cleared
})
```

**Correct: with cleanup**

```typescript
watchEffect((onCleanup) => {
  const interval = setInterval(() => {
    updateData(data.value)
  }, 1000)

  onCleanup(() => {
    clearInterval(interval)
  })
})
```

### 5.5 Avoid Unnecessary Reactivity

Don't make everything reactive—use plain objects when reactivity isn't needed.

**Incorrect: unnecessary reactivity**

```typescript
// Static config doesn't need reactivity
const config = reactive({
  apiUrl: '/api',
  timeout: 5000
})
```

**Correct: plain object for static data**

```typescript
// Plain object for static config
const config = {
  apiUrl: '/api',
  timeout: 5000
} as const
```

### 5.6 toRaw for Read-Only Access

Use toRaw when you need to read reactive data without triggering tracking.

**Incorrect: triggers unnecessary tracking**

```typescript
function logItems() {
  // Every property access is tracked
  console.log(JSON.stringify(items.value))
}
```

**Correct: no tracking overhead**

```typescript
import { toRaw } from 'vue'

function logItems() {
  // No reactivity tracking
  console.log(JSON.stringify(toRaw(items.value)))
}
```

---

## 6. Rendering Performance

**Impact: MEDIUM**

Optimizing the rendering process reduces the work the browser needs to do.

### 6.1 v-once for Static Content

Use v-once for content that never changes after initial render.

**Incorrect: re-evaluated every render**

```vue
<template>
  <div>
    <h1>{{ appTitle }}</h1>
    <p>{{ staticDescription }}</p>
  </div>
</template>
```

**Correct: rendered once**

```vue
<template>
  <div>
    <h1 v-once>{{ appTitle }}</h1>
    <p v-once>{{ staticDescription }}</p>
  </div>
</template>
```

### 6.2 v-memo for List Optimization

Use v-memo to skip re-rendering unchanged list items.

**Incorrect: all items re-render on any change**

```vue
<template>
  <div v-for="item in items" :key="item.id">
    <ExpensiveComponent :item="item" />
  </div>
</template>
```

**Correct: only changed items re-render**

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

### 6.3 KeepAlive for Expensive Components

Use KeepAlive to cache component state when toggling visibility.

**Incorrect: component destroyed and recreated**

```vue
<template>
  <component :is="currentTab" />
</template>
```

**Correct: component state preserved**

```vue
<template>
  <KeepAlive :max="10">
    <component :is="currentTab" />
  </KeepAlive>
</template>
```

**With include/exclude:**

```vue
<template>
  <KeepAlive :include="['Dashboard', 'Settings']">
    <component :is="currentTab" />
  </KeepAlive>
</template>
```

### 6.4 Teleport for Modals

Use Teleport to render modals at document root, avoiding z-index and overflow issues.

```vue
<template>
  <button @click="showModal = true">Open Modal</button>

  <Teleport to="body">
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <slot />
      </div>
    </div>
  </Teleport>
</template>
```

### 6.5 CSS content-visibility for Long Lists

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

### 6.6 Functional Components for Stateless UI

Use functional components for simple, stateless presentation.

```vue
<!-- FunctionalButton.vue -->
<script lang="ts">
export default defineComponent({
  functional: true,
  props: ['label', 'onClick'],
  setup(props) {
    return () => h('button', { onClick: props.onClick }, props.label)
  }
})
</script>

<!-- Or simply -->
<script setup lang="ts">
defineProps<{ label: string }>()
const emit = defineEmits<{ click: [] }>()
</script>

<template>
  <button @click="emit('click')">{{ label }}</button>
</template>
```

### 6.7 Use Explicit Conditional Rendering

Use v-if with explicit conditions instead of relying on falsy values.

**Incorrect: renders "0" when count is 0**

```vue
<template>
  <div>
    <span v-if="count" class="badge">{{ count }}</span>
  </div>
</template>
```

**Correct: explicit comparison**

```vue
<template>
  <div>
    <span v-if="count > 0" class="badge">{{ count }}</span>
  </div>
</template>
```

---

## 7. JavaScript Performance

**Impact: LOW-MEDIUM**

Micro-optimizations for hot paths can add up to meaningful improvements.

### 7.1 Batch DOM CSS Changes

Group multiple CSS changes together via classes.

**Incorrect: multiple style changes**

```typescript
function updateStyles(el: HTMLElement) {
  el.style.width = '100px'
  el.style.height = '200px'
  el.style.backgroundColor = 'blue'
}
```

**Correct: toggle class**

```typescript
function updateStyles(el: HTMLElement) {
  el.classList.add('highlighted-box')
}
```

### 7.2 Build Index Maps for Repeated Lookups

Multiple .find() calls by the same key should use a Map.

**Incorrect (O(n) per lookup):**

```typescript
function processOrders(orders: Order[], users: User[]) {
  return orders.map(order => ({
    ...order,
    user: users.find(u => u.id === order.userId)
  }))
}
```

**Correct (O(1) per lookup):**

```typescript
function processOrders(orders: Order[], users: User[]) {
  const userById = new Map(users.map(u => [u.id, u]))

  return orders.map(order => ({
    ...order,
    user: userById.get(order.userId)
  }))
}
```

### 7.3 Cache Property Access in Loops

Cache object property lookups in hot paths.

**Incorrect: 3 lookups × N iterations**

```typescript
for (let i = 0; i < arr.length; i++) {
  process(obj.config.settings.value)
}
```

**Correct: 1 lookup total**

```typescript
const value = obj.config.settings.value
const len = arr.length
for (let i = 0; i < len; i++) {
  process(value)
}
```

### 7.4 Cache Repeated Function Calls

Use a Map to cache function results.

```typescript
const slugCache = new Map<string, string>()

function getCachedSlug(text: string): string {
  if (!slugCache.has(text)) {
    slugCache.set(text, slugify(text))
  }
  return slugCache.get(text)!
}
```

### 7.5 Cache Storage API Calls

localStorage and sessionStorage are synchronous and expensive. Cache reads in memory.

```typescript
const storageCache = new Map<string, string | null>()

function getLocalStorage(key: string) {
  if (!storageCache.has(key)) {
    storageCache.set(key, localStorage.getItem(key))
  }
  return storageCache.get(key)
}

function setLocalStorage(key: string, value: string) {
  localStorage.setItem(key, value)
  storageCache.set(key, value)
}
```

### 7.6 Combine Multiple Array Iterations

Multiple .filter() calls iterate the array multiple times. Combine into one loop.

**Incorrect: 3 iterations**

```typescript
const admins = users.filter(u => u.isAdmin)
const testers = users.filter(u => u.isTester)
const inactive = users.filter(u => !u.isActive)
```

**Correct: 1 iteration**

```typescript
const admins: User[] = []
const testers: User[] = []
const inactive: User[] = []

for (const user of users) {
  if (user.isAdmin) admins.push(user)
  if (user.isTester) testers.push(user)
  if (!user.isActive) inactive.push(user)
}
```

### 7.7 Early Length Check for Array Comparisons

Check lengths first before expensive comparisons.

```typescript
function hasChanges(current: string[], original: string[]) {
  if (current.length !== original.length) {
    return true
  }
  // Only do expensive comparison when lengths match
  return current.some((item, i) => item !== original[i])
}
```

### 7.8 Early Return from Functions

Return early when result is determined.

**Incorrect: processes all items**

```typescript
function validateUsers(users: User[]) {
  let hasError = false
  for (const user of users) {
    if (!user.email) hasError = true
  }
  return !hasError
}
```

**Correct: returns immediately**

```typescript
function validateUsers(users: User[]) {
  for (const user of users) {
    if (!user.email) return false
  }
  return true
}
```

### 7.9 Hoist RegExp Creation

Don't create RegExp inside render or reactive computations.

**Incorrect: new RegExp every render**

```typescript
const highlighted = computed(() => {
  const regex = new RegExp(`(${query.value})`, 'gi')
  return text.value.replace(regex, '<mark>$1</mark>')
})
```

**Correct: memoize regex**

```typescript
const regex = computed(() => new RegExp(`(${query.value})`, 'gi'))

const highlighted = computed(() => {
  return text.value.replace(regex.value, '<mark>$1</mark>')
})
```

### 7.10 Use Loop for Min/Max Instead of Sort

Finding min/max only requires a single pass.

**Incorrect (O(n log n)):**

```typescript
function getLatest(items: Item[]) {
  return [...items].sort((a, b) => b.date - a.date)[0]
}
```

**Correct (O(n)):**

```typescript
function getLatest(items: Item[]) {
  if (items.length === 0) return null
  return items.reduce((latest, item) =>
    item.date > latest.date ? item : latest
  )
}
```

### 7.11 Use Set/Map for O(1) Lookups

Convert arrays to Set/Map for repeated membership checks.

**Incorrect (O(n) per check):**

```typescript
const allowedIds = ['a', 'b', 'c']
items.filter(item => allowedIds.includes(item.id))
```

**Correct (O(1) per check):**

```typescript
const allowedIds = new Set(['a', 'b', 'c'])
items.filter(item => allowedIds.has(item.id))
```

### 7.12 Use toSorted() Instead of sort()

.sort() mutates the array. Use .toSorted() for immutability.

**Incorrect: mutates original**

```typescript
const sorted = items.sort((a, b) => a.name.localeCompare(b.name))
```

**Correct: creates new array**

```typescript
const sorted = items.toSorted((a, b) => a.name.localeCompare(b.name))
```

---

## 8. Advanced Patterns

**Impact: LOW**

Advanced patterns for specific cases that require careful implementation.

### 8.1 Composables for Reusable Logic

Extract reusable logic into composables.

```typescript
// composables/useCounter.ts
export function useCounter(initial = 0) {
  const count = ref(initial)

  const increment = () => count.value++
  const decrement = () => count.value--
  const reset = () => count.value = initial

  return { count, increment, decrement, reset }
}

// Usage
const { count, increment } = useCounter(10)
```

### 8.2 provide/inject for Dependency Injection

Use provide/inject for deep prop drilling.

```typescript
// Parent component
const theme = ref('dark')
provide('theme', theme)

// Deep child component
const theme = inject('theme', ref('light'))
```

**With typed injection keys:**

```typescript
// keys.ts
import type { InjectionKey, Ref } from 'vue'

export const ThemeKey: InjectionKey<Ref<string>> = Symbol('theme')

// Parent
provide(ThemeKey, theme)

// Child
const theme = inject(ThemeKey)! // TypeScript knows it's Ref<string>
```

### 8.3 VueUse for Common Utilities

Leverage VueUse for common reactive utilities instead of reimplementing.

```typescript
import { useLocalStorage, useDark, useDebounce } from '@vueuse/core'

// Persistent storage with reactivity
const settings = useLocalStorage('settings', { theme: 'auto' })

// Dark mode toggle
const isDark = useDark()

// Debounced search
const search = ref('')
const debouncedSearch = useDebounce(search, 300)
```

---

## References

1. [https://vuejs.org](https://vuejs.org)
2. [https://nuxt.com](https://nuxt.com)
3. [https://vueuse.org](https://vueuse.org)
4. [https://vuejs.org/guide/extras/reactivity-in-depth.html](https://vuejs.org/guide/extras/reactivity-in-depth.html)
5. [https://nuxt.com/docs/guide/concepts/rendering](https://nuxt.com/docs/guide/concepts/rendering)
6. [https://nuxt.com/docs/api/composables/use-async-data](https://nuxt.com/docs/api/composables/use-async-data)
