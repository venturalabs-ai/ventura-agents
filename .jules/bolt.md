## 2024-06-25 - Avoid spreading Map and Set iterables
**Learning:** In this TypeScript codebase, spreading `Map` and `Set` iterables into arrays (e.g., `[...map.values()].filter(...)` or `[...set].map(...)`) to use array functional methods is an anti-pattern. It introduces unnecessary intermediate memory allocations and O(N) overhead.
**Action:** Iterate directly over `Map` and `Set` iterables using `for...of` loops to prevent this unnecessary overhead.
