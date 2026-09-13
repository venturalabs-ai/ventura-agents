## 2024-09-13 - [O(E) Graph Traversal Bottleneck in KnowledgeGraph]
**Learning:** The flat `edges: Edge[]` array in the `KnowledgeGraph` class created an O(E) complexity bottleneck in the `neighbors` lookup, because traversing neighbors for a single node required filtering across the entire edge dataset. In a highly connected graph, this scales poorly.
**Action:** Always index relations (such as graph edges) by their source (e.g., in a `Map<sourceId, Edge[]>`) to enable O(1) adjacency list lookups instead of scanning all relations sequentially.
