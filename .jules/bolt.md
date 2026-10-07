
## 2026-10-07 - Avoid spreading Map/Set Iterables into Arrays for Filtering
**Learning:** The codebase previously contained anti-patterns like `[...map.values()].filter(...)`. This creates an unnecessary, short-lived intermediate array of the entire Map's values, leading to O(N) memory allocation overhead before the actual filtering occurs. This is particularly wasteful for large Maps where only a few items match the filter condition.
**Action:** When filtering or mapping over values from a `Map` or `Set`, always iterate directly over the iterable using a `for...of` loop and construct the resulting array manually, rather than spreading the iterable into a temporary array just to use array functional methods.
