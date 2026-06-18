---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/productivity/obsidian-clipper-template-creator/references/filters.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\productivity\obsidian-clipper-template-creator\references\filters.md
source_ext: .md
source_sha256: 791bdbad9196dc9bbe6d31f317a1f95a60e7b4b6c2c2f411707ccde8239fd50a
text_sha256: 6243c4b9097a552a4b5fbc256092e088570fed2d77cc3f7a077c4575bc266000
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# filters.md

- Source: `claude-code-templates/cli-tool/components/skills/productivity/obsidian-clipper-template-creator/references/filters.md`
- Extract: `text`
- SHA256: `791bdbad9196dc9bbe6d31f317a1f95a60e7b4b6c2c2f411707ccde8239fd50a`

## Content

# Obsidian Web Clipper Filters

**Official Docs:** [help.obsidian.md/web-clipper/filters](https://help.obsidian.md/web-clipper/filters)

Use filters to format variables: `{{variable|filter}}`.

## Text Formatting
- `markdown`: Convert HTML to Markdown.
- `strip_tags`: Remove HTML tags.
- `trim`: Remove whitespace.
- `upper`: Convert to uppercase.
- `lower`: Convert to lowercase.
- `title`: Title Case.
- `capitalize`: Capitalize first letter.
- `camel`: CamelCase.
- `kebab`: kebab-case.
- `snake`: snake_case.
- `pascal`: PascalCase.
- `replace:"old","new"`: Replace text.
- `safe_name`: Make safe for filenames.
- `blockquote`: Format as blockquote.
- `link`: Create markdown link.
- `wikilink`: Create \[\[wikilink\]\].
- `list`: Format array as list.
- `table`: Format array as table.
- `callout`: Format as callout block.

## Dates
- `date:"format"`: Format date (e.g., `YYYY-MM-DD`).
- `date_modify:"+1 day"`: Modify date.
- `duration`: Format duration.

## Numbers
- `calc`: Perform calculations.
- `length`: Get length of string/array.
- `round`: Round numbers.

## HTML Processing
- `remove_html`: Remove HTML tags.
- `remove_attr`: Remove attributes.
- `strip_attr`: Strip specific attributes.

## Arrays and Objects
- `map`: Transform array items (e.g., `map:item =>> item.text`).
- `join:"separator"`: Join array items.
- `split:"separator"`: Split string into array.
- `first`: First item.
- `last`: Last item.
- `slice:start,end`: Slice array.
- `unique`: Unique items.
- `template:"format"`: Format items using a template string.

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
