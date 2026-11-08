## 2024-05-18 - Avoid spreading Map and Set Iterables
**Learning:** Spreading Maps or Sets into arrays before filtering/mapping creates intermediate arrays causing O(N) memory allocations and iteration overhead, which can be an anti-pattern in TypeScript when functional methods are used.
**Action:** Iterate directly over Iterables using `for...of` loops to perform filtering and mapping in a single pass without intermediate array allocations.
