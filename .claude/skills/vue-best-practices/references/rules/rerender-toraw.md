---
title: toRaw for Read-Only Access
impact: MEDIUM
impactDescription: avoids reactivity tracking overhead
tags: rerender, toRaw, reactivity, performance
---

## toRaw for Read-Only Access

Use toRaw when you need to read reactive data without triggering tracking.

**Incorrect (triggers unnecessary tracking):**

```typescript
function logItems() {
  // Every property access is tracked
  console.log(JSON.stringify(items.value))
}

function sendToAnalytics() {
  // Tracking overhead for read-only operation
  analytics.track('items', items.value)
}
```

**Correct (no tracking overhead):**

```typescript
import { toRaw } from 'vue'

function logItems() {
  // No reactivity tracking
  console.log(JSON.stringify(toRaw(items.value)))
}

function sendToAnalytics() {
  // No tracking overhead
  analytics.track('items', toRaw(items.value))
}
```

**Common use cases:**

```typescript
// Passing to external libraries
externalLib.process(toRaw(data.value))

// Deep cloning
const clone = structuredClone(toRaw(items.value))

// Comparison operations
if (isEqual(toRaw(a.value), toRaw(b.value))) {
  // ...
}
```

Reference: [Vue toRaw](https://vuejs.org/api/reactivity-advanced.html#toraw)
