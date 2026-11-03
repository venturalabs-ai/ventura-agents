
## 2024-11-03 - Avoiding Map/Set spread allocations
**Learning:** Spreading Map or Set iterables into arrays (e.g. `[...map.values()]`) just to use functional array methods like `.filter()` or `.map()` creates unnecessary intermediate memory allocations and adds O(N) overhead in hot paths.
**Action:** Always iterate over Map or Set iterables directly using `for...of` loops to build the resulting array, eliminating the intermediate array allocation.
