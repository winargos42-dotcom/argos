---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/performance/optimize-memory-usage.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\performance\optimize-memory-usage.md
source_ext: .md
source_sha256: c2beaa3da3e703263beefeba3f08acf0a990365d04799ced249c5ce2aeef4042
text_sha256: f0c59948fe060633bedaa0dba89df3242d9558d4c8166ed577512c0a3ee30ae2
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# optimize-memory-usage.md

- Source: `claude-code-templates/cli-tool/components/commands/performance/optimize-memory-usage.md`
- Extract: `text`
- SHA256: `c2beaa3da3e703263beefeba3f08acf0a990365d04799ced249c5ce2aeef4042`

## Content

---
allowed-tools: Read, Bash, Grep, Glob
argument-hint: [target-area] | --frontend | --backend | --database
description: Comprehensive memory usage optimization with leak detection, garbage collection tuning, and memory profiling
---

# Optimize Memory Usage

Analyze and optimize memory usage patterns to prevent leaks and improve application performance: **$ARGUMENTS**

## Instructions

1. **Memory Analysis and Profiling**
   - Profile current memory usage patterns using appropriate tools (Chrome DevTools, Node.js --inspect, Valgrind)
   - Identify memory leaks and excessive memory consumption hotspots
   - Analyze garbage collection patterns and performance impact
   - Create baseline measurements for optimization tracking
   - Document memory allocation hotspots and growth patterns over time

2. **Memory Leak Detection**
   - Set up memory leak detection for different runtime environments
   - Monitor heap snapshots and compare over time intervals
   - Track DOM node leaks in browser applications
   - Implement event listener cleanup and monitoring
   - Use profiling tools to identify growing memory patterns

3. **Garbage Collection Optimization**
   - Configure garbage collection settings for your runtime environment
   - Tune Node.js heap sizes and GC flags for optimal performance
   - Monitor GC pause times and frequency
   - Implement GC performance monitoring and alerting
   - Optimize object lifecycles to reduce GC pressure

4. **Memory Pool and Object Reuse**
   - Implement object pooling for frequently allocated objects
   - Create buffer pools for Node.js applications
   - Reuse DOM elements and components in frontend applications
   - Design memory-efficient data structures (circular buffers, sparse arrays)
   - Pre-allocate objects to reduce runtime allocation overhead

5. **String and Text Optimization**
   - Implement string interning for frequently used strings
   - Optimize string concatenation and manipulation operations
   - Use efficient text processing algorithms
   - Minimize string duplication across the application
   - Consider string compression for large text data

6. **Database Connection Optimization**
   - Implement proper connection pooling with appropriate limits
   - Configure connection timeouts and cleanup procedures
   - Optimize query result caching and memory usage
   - Monitor database connection memory overhead
   - Implement connection leak detection and prevention

7. **Frontend Memory Optimization**
   - Optimize component lifecycle and cleanup
   - Implement proper event listener cleanup
   - Use lazy loading for images and components
   - Minimize bundle size and code splitting
   - Monitor and optimize browser memory usage patterns

8. **Backend Memory Optimization**
   - Optimize server request handling and cleanup
   - Implement streaming for large data processing
   - Configure appropriate memory limits and monitoring
   - Optimize middleware and request lifecycle
   - Use memory-efficient data processing patterns

9. **Container and Deployment Optimization**
   - Configure appropriate container memory limits
   - Optimize Docker image layers for memory efficiency
   - Monitor memory usage in production environments
   - Implement memory-based auto-scaling policies
   - Set up memory usage alerting and monitoring

10. **Memory Monitoring and Alerting**
    - Set up real-time memory monitoring dashboards
    - Configure memory usage alerts and thresholds
    - Implement memory leak detection in production
    - Track memory performance metrics over time
    - Create automated memory optimization testing

11. **Production Memory Management**
    - Implement graceful memory pressure handling
    - Configure memory-based health checks
    - Set up memory usage trending and analysis
    - Implement emergency memory cleanup procedures
    - Monitor and optimize memory usage patterns

Focus on the specific memory optimization strategies that provide the biggest impact for your target environment. Always measure memory usage before and after optimizations to quantify improvements.

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
