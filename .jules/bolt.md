## 2024-05-24 - Avoid spreading iterables into arrays in TypeScript
**Learning:** In TypeScript codebases, spreading `Map` and `Set` iterables into arrays (e.g., `[...map.values()].filter(...)`) to use array functional methods creates unnecessary intermediate memory allocations and O(N) overhead.
**Action:** Iterate directly over the `Map` or `Set` using `for...of` loops to prevent this performance anti-pattern.
