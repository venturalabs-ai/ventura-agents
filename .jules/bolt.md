
## 2023-10-24 - Avoiding Iterator Spreads
**Learning:** Spreading `Map` or `Set` iterables into arrays (e.g., `[...map.values()].filter(...)`) to use array methods causes unnecessary intermediate memory allocations and O(N) overhead.
**Action:** Iterate directly using `for...of` loops instead of spreading into arrays.
