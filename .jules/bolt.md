## 2024-09-15 - [Avoid spreading maps and sets for Array methods]
**Learning:** The codebase heavily relies on spreading `Map` and `Set` iterables into arrays (e.g. `[...map.values()].filter(...)`) simply to use array functional methods. This causes unnecessary intermediate array allocations, memory spikes, and an O(N) memory/time overhead.
**Action:** Always iterate directly over the `Map` or `Set` iterables with `for...of` loops, pushing matching items to a single result array. This eliminates the intermediate allocations and multiple iteration passes.
