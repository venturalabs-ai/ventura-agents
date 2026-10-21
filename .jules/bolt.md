## 2026-10-21 - Avoid Map/Set spread anti-pattern
**Learning:** Spreading Maps and Sets into arrays using `[...map.values()]` or similar to use array functional methods creates unnecessary intermediate memory allocations and O(N) array creation overhead in this TypeScript codebase.
**Action:** Use direct `for...of` loops to iterate over `Map` and `Set` iterables to prevent memory bloat and improve execution time.
