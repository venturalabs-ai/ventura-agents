## 2026-10-04 - Optimize Map and Set Iterations
**Learning:** In TypeScript, spreading `Map` or `Set` values/entries into arrays (e.g., `[...map.values()].filter(...)` or `[...set].map(...)`) is a performance anti-pattern. It forces unnecessary O(N) memory allocations for the intermediate arrays and adds GC overhead, especially when methods like `.filter()` or `.map()` create yet another array.
**Action:** Use direct `for...of` iteration to push elements conditionally into a target array or process them inline. This avoids intermediate array creations while achieving the exact same result.
