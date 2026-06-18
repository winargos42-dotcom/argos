---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/performance/add-performance-monitoring.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\performance\add-performance-monitoring.md
source_ext: .md
source_sha256: d9b5484d4a359ff9e050c8fb24017f9b72fbf0aaedafe021bab7fa107e1b917b
text_sha256: 7a37b1fb32476ead2334f43b59e3266175b3960614d0cb4f965f193adb8706ee
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# add-performance-monitoring.md

- Source: `claude-code-templates/cli-tool/components/commands/performance/add-performance-monitoring.md`
- Extract: `text`
- SHA256: `d9b5484d4a359ff9e050c8fb24017f9b72fbf0aaedafe021bab7fa107e1b917b`

## Content

---
allowed-tools: Read, Bash, Grep, Glob
argument-hint: [monitoring-type] | --apm | --rum | --custom
description: Setup comprehensive application performance monitoring with metrics, alerting, and observability
---

# Add Performance Monitoring

Setup application performance monitoring: **$ARGUMENTS**

## Instructions

1. **Performance Monitoring Strategy**
   - Define key performance indicators (KPIs) and service level objectives (SLOs)
   - Identify critical user journeys and performance bottlenecks
   - Plan monitoring architecture and data collection strategy
   - Assess existing monitoring infrastructure and integration points
   - Define alerting thresholds and escalation procedures

2. **Application Performance Monitoring (APM)**
   - Set up comprehensive APM solution (New Relic, Datadog, AppDynamics)
   - Configure distributed tracing for request lifecycle visibility
   - Implement custom metrics and performance tracking
   - Set up transaction monitoring and error tracking
   - Configure performance profiling and diagnostics

3. **Real User Monitoring (RUM)**
   - Implement client-side performance tracking and web vitals monitoring
   - Set up user experience metrics collection (LCP, FID, CLS, TTFB)
   - Configure custom performance metrics for user interactions
   - Monitor page load performance and resource loading
   - Track user journey performance across different devices

4. **Server Performance Monitoring**
   - Monitor system metrics (CPU, memory, disk, network)
   - Set up process and application-level monitoring
   - Configure event loop lag and garbage collection monitoring
   - Implement custom server performance metrics
   - Monitor resource utilization and capacity planning

5. **Database Performance Monitoring**
   - Track database query performance and slow query identification
   - Monitor database connection pool utilization
   - Set up database performance metrics and alerting
   - Implement query execution plan analysis
   - Monitor database resource usage and optimization opportunities

6. **Error Tracking and Monitoring**
   - Implement comprehensive error tracking (Sentry, Bugsnag, Rollbar)
   - Configure error categorization and impact analysis
   - Set up error alerting and notification systems
   - Track error trends and resolution metrics
   - Implement error context and debugging information

7. **Custom Metrics and Dashboards**
   - Implement business metrics tracking (Prometheus, StatsD)
   - Create performance dashboards and visualizations
   - Configure custom alerting rules and thresholds
   - Set up performance trend analysis and reporting
   - Implement performance regression detection

8. **Alerting and Notification System**
   - Configure intelligent alerting based on performance thresholds
   - Set up multi-channel notifications (email, Slack, PagerDuty)
   - Implement alert escalation and on-call procedures
   - Configure alert fatigue prevention and noise reduction
   - Set up performance incident management workflows

9. **Performance Testing Integration**
   - Integrate monitoring with load testing and performance testing
   - Set up continuous performance testing and monitoring
   - Configure performance baseline tracking and comparison
   - Implement performance test result analysis and reporting
   - Monitor performance under different load scenarios

10. **Performance Optimization Recommendations**
    - Generate actionable performance insights and recommendations
    - Implement automated performance analysis and reporting
    - Set up performance optimization tracking and measurement
    - Configure performance improvement validation
    - Create performance optimization prioritization frameworks

Focus on monitoring strategies that provide actionable insights for performance optimization. Ensure monitoring overhead is minimal and doesn't impact application performance.

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
