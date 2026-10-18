## 2024-05-18 - [Spreading Iterables Anti-pattern]
**Learning:** [In this TypeScript codebase, avoiding the anti-pattern of spreading `Map` and `Set` iterables into arrays (e.g. `[...map.values()].filter(...)`) to use array functional methods is critical. Iterating directly using `for...of` loops prevents unnecessary intermediate memory allocations and O(N) overhead.]
**Action:** [Use direct `for...of` loops instead of spreading iterables to prevent unnecessary memory allocations and overhead.]
