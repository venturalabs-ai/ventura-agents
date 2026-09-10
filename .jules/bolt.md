## 2024-03-24 - Intermediate Array Allocations
**Learning:** Found chained array methods (`.filter().map().filter()`) in hot paths like graph traversals (`KnowledgeGraph.neighbors`), which allocate intermediate arrays and require multiple passes.
**Action:** Replace multi-pass chained array methods with a single `for...of` loop in frequently called methods to reduce memory overhead and redundant iterations.
