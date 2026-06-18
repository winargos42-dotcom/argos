---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/performance/optimize-database-performance.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\performance\optimize-database-performance.md
source_ext: .md
source_sha256: b963d8af9875add4983991e76c50a2990d33afbbdc89bc1976d8bf1834a79664
text_sha256: c8f192ae68c88fc1d317d8ca32dc039bf276654c820f8dccff85fe66eab92f9f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# optimize-database-performance.md

- Source: `claude-code-templates/cli-tool/components/commands/performance/optimize-database-performance.md`
- Extract: `text`
- SHA256: `b963d8af9875add4983991e76c50a2990d33afbbdc89bc1976d8bf1834a79664`

## Content

---
allowed-tools: Read, Bash, Grep, Glob
argument-hint: [database-type] | --postgresql | --mysql | --mongodb
description: Optimize database queries, indexing, and performance for improved response times and scalability
---

# Optimize Database Performance

Optimize database queries and performance: **$ARGUMENTS**

## Instructions

1. **Database Performance Analysis**
   - Analyze current database performance and identify bottlenecks
   - Review slow query logs and execution plans
   - Assess database schema design and normalization
   - Evaluate indexing strategy and query patterns
   - Monitor database resource utilization (CPU, memory, I/O)

2. **Query Optimization**
   - Identify and optimize slow-performing queries
   - Analyze query execution plans and optimization strategies
   - Rewrite queries for better performance and efficiency
   - Implement query hints and optimization directives
   - Configure query timeout and resource limits

3. **Index Strategy Optimization**
   - Analyze existing indexes and their usage patterns
   - Design optimal indexing strategy for query patterns
   - Create composite indexes for multi-column queries
   - Implement covering indexes to avoid table lookups
   - Remove unused and redundant indexes

4. **Schema Design Optimization**
   - Optimize table structure and data types
   - Implement denormalization strategies for read-heavy workloads
   - Design partitioning strategies for large tables
   - Create materialized views for complex aggregations
   - Optimize foreign key relationships and constraints

5. **Connection Pool Optimization**
   - Configure optimal database connection pooling settings
   - Tune connection pool size and timeout settings
   - Implement connection monitoring and health checks
   - Optimize connection lifecycle and cleanup procedures
   - Configure connection security and SSL settings

6. **Query Result Caching**
   - Implement intelligent database result caching
   - Design cache invalidation strategies for data consistency
   - Set up query-level and result-set caching
   - Configure cache expiration and refresh policies
   - Monitor cache effectiveness and hit rates

7. **Database Monitoring and Profiling**
   - Set up comprehensive database performance monitoring
   - Monitor query performance and resource usage
   - Track database connections and session activity
   - Implement alerting for performance degradation
   - Configure automated performance reporting

8. **Read Replica and Load Balancing**
   - Configure read replicas for query distribution
   - Implement intelligent read/write query routing
   - Set up load balancing across database instances
   - Monitor replication lag and consistency
   - Configure failover and disaster recovery procedures

9. **Database Vacuum and Maintenance**
   - Implement automated database maintenance procedures
   - Configure vacuum and analyze operations for optimal performance
   - Set up index rebuilding and maintenance schedules
   - Monitor table bloat and fragmentation
   - Implement automated cleanup and archival strategies

10. **Performance Testing and Benchmarking**
    - Set up database performance testing frameworks
    - Implement load testing scenarios for realistic workloads
    - Benchmark query performance under different conditions
    - Test database scalability and capacity limits
    - Monitor performance regression and improvements

Focus on database optimizations that provide the most significant performance improvements for your specific workload patterns. Always measure performance before and after changes to validate optimizations.

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
