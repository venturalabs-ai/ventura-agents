## 2024-05-24 - Array spreading performance anti-pattern
**Learning:** Found multiple instances where `[...map.values()].filter(...)` and similar structures were used. This pattern is problematic because it unnecessarily forces intermediate array memory allocation and iteration of iterables like maps/sets solely to perform array operations like map and filter.
**Action:** Use standard `for...of` loops to directly iterate map elements and construct target arrays. Ensure to add required explanatory comments for any performance optimization code adjustments.
