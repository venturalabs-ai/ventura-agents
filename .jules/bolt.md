## 2026-09-02 - Optimize Graph Lookup Time
**Learning:** Graph data structures using a flat array of edges and performing O(E) scans with array methods (.filter.map.filter) for neighbor lookups can be a hidden performance bottleneck, especially as the number of edges grows.
**Action:** Always prefer adjacency lists (e.g., `Map<string, Edge[]>`) for graphs to reduce neighbor lookup time from O(E) to O(degree). Also, avoid unnecessary chained array loops in favor of a single manual loop.
