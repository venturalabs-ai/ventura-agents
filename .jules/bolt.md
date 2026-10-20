## 2024-10-21 - Map/Set Spread Anti-Pattern
**Learning:** Found multiple instances where `Map.values()` and `Set` were being spread into arrays `[...map.values()]` just to run `.filter()` or `.map()` over them. This creates unnecessary intermediate memory allocations and adds O(N) overhead.
**Action:** Always iterate directly over Map/Set iterables using `for...of` loops rather than spreading them into temporary arrays.
