## 2024-06-25 - Graph Query Performance (O(N) vs O(1))
**Learning:** In `KnowledgeGraph`, storing edges in a flat array (`Edge[]`) causes `neighbors()` to scan all edges in the entire graph (O(E)). This is a textbook performance anti-pattern that severely degrades graph traversal speed at scale.
**Action:** When implementing graph or node-relationship structures, always use an adjacency list (e.g. `Map<string, Edge[]>`) to ensure localized, O(degree) lookups instead of scanning the full graph.
