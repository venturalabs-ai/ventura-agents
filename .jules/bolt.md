
## 2026-10-12 - Avoid spreading Map and Set iterables into arrays for filtering
**Learning:** In this TypeScript codebase, a common anti-pattern was found where `Map` iterables were spread into arrays (e.g., `[...map.values()].filter(...)`) just to use functional array methods like `filter`. This causes unnecessary intermediate memory allocations and introduces O(N) overhead during the array creation before the filtering even happens.
**Action:** When filtering or iterating over `Map` or `Set` values, always iterate directly using `for...of` loops. This prevents the unnecessary O(N) memory allocation and overhead of converting the entire iterable to an array first.
