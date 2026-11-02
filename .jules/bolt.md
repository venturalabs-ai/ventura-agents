
## 2024-11-02 - [Avoid Spreading Iterables in TypeScript]
**Learning:** [Spreading iterables from `Map` or `Set` objects into arrays using `[...map.values()]` or `[...set.values()]` prior to looping in order to use array functional methods like `filter` or `map` is an anti-pattern. This results in unnecessary, intermediate O(N) memory allocations and iteration overhead.]
**Action:** [Instead of spreading, always use `for...of` loops to iterate directly over the map/set values. Collect the resulting elements (if needed) by manually pushing them into an array during the loop. This minimizes overhead, speeds up processing for large maps, and preserves readability.]
