## 2024-05-18 - Avoid Spreading Map and Set Iterables
**Learning:** Spreading `Map` and `Set` iterables into arrays (e.g. `[...map.values()].filter(...)`) to use array functional methods creates unnecessary intermediate memory allocations and O(N) overhead in this architecture.
**Action:** Always iterate directly using `for...of` loops to prevent these allocations.
