## 2026-09-27 - [Optimize Iterables Memory Allocation]
**Learning:** [Spreading Maps and Sets into arrays using `[...iterable.values()]` creates an unnecessary O(N) memory allocation and processing overhead, which is bad practice especially when chaining `.filter()` or similar methods on high-volume collections.]
**Action:** [Use direct `for...of` iteration over iterables to avoid intermediate array allocations.]
