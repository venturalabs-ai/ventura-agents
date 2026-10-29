
## 2024-10-30 - [Performance Anti-Pattern: Spreading Maps and Sets]
**Learning:** Avoid the anti-pattern of spreading `Map` and `Set` iterables into arrays (e.g. `[...map.values()].filter(...)`) just to use array functional methods. This creates unnecessary intermediate memory allocations and introduces O(N) overhead.
**Action:** Iterate directly using `for...of` loops instead of spreading when working with Maps and Sets in TypeScript.
