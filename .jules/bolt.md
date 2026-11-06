
## 2024-11-06 - Avoid spreading Sets and Maps in hot paths
**Learning:** In TypeScript, spreading `Set.values()`, `Map.values()`, or iterables using `[...iterable]` into an array just to use functional array methods (like `.map` or `.filter`) incurs unnecessary intermediate memory allocations and O(N) overhead.
**Action:** When filtering or mapping data from a `Set` or `Map`, iterate over the iterable directly using a `for...of` loop and push matching/transformed elements to an array, bypassing the intermediate array creation.
