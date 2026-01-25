---
title: Use Explicit Conditional Rendering
impact: MEDIUM
impactDescription: avoids unexpected rendering of falsy values
tags: rendering, v-if, conditional, falsy
---

## Use Explicit Conditional Rendering

Use v-if with explicit conditions instead of relying on falsy values.

**Incorrect (renders "0" when count is 0):**

```vue
<template>
  <div>
    <span v-if="count" class="badge">{{ count }}</span>
  </div>
</template>
```

**Correct (explicit comparison):**

```vue
<template>
  <div>
    <span v-if="count > 0" class="badge">{{ count }}</span>
  </div>
</template>
```

**Other examples:**

```vue
<template>
  <!-- Incorrect: shows "0" or empty string -->
  <span v-if="items.length">{{ items.length }} items</span>

  <!-- Correct: explicit check -->
  <span v-if="items.length > 0">{{ items.length }} items</span>

  <!-- Incorrect: shows "null" text in some edge cases -->
  <span v-if="user?.name">{{ user.name }}</span>

  <!-- Correct: explicit null check -->
  <span v-if="user?.name != null">{{ user.name }}</span>
</template>
```
