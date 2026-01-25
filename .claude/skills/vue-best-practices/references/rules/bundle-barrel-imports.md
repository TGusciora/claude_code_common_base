---
title: Avoid Barrel File Imports
impact: CRITICAL
impactDescription: 15-70% faster dev boot, 28% faster builds
tags: bundle, imports, tree-shaking, optimization
---

## Avoid Barrel File Imports

Import directly from source files instead of barrel files to avoid loading unused modules.

**Incorrect (imports entire library):**

```typescript
import { Check, X, Menu } from 'lucide-vue-next'
// Loads 1,500+ modules

import { Button, TextField } from '@headlessui/vue'
// Loads entire component library
```

**Correct (imports only what you need):**

```typescript
import Check from 'lucide-vue-next/dist/esm/icons/check'
import X from 'lucide-vue-next/dist/esm/icons/x'
import Menu from 'lucide-vue-next/dist/esm/icons/menu'
// Loads only 3 modules

import Button from '@headlessui/vue/dist/components/button/button'
// Loads only what you use
```

Libraries commonly affected: `lucide-vue-next`, `@headlessui/vue`, `@heroicons/vue`, `vue-icons`, `lodash`, `date-fns`, `rxjs`, `vueuse`.
