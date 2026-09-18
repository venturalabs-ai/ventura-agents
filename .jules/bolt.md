## 2024-09-19 - Avoid Spreading Iterables in TypeScript

**Learning:** Spreading `Map` and `Set` iterables into arrays (e.g., `[...map.values()].filter(...)`) just to use array functional methods like `filter` or `map` causes unnecessary intermediate memory allocations and O(N) overhead in this Node.js application.
**Action:** Iterate directly using `for...of` loops and manually push to a result array. This provides identical functionality while significantly reducing memory churn during hot paths like event publishing or registry lookups.
