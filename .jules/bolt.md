## 2024-09-12 - [Array Operation Allocation Optimization]
**Learning:** Using `[...map.values()]` and `Array.prototype.filter`, as well as spread syntax and chaining `Array.prototype.map` followed by `Array.prototype.join`, leads to significantly high memory allocations and garbage collection overhead in tight loops (e.g. resolving capabilities across a large catalog). Native `for` loops that push conditionally to pre-allocated or newly constructed arrays directly provide a considerable speedup (20-30% improvement) in this specific architecture's hot paths.
**Action:** Always favor native `for..of` or indexed `for` loops when processing maps/sets or combining strings over large data sources. Avoid chaining array manipulation methods in high-frequency path files (like `context.ts` or `registry.ts`).
## 2024-09-12 - [CI Fix]
**Learning:** The SonarQube Action version specified (`v1.3.0`) was invalid and caused the CI pipeline to fail because this version doesn't exist.
**Action:** When specifying GitHub Actions versions, verify the latest stable release (e.g. `v1.2.1` for `sonarqube-quality-gate-action`) via the GitHub API before hardcoding a version bump to avoid breaking the CI.
## 2024-09-12 - [GitHub Actions Conditionals]
**Learning:** In GitHub Actions, `env` variables set locally in a step or evaluated dynamically are not accessible to the `if` conditional on the same step (the `if` block is evaluated before the step execution context).
**Action:** When adding conditional execution logic depending on secrets, use `${{ secrets.MY_SECRET != '' }}` or ensure you export variables to `$GITHUB_ENV` in a *previous* step if you need to use `env` in conditionals.
