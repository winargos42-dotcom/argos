---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/setup/setup-rate-limiting.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\setup\setup-rate-limiting.md
source_ext: .md
source_sha256: 506dc367909044bf2601a19b8806f081fc5ca542bd1a48686bd6023190206982
text_sha256: 6d1272c9b1a2192e7ad8703aeb9bdf13b5248cc9525b44fe1059ec280f1cc513
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# setup-rate-limiting.md

- Source: `claude-code-templates/cli-tool/components/commands/setup/setup-rate-limiting.md`
- Extract: `text`
- SHA256: `506dc367909044bf2601a19b8806f081fc5ca542bd1a48686bd6023190206982`

## Content

---
allowed-tools: Read, Write, Edit, Bash
argument-hint: [rate-limit-type] | --api | --authentication | --file-upload | --database
description: Implement comprehensive API rate limiting with advanced algorithms and user-specific policies
---

# Setup Rate Limiting

Implement comprehensive API rate limiting with advanced control mechanisms: **$ARGUMENTS**

## Current API State

- Framework detection: @package.json or @requirements.txt (Express, FastAPI, Spring Boot, etc.)
- Existing rate limiting: !`grep -r "rate.limit\|throttle\|rateLimit" src/ 2>/dev/null | wc -l`
- Redis availability: !`redis-cli ping 2>/dev/null || echo "Redis not available"`
- API endpoints: !`grep -r "route\|endpoint\|@app\\.route" src/ 2>/dev/null | wc -l`

## Task

Implement production-ready rate limiting system with sophisticated algorithms and user policies:

**Rate Limit Type**: Use $ARGUMENTS to focus on API rate limiting, authentication limiting, file upload controls, or database access limiting

**Rate Limiting Architecture**:
1. **Algorithm Implementation** - Token bucket, sliding window, fixed window, leaky bucket algorithms
2. **User Policies** - Tier-based limits, authenticated vs anonymous, user-specific quotas, IP-based controls
3. **Storage Backend** - Redis integration, distributed rate limiting, persistence strategies, failover mechanisms
4. **Endpoint Configuration** - Per-route limits, method-specific rules, dynamic configuration, A/B testing
5. **Monitoring & Analytics** - Usage tracking, abuse detection, performance metrics, alerting systems
6. **Bypass Mechanisms** - Whitelist management, internal request handling, emergency overrides

**Advanced Features**: Adaptive rate limiting, geo-based controls, API key management, quota systems, abuse prevention.

**Production Readiness**: High availability, performance optimization, security controls, comprehensive monitoring.

**Output**: Complete rate limiting system with intelligent policies, comprehensive monitoring, and advanced abuse prevention capabilities.

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
