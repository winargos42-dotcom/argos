---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/web-development/react-best-practices/references/rules/async-dependencies.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\web-development\react-best-practices\references\rules\async-dependencies.md
source_ext: .md
source_sha256: dc7a0e91c915996cc6c43ddd2a67555c1d5f215ebf88ccae0d65f0b68130e3a0
text_sha256: bfd348ab519f168447ffdbde7b70f40ecb99115c3cdae9292182ec8e28e1ab63
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# async-dependencies.md

- Source: `claude-code-templates/cli-tool/components/skills/web-development/react-best-practices/references/rules/async-dependencies.md`
- Extract: `text`
- SHA256: `dc7a0e91c915996cc6c43ddd2a67555c1d5f215ebf88ccae0d65f0b68130e3a0`

## Content

---
title: Dependency-Based Parallelization
impact: CRITICAL
impactDescription: 2-10× improvement
tags: async, parallelization, dependencies, better-all
---

## Dependency-Based Parallelization

For operations with partial dependencies, use `better-all` to maximize parallelism. It automatically starts each task at the earliest possible moment.

**Incorrect (profile waits for config unnecessarily):**

```typescript
const [user, config] = await Promise.all([
  fetchUser(),
  fetchConfig()
])
const profile = await fetchProfile(user.id)
```

**Correct (config and profile run in parallel):**

```typescript
import { all } from 'better-all'

const { user, config, profile } = await all({
  async user() { return fetchUser() },
  async config() { return fetchConfig() },
  async profile() {
    return fetchProfile((await this.$.user).id)
  }
})
```

Reference: [https://github.com/shuding/better-all](https://github.com/shuding/better-all)

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
