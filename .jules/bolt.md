## 2024-05-19 - [KnowledgeGraph Adjacency Map]
**Learning:** Using an array to store edges in a graph results in O(E) complexity for neighbor lookups, which becomes a major bottleneck as the graph scales (E = total edges). For 50,000 edges and 100 queries, it took 84.6ms.
**Action:** Always prefer adjacency lists/maps (`Map<string, Edge[]>`) over flat arrays (`Edge[]`) for edge storage in graph implementations to achieve O(1) neighbor lookups, drastically reducing query time (down to 0.36ms for the same 100 queries).
