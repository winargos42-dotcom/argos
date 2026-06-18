---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/performance/implement-caching-strategy.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\performance\implement-caching-strategy.md
source_ext: .md
source_sha256: ab67c4e453fdaf7957f4fe947644a368b088a9c5c0fc7cf86f507e9a03b59da7
text_sha256: 8c88549dd740714c0df2d142292290b086578e46e61acbf04292d06892f0007c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# implement-caching-strategy.md

- Source: `claude-code-templates/cli-tool/components/commands/performance/implement-caching-strategy.md`
- Extract: `text`
- SHA256: `ab67c4e453fdaf7957f4fe947644a368b088a9c5c0fc7cf86f507e9a03b59da7`

## Content

---
allowed-tools: Read, Bash, Grep, Glob
argument-hint: [cache-type] | --browser | --application | --database
description: Design and implement comprehensive caching solutions for improved performance and scalability
---

# Implement Caching Strategy

Design and implement caching solutions: **$ARGUMENTS**

## Instructions

1. **Caching Strategy Analysis**
   - Analyze application architecture and identify caching opportunities
   - Assess current performance bottlenecks and data access patterns
   - Define caching requirements (TTL, invalidation, consistency)
   - Plan multi-layer caching architecture (browser, CDN, application, database)
   - Evaluate caching technologies and storage solutions

2. **Browser and Client-Side Caching**
   - Configure HTTP caching headers and cache policies for static assets
   - Implement service worker caching strategies for progressive web apps
   - Set up browser storage caching (localStorage, sessionStorage, IndexedDB)
   - Configure CDN caching rules and edge optimization
   - Implement cache-first, network-first, and stale-while-revalidate strategies

3. **Application-Level Caching**
   - Implement in-memory caching for frequently accessed data
   - Set up distributed caching with Redis or Memcached
   - Design cache key naming conventions and namespacing
   - Implement cache warming strategies for critical data
   - Configure cache expiration and TTL policies

4. **Database Query Caching**
   - Implement query result caching for expensive database operations
   - Set up prepared statement caching and connection pooling
   - Design cache invalidation strategies for data consistency
   - Implement materialized views for complex aggregations
   - Configure database-level caching features and optimizations

5. **API Response Caching**
   - Implement API endpoint response caching with appropriate headers
   - Set up middleware for automatic response caching
   - Configure GraphQL query caching and field-level optimization
   - Implement conditional requests with ETag and Last-Modified headers
   - Design cache invalidation for API data updates

6. **Cache Invalidation Strategies**
   - Design intelligent cache invalidation based on data dependencies
   - Implement event-driven cache invalidation systems
   - Set up cache tagging and bulk invalidation mechanisms
   - Configure time-based and trigger-based invalidation policies
   - Implement cache versioning and rollback strategies

7. **Frontend Caching Strategies**
   - Implement client-side data caching with libraries like React Query
   - Set up component-level caching and memoization
   - Configure asset bundling and chunk caching strategies
   - Implement progressive image loading and caching
   - Set up offline-first caching for PWAs

8. **Cache Monitoring and Analytics**
   - Set up cache performance monitoring and metrics collection
   - Track cache hit rates, miss rates, and efficiency metrics
   - Monitor cache memory usage and storage optimization
   - Implement cache performance alerting and notifications
   - Analyze cache usage patterns and optimization opportunities

9. **Cache Warming and Preloading**
   - Implement automated cache warming for critical data
   - Set up scheduled cache refresh and preloading strategies
   - Design on-demand cache generation for popular content
   - Configure cache warming triggers based on usage patterns
   - Implement predictive caching based on user behavior

10. **Testing and Validation**
    - Set up cache performance testing and benchmarking
    - Implement cache consistency validation and testing
    - Configure cache invalidation testing scenarios
    - Test cache behavior under high load and failure conditions
    - Validate cache security and data isolation requirements

Focus on implementing caching strategies that provide the most significant performance improvements while maintaining data consistency and system reliability. Always measure cache effectiveness and adjust strategies based on real-world usage patterns.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
