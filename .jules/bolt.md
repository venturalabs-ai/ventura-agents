
## 2024-05-14 - Iterate Iterables Directly
**Learning:** In TypeScript, spreading `Map` and `Set` iterables into arrays (e.g. `[...map.values()].filter(...)` or `[...set].map(...)`) just to use functional array methods introduces unnecessary intermediate memory allocations and O(N) overhead.
**Action:** Always iterate `Map` and `Set` directly using `for...of` loops and build up output arrays (e.g. `const result = []; for (const item of iterable) { ... }`) to prevent unnecessary intermediate memory allocation.
