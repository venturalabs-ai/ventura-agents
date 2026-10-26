## 2024-05-18 - [Spreading Iterables Anti-Pattern]
**Learning:** Spreading Map or Set iterables into arrays (e.g., `[...map.values()].filter(...)`) just to use functional array methods introduces unnecessary O(N) memory allocations and iteration overhead, significantly impacting performance in frequently called loops.
**Action:** Always iterate directly over Maps and Sets using `for...of` loops, collecting results directly, rather than spreading them into intermediate arrays.
