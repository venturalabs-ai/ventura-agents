## 2024-06-25 - [Knowledge Graph O(n) to O(1) adjacency lookup]
**Learning:** The knowledge graph representation in `src/platform/knowledge.ts` was storing edges in a flat array and filtering all edges to find neighbors (O(n) per query). For large graphs, this becomes a severe performance bottleneck.
**Action:** When implementing graph data structures, always use adjacency lists (or hash map lookups) rather than flat arrays for neighborhood queries to ensure O(1) or O(d) lookup time, where d is the degree of the node.
