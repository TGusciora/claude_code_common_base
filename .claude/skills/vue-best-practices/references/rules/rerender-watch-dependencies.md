---
title: Narrow Watch Dependencies
impact: MEDIUM
impactDescription: reduces unnecessary watcher executions
tags: rerender, watch, dependencies, optimization
---

## Narrow Watch Dependencies

Watch specific properties instead of entire objects.

**Incorrect (re-runs on any user field change):**

```typescript
watch(user, (newUser) => {
  console.log('User changed:', newUser.id)
})
```

**Correct (re-runs only when id changes):**

```typescript
watch(() => user.value.id, (newId) => {
  console.log('User ID changed:', newId)
})
```

**For multiple specific properties:**

```typescript
watch(
  () => [user.value.id, user.value.role],
  ([newId, newRole]) => {
    updatePermissions(newId, newRole)
  }
)
```

**For derived boolean state:**

```typescript
// Incorrect: runs on width=767, 766, 765...
watch(windowWidth, (width) => {
  if (width < 768) enableMobileMode()
})

// Correct: runs only on boolean transition
const isMobile = computed(() => windowWidth.value < 768)
watch(isMobile, (mobile) => {
  if (mobile) enableMobileMode()
})
```
