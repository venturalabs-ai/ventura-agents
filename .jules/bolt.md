## 2024-05-15 - Array Method Chaining Overhead
**Learning:** Chaining array methods like `.filter().map().filter()` or spreading Iterables (`[...map.values()]`) creates significant temporary object allocation and O(N) overhead in hot paths.
**Action:** Replace iterable spreads and array method chains with single-pass `for...of` loops that push valid items directly to a result array to improve memory efficiency and execution speed without losing readability.
