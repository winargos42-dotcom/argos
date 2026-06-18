---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/marketing/publisher-linkedin.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\marketing\publisher-linkedin.md
source_ext: .md
source_sha256: d90df485a75d800dbedcf8e7c5caa181aaacc0036731f299d6e0cc4bbcc9ba14
text_sha256: 6ffc939897929441340ac7216f80fb2d4f16ae3e4c3ccab8cb638ae642963776
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:29
---

# publisher-linkedin.md

- Source: `claude-code-templates/cli-tool/components/commands/marketing/publisher-linkedin.md`
- Extract: `text`
- SHA256: `d90df485a75d800dbedcf8e7c5caa181aaacc0036731f299d6e0cc4bbcc9ba14`

## Content

---
allowed-tools: Read, Write, Bash, Glob, WebFetch
argument-hint: <input> [lang] [custom-file-path]
description: Generate LinkedIn posts from blog content with automatic media attachment via LinkedIn API
---

# LinkedIn Post Generator

Create professional LinkedIn posts from any content source with optional media attachment.

**Usage:** `$ARGUMENTS`

**Examples:**
```bash
/publisher:linkedin my-post                    # Auto-detect and attach blog diagrams
/publisher:linkedin my-post en                 # English with diagrams
/publisher:linkedin my-post en image.png       # Custom image attachment
/publisher:linkedin my-post ja report.pdf      # Japanese with custom PDF
```

**Process:**

1. **Parse Input Arguments**
   - Content input (slug, file path, or URL)
   - Optional language parameter (en/ja)
   - Optional custom file path for attachment

2. **Universal Input Detection**
   - **File path**: Read and parse (markdown, PDF, HTML, text, JSON)
   - **URL**: Use WebFetch to retrieve content
   - **Slug**: Search codebase for matching blog post

3. **Generate Professional LinkedIn Post**
   - Use thought leadership tone for English
   - Use professional business tone (敬語) for Japanese
   - Extract key insights from actual content
   - Include relevant hashtags (2-4 max)
   - Add link to full article

4. **Handle Media Attachment**
   - **Custom file**: Use specified image/PDF if provided
   - **Auto-detect**: Find blog diagrams if available
   - Supported formats: PNG, JPG, JPEG, PDF

5. **Post via LinkedIn API** (using Bash + curl)
   - Check for credentials in .env file
   - Handle OAuth flow if needed
   - **CRITICAL**: Escape LinkedIn Little Text Format reserved characters: `| { } @ [ ] ( ) < > # * _ ~`
   - Upload media file and get asset URN
   - Create draft post with commentary and media
   - Open LinkedIn in browser for review

**LinkedIn API Authentication:**
1. Create LinkedIn app at https://www.linkedin.com/developers/apps
2. Add credentials to .env:
   ```
   LINKEDIN_CLIENT_ID=your_client_id
   LINKEDIN_CLIENT_SECRET=your_secret
   LINKEDIN_ACCESS_TOKEN=your_token (auto-generated on first use)
   ```

**Without API setup**: Command still generates the post content for manual copy-paste.

**Note**: Works in ANY repo type (Python, Rust, Go, etc.) - uses only bash and curl, no Node.js required.

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
