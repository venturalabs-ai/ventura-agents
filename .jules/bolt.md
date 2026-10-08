## 2023-10-08 - Array Spread Anti-Pattern
**Learning:** Spreading `Map` and `Set` iterables into arrays (e.g., `[...map.values()].filter(...)`) just to use array functional methods creates unnecessary intermediate array allocations, resulting in O(N) memory overhead and performance degradation.
**Action:** Avoid this anti-pattern. Instead, iterate directly using `for...of` loops to process `Map` and `Set` values efficiently without creating intermediate arrays.
