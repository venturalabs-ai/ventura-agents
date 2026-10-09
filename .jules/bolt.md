## 2024-10-09 - Avoid spreading Map/Set iterables for performance
**Learning:** Spreading `Map` and `Set` iterables into arrays (e.g., `[...map.values()].filter(...)`) to use array functional methods creates unnecessary intermediate memory allocations and introduces O(N) overhead.
**Action:** Iterate directly using `for...of` loops to prevent these memory allocations and overhead.
