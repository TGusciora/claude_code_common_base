---
title: VueUse for Common Utilities
impact: LOW
impactDescription: avoid reinventing common utilities
tags: advanced, vueuse, utilities, composables
---

## VueUse for Common Utilities

Leverage VueUse for common reactive utilities instead of reimplementing.

```typescript
import {
  useLocalStorage,
  useDark,
  useDebounce,
  useIntersectionObserver,
  useEventListener
} from '@vueuse/core'

// Persistent storage with reactivity
const settings = useLocalStorage('settings', { theme: 'auto' })

// Dark mode toggle
const isDark = useDark()

// Debounced search
const search = ref('')
const debouncedSearch = useDebounce(search, 300)

// Intersection observer
const target = ref<HTMLElement | null>(null)
const { isIntersecting } = useIntersectionObserver(target)

// Event listeners with auto cleanup
useEventListener(window, 'resize', handleResize)
```

**Common utilities to use:**

- `useLocalStorage` / `useSessionStorage` - Reactive storage
- `useDebounce` / `useThrottle` - Rate limiting
- `useFetch` - Reactive fetch wrapper
- `useInfiniteScroll` - Infinite scrolling
- `useVirtualList` - Virtual scrolling
- `useDark` - Dark mode
- `useMediaQuery` - Responsive queries

Reference: [VueUse](https://vueuse.org)
