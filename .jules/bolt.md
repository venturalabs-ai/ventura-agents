
## 2026-09-29 - Array Spread Iteration Anti-Pattern
**Learning:** Spreading Map/Set iterables into arrays just to use functional methods like `.filter()` or `.map()` forces immediate execution and O(N) intermediate memory allocation.
**Action:** Use direct `for...of` iteration to filter and accumulate values, significantly reducing unnecessary memory allocations and overhead.
