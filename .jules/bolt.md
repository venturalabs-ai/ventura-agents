## 2024-10-24 - [Avoid Array Spread on Iterables]
**Learning:** Spreading map/set iterables into arrays (e.g., `[...map.values()].filter(...)`) creates unnecessary intermediate memory allocations and adds O(N) overhead compared to a direct `for...of` iteration.
**Action:** Iterate directly over Maps and Sets using `for...of` loops to prevent unnecessary allocations, adhering strictly to the memory guidelines for the codebase.
