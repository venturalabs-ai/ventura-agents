
## 2024-05-14 - Map/Set Iterable Filtering Anti-Pattern
**Learning:** Spreading `Map` or `Set` iterables into arrays (e.g., `[...map.values()].filter(...)`) to use array functional methods incurs unnecessary O(N) overhead due to intermediate memory allocations.
**Action:** Always iterate over `Map` or `Set` values directly using `for...of` loops, collecting required elements into a new array.
