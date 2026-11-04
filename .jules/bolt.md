## 2026-11-04 - [Iterator Spread Anti-pattern Optimization]
**Learning:** Spreading Map/Set values into arrays (e.g. `[...map.values()].filter(...)`) creates unnecessary intermediate arrays and O(N) memory allocation overhead in TypeScript/V8.
**Action:** Use direct `for...of` iteration to collect results when filtering or mapping Map/Set iterables, rather than spreading and using array methods.
