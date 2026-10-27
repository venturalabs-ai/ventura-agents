
## 2024-05-24 - Avoid spreading Map iterables for filtering
**Learning:** Spreading Map and Set iterables into arrays (e.g. [...map.values()].filter(...)) to use array functional methods incurs unnecessary intermediate memory allocations and O(N) overhead.
**Action:** Iterate directly using for...of loops instead of spreading when extracting and filtering values from Map or Set.
