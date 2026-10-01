## 2024-05-18 - [Avoid Map/Set spread allocations]
**Learning:** In this TypeScript codebase, spreading `Map` and `Set` iterables into arrays (e.g. `[...map.values()].filter(...)`) to use array functional methods creates unnecessary intermediate memory allocations and O(N) overhead.
**Action:** Iterate directly using `for...of` loops to prevent unnecessary intermediate memory allocations and O(N) overhead.
