
## 2025-02-14 - [Avoid Map/Set Iterable Spread Overhead]
**Learning:** Spreading iterables from `Map` or `Set` (e.g. `[...map.values()].filter(...)` or `[...set].map(...)`) into arrays purely to use array methods causes a massive, unnecessary O(N) memory allocation and overhead. It creates intermediate garbage collections that drag down performance, especially in hot paths or large collections.
**Action:** Always iterate over `Map` and `Set` collections directly using `for...of` loops, executing filtering or mapping logic within the loop, and pushing only the final results to a new array when an array is strictly needed.
