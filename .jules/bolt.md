
## 2026-11-11 - Map/Set Iterable Spreading Anti-Pattern
**Learning:** Spreading Map and Set iterables into arrays (e.g. `[...map.values()].filter(...)`) to use array methods causes unnecessary intermediate memory allocations and O(N) overhead in this architecture.
**Action:** Iterate directly over Map and Set iterables using `for...of` loops to preserve memory efficiency, and pass collected results appropriately (e.g., to `Promise.all`).
