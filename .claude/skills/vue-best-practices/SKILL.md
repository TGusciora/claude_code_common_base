---
name: vue-best-practices
description: Comprehensive Vue 3 and Nuxt 3 performance optimization guide with 40+ rules for eliminating waterfalls, optimizing bundles, and improving rendering. Use when optimizing Vue apps, reviewing performance, or refactoring components.
version: 1.0.0
author: Vue/Nuxt Community
license: MIT
tags: [Vue, Nuxt, Performance, Optimization, SSR, Composition API, Server Components]
dependencies: []
---

# Vue Best Practices - Performance Optimization

Comprehensive performance optimization guide for Vue 3 and Nuxt 3 applications with 40+ rules organized by impact level. Designed to help developers eliminate performance bottlenecks and follow best practices.

## When to use this skill

**Use Vue Best Practices when:**
- Optimizing Vue 3 or Nuxt 3 application performance
- Reviewing code for performance improvements
- Refactoring existing components for better performance
- Implementing new features with performance in mind
- Debugging slow rendering or loading issues
- Reducing bundle size
- Eliminating request waterfalls

**Key areas covered:**
- **Eliminating Waterfalls** (CRITICAL): Prevent sequential async operations
- **Bundle Size Optimization** (CRITICAL): Reduce initial JavaScript payload
- **Server-Side Performance** (HIGH): Optimize Nuxt SSR and data fetching
- **Client-Side Data Fetching** (MEDIUM-HIGH): Implement efficient caching
- **Re-render Optimization** (MEDIUM): Minimize unnecessary re-renders
- **Rendering Performance** (MEDIUM): Optimize browser rendering
- **JavaScript Performance** (LOW-MEDIUM): Micro-optimizations for hot paths
- **Advanced Patterns** (LOW): Specialized techniques for edge cases

## Quick reference

### Critical priorities

1. **Use Promise.all with useAsyncData** - Parallelize independent data fetching
2. **Use defineAsyncComponent** - Lazy-load heavy components
3. **Avoid barrel imports** - Import directly from source files
4. **Use shallowRef for large objects** - Prevent deep reactivity overhead
5. **Strategic Suspense boundaries** - Stream content while showing layout

### Common patterns

**Parallel data fetching:**
```typescript
const [{ data: user }, { data: posts }, { data: comments }] = await Promise.all([
  useAsyncData('user', () => fetchUser()),
  useAsyncData('posts', () => fetchPosts()),
  useAsyncData('comments', () => fetchComments())
])
```

**Direct imports:**
```typescript
// Bad - Loads entire library
import { Check } from 'lucide-vue-next'

// Good - Loads only what you need
import Check from 'lucide-vue-next/dist/esm/icons/check'
```

**Async components:**
```typescript
import { defineAsyncComponent } from 'vue'

const MonacoEditor = defineAsyncComponent(
  () => import('./MonacoEditor.vue')
)
```

## Using the guidelines

The complete performance guidelines are available in the references folder:

- **vue-performance-guidelines.md**: Complete guide with all 40+ rules, code examples, and impact analysis

Each rule includes:
- Incorrect/correct code comparisons
- Specific impact metrics
- When to apply the optimization
- Real-world examples

## Categories overview

### 1. Eliminating Waterfalls (CRITICAL)
Waterfalls are the #1 performance killer. Each sequential await adds full network latency.
- Use Promise.all with useAsyncData/useFetch
- Dependency-based parallelization
- Prevent waterfall chains in server routes
- Strategic Suspense boundaries
- Defer await until needed

### 2. Bundle Size Optimization (CRITICAL)
Reducing initial bundle size improves Time to Interactive and Largest Contentful Paint.
- Avoid barrel file imports
- Use defineAsyncComponent for heavy components
- Leverage Nuxt auto-imports (no manual imports needed)
- Conditional module loading
- Preload based on user intent

### 3. Server-Side Performance (HIGH)
Optimize Nuxt SSR, Nitro caching, and data fetching.
- Use Nitro routeRules for caching
- Hybrid rendering with routeRules
- Minimize serialization at server/client boundary
- Cross-request caching with cachedEventHandler

### 4. Client-Side Data Fetching (MEDIUM-HIGH)
Automatic deduplication and efficient data fetching patterns.
- Use useFetch for automatic deduplication
- Leverage ClientOnly for browser-specific content
- SWR-like patterns with stale-while-revalidate

### 5. Re-render Optimization (MEDIUM)
Reduce unnecessary re-renders to minimize wasted computation.
- Use shallowRef for large objects
- Computed properties for derived state
- watchEffect cleanup patterns
- Proper watch dependency management

### 6. Rendering Performance (MEDIUM)
Optimize the browser rendering process.
- Use v-once for static content
- Use v-memo for list optimization
- KeepAlive for expensive components
- Teleport for modal/popup optimization
- CSS content-visibility for long lists

### 7. JavaScript Performance (LOW-MEDIUM)
Micro-optimizations for hot paths.
- Batch DOM CSS changes
- Build index maps for repeated lookups
- Cache property access in loops
- Use Set/Map for O(1) lookups
- Early return from functions

### 8. Advanced Patterns (LOW)
Specialized techniques for edge cases.
- Composables for reusable logic
- provide/inject for dependency injection
- VueUse for common utilities
- Custom directives for DOM manipulation

## Implementation approach

When optimizing a Vue application:

1. **Profile first**: Use Vue DevTools and browser performance tools to identify bottlenecks
2. **Focus on critical paths**: Start with eliminating waterfalls and reducing bundle size
3. **Measure impact**: Verify improvements with metrics (LCP, TTI, FID)
4. **Apply incrementally**: Don't over-optimize prematurely
5. **Test thoroughly**: Ensure optimizations don't break functionality

## Key metrics to track

- **Time to Interactive (TTI)**: When page becomes fully interactive
- **Largest Contentful Paint (LCP)**: When main content is visible
- **First Input Delay (FID)**: Responsiveness to user interactions
- **Cumulative Layout Shift (CLS)**: Visual stability
- **Bundle size**: Initial JavaScript payload
- **Server response time**: TTFB for server-rendered content

## Common pitfalls to avoid

**Don't:**
- Use barrel imports from large libraries
- Block parallel operations with sequential awaits
- Make every ref deeply reactive when shallowRef suffices
- Load analytics/tracking in the critical path
- Mutate arrays with .sort() instead of .toSorted()
- Create RegExp or heavy objects inside render functions

**Do:**
- Import directly from source files
- Use Promise.all() for independent operations
- Use shallowRef/shallowReactive for large data structures
- Lazy-load non-critical code with defineAsyncComponent
- Use immutable array methods
- Hoist static objects outside components

## Resources

- [Vue 3 Documentation](https://vuejs.org)
- [Nuxt 3 Documentation](https://nuxt.com)
- [VueUse](https://vueuse.org)
- [Nuxt Performance Guide](https://nuxt.com/docs/guide/concepts/rendering)
- [Vue Reactivity in Depth](https://vuejs.org/guide/extras/reactivity-in-depth.html)

## Version history

**v1.0.0** (January 2026)
- Initial release
- 40+ performance rules across 8 categories
- Comprehensive code examples and impact analysis
