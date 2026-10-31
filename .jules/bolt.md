## 2024-05-15 - [Avoid Map and Set spreading anti-pattern]
**Learning:** [Spreading Maps and Sets into arrays (e.g., `[...map.values()].filter(...)`) creates unnecessary intermediate memory allocations and introduces O(N) memory and time overhead.]
**Action:** [Always iterate directly over `Map` and `Set` elements using `for...of` loops and build output arrays or promises explicitly, avoiding the spread operator on these iterables for functional methods.]
