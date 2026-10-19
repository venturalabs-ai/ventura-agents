## 2025-02-12 - Memory Allocation Anti-Pattern (Iterable Spread)
**Learning:** Spreading iterables like Maps and Sets into Arrays just to use functional array methods (e.g. `[...map.values()].filter(...)` or `[...set].map(...)`) introduces unnecessary intermediate memory allocations and O(N) overhead.
**Action:** Always iterate directly over Maps and Sets using `for...of` loops to perform filtering or mapping logic in place, saving memory allocations.
