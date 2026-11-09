## 2024-11-09 - Avoid spreading Map/Set iterables for functional array methods
**Learning:** Spreading Map or Set iterables into arrays (e.g., `[...map.values()].filter(...)`) simply to use functional array methods is an anti-pattern. It incurs O(N) memory overhead for intermediate allocations and performance costs.
**Action:** Instead, iterate over collections directly using `for...of` loops and build output arrays sequentially to maintain high performance with lower memory footprint.
