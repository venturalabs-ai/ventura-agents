## 2024-05-24 - Avoid spreading iterables
**Learning:** Spreading Map or Set iterables into arrays (e.g. [...map.values()].filter(...)) to use array functional methods causes unnecessary intermediate memory allocations and O(N) overhead.
**Action:** Iterate directly using for...of loops instead.
