## 2026-10-03 - [TypeScript Memory Optimizations]
**Learning:** In this TypeScript codebase, avoid the anti-pattern of spreading Map and Set iterables into arrays (e.g. `[...map.values()].filter(...)`) to use array functional methods. It creates unnecessary intermediate memory allocations and O(N) overhead.
**Action:** Iterate directly using `for...of` loops instead.
