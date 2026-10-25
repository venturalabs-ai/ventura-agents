
## 2026-10-25 - Avoid spreading Iterables into Arrays for filtering
**Learning:** The codebase has multiple occurrences of spreading Map/Set iterables into Arrays just to use Array functional methods (e.g., `[...map.values()].filter(...)`). This creates unnecessary intermediate arrays and O(N) overhead in memory allocation and iteration time. We also saw array functional methods `.filter(...).map(...).filter(...)` which iterates multiple times.
**Action:** Use standard `for...of` loops instead of spreading `Map` and `Set` iterables to arrays for functional methods in TypeScript projects where performance is critical. Also avoid chaining array methods on large arrays.
