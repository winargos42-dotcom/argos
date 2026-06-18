---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/productivity/obsidian-clipper-template-creator/references/variables.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\productivity\obsidian-clipper-template-creator\references\variables.md
source_ext: .md
source_sha256: 7cd28afa1ee522b5f9fe463b021aff945e3b5ad0c25191cc44b463151c41e058
text_sha256: 05e5019fb1d727327710a8d1bae721561ac43010d1063d384af88e66bbab8f1a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# variables.md

- Source: `claude-code-templates/cli-tool/components/skills/productivity/obsidian-clipper-template-creator/references/variables.md`
- Extract: `text`
- SHA256: `7cd28afa1ee522b5f9fe463b021aff945e3b5ad0c25191cc44b463151c41e058`

## Content

# Obsidian Web Clipper Variables

**Official Docs:** [help.obsidian.md/web-clipper/variables](https://help.obsidian.md/web-clipper/variables)

## Preset Variables
Automatically extracted from the page.

- `{{content}}`: Main article content (markdown).
- `{{contentHtml}}`: Main article content (HTML).
- `{{title}}`: Page title.
- `{{url}}`: Page URL.
- `{{author}}`: Author name.
- `{{date}}`: Current date.
- `{{published}}`: Publication date (if detected).
- `{{site}}`: Site name.
- `{{description}}`: Meta description.
- `{{highlights}}`: Highlighted text (if any).
- `{{selection}}`: Selected text.
- `{{fullHtml}}`: Full page HTML.
- `{{favicon}}`: Favicon URL.
- `{{image}}`: Social share image URL.
- `{{words}}`: Word count.
- `{{domain}}`: Domain name.

## Prompt Variables (AI)
Use `{{"Your prompt here"}}` to ask the AI Interpreter to extract or summarize info.
*Requires Interpreter to be enabled.*

Examples:
- `{{"Summarize in 3 bullet points"}}`
- `{{"Extract the ingredients list"}}`
- `{{"Translate to English"}}`

## Selector Variables
Extract content using CSS selectors.
Syntax: `{{selector:css-selector}}` or `{{selector:css-selector?attribute}}`

Examples:
- `{{selector:h1}}`: Text of H1 tag.
- `{{selector:img.hero?src}}`: Source of image with class 'hero'.
- `{{selector:.author}}`: Text of element with class 'author'.
- `{{selectorHtml:body|markdown}}`: Full HTML converted to markdown.

## Meta Variables
Extract data from meta tags.
Syntax: `{{meta:name}}` or `{{meta:property}}`

Examples:
- `{{meta:description}}`
- `{{meta:og:title}}`

## Schema.org Variables
Extract structured data.
Syntax: `{{schema:Property}}` or `{{schema:@Type:Property}}`

Examples:
- `{{schema:Recipe:recipeIngredient}}`
- `{{schema:author.name}}`
- `{{schema:Article:headline}}`

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
