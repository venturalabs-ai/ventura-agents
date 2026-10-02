## 2024-10-02 - [Iterating Iterables without Spreading]
**Learning:** Avoid the anti-pattern of spreading `Map` and `Set` iterables into arrays (e.g., `[...map.values()].filter(...)`) to use array functional methods. This creates unnecessary intermediate memory allocations and incurs O(N) overhead.
**Action:** Iterate directly using `for...of` loops to prevent unnecessary intermediate memory allocations and overhead when working with `Map` and `Set` collections.
