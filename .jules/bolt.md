## 2026-11-07 - Prevent spreading iterables into arrays
**Learning:** Spreading Map and Set iterables into arrays (e.g. `[...map.values()]`) is an anti-pattern when we can just iterate directly with `for...of`.
**Action:** Iterate directly over Maps and Sets instead of spreading them into arrays to avoid unnecessary intermediate allocations and O(N) overhead.
