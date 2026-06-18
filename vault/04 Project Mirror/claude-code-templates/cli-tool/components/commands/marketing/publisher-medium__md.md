---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/marketing/publisher-medium.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\marketing\publisher-medium.md
source_ext: .md
source_sha256: f4d6d857cb8e4706329599e8f17e93dc2fadca0a334140bbcda95223a523b38a
text_sha256: f350e8218599d152d3ce9ee099f583cd4683500b0d559dcd8ecbcdfc75a1004b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# publisher-medium.md

- Source: `claude-code-templates/cli-tool/components/commands/marketing/publisher-medium.md`
- Extract: `text`
- SHA256: `f4d6d857cb8e4706329599e8f17e93dc2fadca0a334140bbcda95223a523b38a`

## Content

---
allowed-tools: Read, Write, Bash, Glob, WebFetch
argument-hint: <input> [lang]
description: Convert blog posts to Medium-ready HTML format with image upload markers
---

# Medium Article Converter

Convert blog posts to Medium-ready format with proper HTML structure and image handling.

**Usage:** `$ARGUMENTS`

**Examples:**
```bash
/publisher:medium my-post           # Default English
/publisher:medium my-post ja        # Japanese
/publisher:medium article.md        # From file path
/publisher:medium https://blog.com/post  # From URL
```

**Process:**

1. **Parse Input & Detect Source**
   - File path, URL, or blog post slug
   - Optional language parameter (en/ja)

2. **Universal Input Detection**
   - **File**: Read markdown, PDF, HTML, or text
   - **URL**: WebFetch to retrieve content
   - **Slug**: Search codebase for blog post

3. **Convert to Medium Format**
   - Parse markdown and extract frontmatter
   - Convert to clean HTML suitable for Medium
   - Preserve headers, lists, code blocks, quotes
   - Add image upload markers for diagrams
   - Include image paths for easy upload reference

4. **Create HTML Preview File**
   - Generate `medium-article-[LANG].html` preview
   - Include one-click copy button
   - Add image upload instructions with file paths
   - Use Medium-style formatting and colors

5. **Open in Browser**
   - Open HTML preview file
   - Open Medium editor (https://medium.com/new-story)
   - User can copy HTML and paste into Medium
   - Follow image markers to upload diagrams

**Output:**
- HTML preview file with copy button
- Clear image upload markers
- File paths shown for each image
- Ready to paste into Medium editor

**Note**: Works universally - no dependencies required, just Read, Write, and Bash tools.

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
