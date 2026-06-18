---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/marketing/publisher-devto.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\marketing\publisher-devto.md
source_ext: .md
source_sha256: a710950dd299c1ea05f4c21485fcc57bb688026e4a4c704fe13dd622876fef4c
text_sha256: 954bee63945cce469e68d001dc5945fe2b2375ca251124cff9ac0ffd15a1ee79
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# publisher-devto.md

- Source: `claude-code-templates/cli-tool/components/commands/marketing/publisher-devto.md`
- Extract: `text`
- SHA256: `a710950dd299c1ea05f4c21485fcc57bb688026e4a4c704fe13dd622876fef4c`

## Content

---
allowed-tools: Read, Write, Bash, Glob
argument-hint:
description: Generate Dev.to RSS feed from all blog posts for automatic syndication
---

# Dev.to RSS Feed Generator

Generate a complete RSS feed from all your blog posts for automatic import to Dev.to.

**Usage:** `/publisher:devto` (no arguments needed)

**What it does:**
- Scans all blog posts in your codebase
- Converts markdown to HTML
- Generates RSS 2.0 feed with proper encoding
- Creates `public/rss-devto.xml` file
- Provides setup instructions for Dev.to

**Process:**

1. **Scan for Blog Posts**
   - Search codebase for markdown files
   - Common patterns:
     - `src/content/blog/**/*.md`
     - `content/blog/**/*.md`
     - `posts/**/*.md`
     - `blog/**/*.md`

2. **Parse Blog Posts**
   - Extract frontmatter (title, date, description, tags)
   - Convert markdown body to HTML
   - Encode HTML properly for RSS (CDATA sections)
   - Extract publication dates

3. **Generate RSS Feed**
   - Create valid RSS 2.0 XML structure
   - Include all blog posts as items
   - Add proper channel metadata
   - HTML-encode content for Dev.to compatibility

4. **Save Feed File**
   - Write to `public/rss-devto.xml`
   - Ensure proper XML formatting
   - Validate RSS structure

5. **Display Setup Instructions**
   - Show how to add RSS to Dev.to
   - Explain deployment requirements
   - Guide user through configuration

**One-time Setup:**
1. Run this command to generate RSS feed
2. Deploy your site (make RSS publicly accessible)
3. Go to https://dev.to/settings/extensions
4. Add your RSS URL (e.g., `https://yoursite.com/rss-devto.xml`)
5. Dev.to will auto-import all future posts

**Benefits:**
- Automatic syndication to Dev.to
- All future posts sync automatically
- No manual copying required
- Maintains original formatting

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
