## 2026-10-14 - Avoid Spreading Map/Set Iterables
**Learning:** Spreading Map and Set iterables into arrays (e.g., `[...map.values()].filter(...)`) creates unnecessary intermediate memory allocations and adds O(N) overhead to what could be done directly in a loop.
**Action:** Iterate directly using `for...of` loops to prevent unnecessary intermediate memory allocations and O(N) overhead.
