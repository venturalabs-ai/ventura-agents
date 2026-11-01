
## 2026-11-01 - Avoid spreading Map/Set iterables for filtering
**Learning:** Spreading Map or Set iterables into arrays (e.g., `[...map.values()].filter(...)`) creates unnecessary intermediate arrays, allocating extra memory and causing O(N) overhead before the filtering even happens.
**Action:** When filtering values from a Map or Set in TypeScript, use a direct `for...of` loop to iterate over the values and conditionally add them to the result array.
