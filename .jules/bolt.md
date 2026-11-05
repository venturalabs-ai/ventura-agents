## 2024-05-24 - Avoid Map/Set iterable spreading
**Learning:** Spreading Map and Set iterables into arrays (e.g. `[...map.values()].filter(...)`) to use array functional methods causes unnecessary intermediate memory allocations and O(N) overhead.
**Action:** Iterate directly using `for...of` loops instead of spreading iterables into arrays to prevent unnecessary allocations.
