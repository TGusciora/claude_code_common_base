---
title: provide/inject for Dependency Injection
impact: LOW
impactDescription: avoids prop drilling
tags: advanced, provide, inject, dependency-injection
---

## provide/inject for Dependency Injection

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

**With default factory:**

```typescript
const config = inject('config', () => createDefaultConfig(), true)
```

Reference: [Vue provide/inject](https://vuejs.org/guide/components/provide-inject.html)
