---
title: Build Index Maps for Repeated Lookups
impact: LOW-MEDIUM
impactDescription: O(n) -> O(1) per lookup
tags: js, map, lookup, performance
---

## Build Index Maps for Repeated Lookups

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

For 1000 orders x 1000 users: 1M ops -> 2K ops.
