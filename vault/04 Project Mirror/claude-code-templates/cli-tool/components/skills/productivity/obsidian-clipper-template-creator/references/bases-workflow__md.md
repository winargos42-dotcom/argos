---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/productivity/obsidian-clipper-template-creator/references/bases-workflow.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\productivity\obsidian-clipper-template-creator\references\bases-workflow.md
source_ext: .md
source_sha256: 9450f9815f734798201ab884b9ec895d1df5f02a875d754e79527dc2f27d06e7
text_sha256: 94dfc761d332f2486dc0c205a6a74e2d11a7d9b861b573d42a78650b58e56889
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# bases-workflow.md

- Source: `claude-code-templates/cli-tool/components/skills/productivity/obsidian-clipper-template-creator/references/bases-workflow.md`
- Extract: `text`
- SHA256: `9450f9815f734798201ab884b9ec895d1df5f02a875d754e79527dc2f27d06e7`

## Content

# Working with Obsidian Bases

The user maintains "Bases" in `Templates/Bases/*.base` which define the schema and properties for different types of notes (e.g., Recipes, Clippings, People).

## Workflow

1.  **Identify the Category:** Determine the type of content the user wants to clip (e.g., a Recipe, a News Article, a YouTube video).
2.  **Find the Base:** Search `Templates/Bases/` for a matching `.base` file.
    *   Example: For a recipe, look for `Templates/Bases/Recipes.base`.
    *   Example: For a generic article, look for `Templates/Bases/Clippings.base`.
3.  **Read the Base:** Read the content of the `.base` file to understand the required properties.

## Interpreting .base Files

Base files use a YAML-like structure. Look for the `properties` section.

```yaml
properties:
  file.name:
    displayName: name
  note.author:
    displayName: author
  note.type:
    displayName: type
  note.ingredients:
    displayName: ingredients
```

*   `note.X` corresponds to a property name `X` in the frontmatter.
*   `displayName` helps understand the intent, but the property key (e.g., `author`, `type`, `ingredients`) is what matters for the template.

## Mapping to Clipper Properties

When creating the JSON for the Web Clipper, map the Base properties to the `properties` array in the JSON.

| Base Property | Clipper JSON Property Name | Value Strategy |
| :--- | :--- | :--- |
| `note.author` | `author` | `{{author}}` or `{{schema:author.name}}` |
| `note.source` | `source` | `{{url}}` |
| `note.published` | `published` | `{{published}}` |
| `note.ingredients` | `ingredients` | `{{schema:Recipe:recipeIngredient}}` |
| `note.type` | `type` | Constant (e.g., `Recipe`) or empty |

**Crucial Step:** Ask the user which properties should be automatically filled, which should be hardcoded (e.g., `type: Recipe`), and which should be left empty for manual entry.

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
