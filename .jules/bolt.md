
## 2024-10-28 - [TypeScript Iterables Performance Pattern]
**Learning:** [Spreading `Map` and `Set` iterables into arrays (e.g. `[...map.values()].filter(...)`) to use array functional methods incurs unnecessary intermediate memory allocations and O(N) overhead.]
**Action:** [Iterate directly using `for...of` loops to prevent this unnecessary memory allocation and improve performance. Be careful to ensure correct typing when doing this, avoiding the anti-pattern of dropping non-native 'thenable' objects for Promise.all.]
