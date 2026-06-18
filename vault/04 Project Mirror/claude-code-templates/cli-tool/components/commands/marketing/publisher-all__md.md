---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/marketing/publisher-all.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\marketing\publisher-all.md
source_ext: .md
source_sha256: 991d37ae46dadac067d6d1fa976cb3820c1e723fbf3c26f9237b00a16eba2f60
text_sha256: bcd86126ed1964234756d5fbbba9b15840a006057a22a72369594ee494880924
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# publisher-all.md

- Source: `claude-code-templates/cli-tool/components/commands/marketing/publisher-all.md`
- Extract: `text`
- SHA256: `991d37ae46dadac067d6d1fa976cb3820c1e723fbf3c26f9237b00a16eba2f60`

## Content

---
allowed-tools: Read, Write, Bash, Glob, WebFetch
argument-hint: <input> [lang]
description: Generate content for ALL platforms at once (X, LinkedIn, Medium, Dev.to)
---

# All-Platform Content Generator

Generate content for X/Twitter, LinkedIn, Medium, and Dev.to in a single command.

**Usage:** `$ARGUMENTS`

**Examples:**
```bash
/publisher:all my-post              # All platforms, English
/publisher:all my-post ja           # All platforms, Japanese
/publisher:all article.md           # From file path
```

**What it does:**
Runs all publisher commands sequentially:
1. `/publisher:x` - X/Twitter thread (3 versions: thread, long, short)
2. `/publisher:linkedin` - LinkedIn post with media attachment
3. `/publisher:medium` - Medium-ready HTML article
4. `/publisher:devto` - Dev.to RSS feed (if not already generated)

**Process:**

For each platform:
1. Parse the same input (slug, file, or URL)
2. Generate platform-specific content
3. Create HTML previews
4. Open all previews in browser tabs

**Output:**
- `x-thread-[LANG].html` - X thread with 3 format tabs
- LinkedIn draft post (via API) or HTML preview
- `medium-article-[LANG].html` - Medium-ready content
- `rss-devto.xml` - Complete RSS feed

**Time Savings:**
Instead of running 4 separate commands and spending ~2 hours manually adapting content, this generates everything in one go.

**Next Steps:**
1. Browser tabs open automatically
2. Review each platform's content
3. Copy-paste or publish via API
4. Adjust as needed for your audience

**Note**: Each platform's content is uniquely optimized - not just copy-paste across channels.

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
