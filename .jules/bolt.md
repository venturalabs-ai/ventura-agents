## 2024-10-18 - [KnowledgeGraph Out-Degree Index]
**Learning:** Graph traversals iterating over all edges are a major performance bottleneck for highly connected graphs.
**Action:** Use adjacency list representations (e.g., mapping source IDs to out-edges) to transform O(E) neighbor lookups to O(deg(V)), significantly boosting retrieval speed.
