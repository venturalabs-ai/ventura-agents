## 2024-05-18 - Optimize Map Iteration
**Learning:** Avoid spreading `Map` and `Set` iterables into arrays (e.g. `[...map.values()].filter(...)`) to use array functional methods. This creates unnecessary intermediate memory allocations and O(N) overhead.
**Action:** Iterate directly using `for...of` loops to prevent this unnecessary allocation, particularly for internal registries and caches.
