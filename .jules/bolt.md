## 2026-10-06 - [Avoid Spreading Iterables]
**Learning:** Spreading Map or Set iterables into arrays (e.g., `[...map.values()].filter(...)`) creates unnecessary intermediate O(N) memory allocations just to use array functional methods.
**Action:** Iterate directly over the iterables using `for...of` loops and construct the necessary data structures iteratively to reduce memory overhead and improve performance.
