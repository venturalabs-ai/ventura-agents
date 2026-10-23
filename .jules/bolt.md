## 2026-10-23 - Optimize Map/Set Iterations
**Learning:** Spreading `Map` and `Set` iterables into arrays (e.g., `[...map.values()].filter(...)`) just to use array functional methods creates unnecessary intermediate memory allocations and introduces O(N) overhead.
**Action:** Iterate directly using `for...of` loops to prevent this unnecessary overhead.
