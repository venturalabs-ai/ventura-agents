## 2024-11-23 - Avoiding Map/Set iterator spread overhead in hot paths
**Learning:** Using the spread operator on Map/Set iterables (e.g., `[...map.values()].filter(...)`) creates intermediate arrays and involves implicit memory allocation with O(N) memory overhead. In this codebase, it's an anti-pattern.
**Action:** Iterate directly over Maps and Sets using `for...of` loops rather than converting them to arrays for functional methods like `.filter()` or `.map()` to preserve memory performance.
