---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/productivity/obsidian-clipper-template-creator/references/analysis-workflow.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\productivity\obsidian-clipper-template-creator\references\analysis-workflow.md
source_ext: .md
source_sha256: efe446b89c92f37dabe6231796933ef92821e1c681e8a4b1b7d327ef69381499
text_sha256: d666273f5db50f27ffa3866ee2bd5f4948bdbbb28ce9635169249bb00da2142f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:48
---

# analysis-workflow.md

- Source: `claude-code-templates/cli-tool/components/skills/productivity/obsidian-clipper-template-creator/references/analysis-workflow.md`
- Extract: `text`
- SHA256: `efe446b89c92f37dabe6231796933ef92821e1c681e8a4b1b7d327ef69381499`

## Content

# Analysis Workflow: Validating Variables

To ensure your template works correctly, you must validate that the target page actually contains the data you want to extract.

## 1. Fetch the Page
Use the `WebFetch` tool to retrieve the content of a representative URL provided by the user.

```
WebFetch(url="https://example.com/recipe/chocolate-cake")
```

## 2. Analyze the Output

### Check for Schema.org (Recommended)
Look for `<script type="application/ld+json">`. This contains structured data which is the most reliable way to extract info.

**Example Found in HTML:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "Recipe",
  "name": "Chocolate Cake",
  "author": {
    "@type": "Person",
    "name": "John Doe"
  }
}
```

**Conclusion:**
*   `{{schema:Recipe:name}}` is valid.
*   `{{schema:Recipe:author.name}}` is valid.
*   **Tip:** You can use `schema:Recipe` in the `triggers` array to automatically select this template for any page with this schema.

### Check for Meta Tags
Look for `<meta>` tags in the `<head>` section.

**Example Found in HTML:**
```html
<meta property="og:title" content="The Best Chocolate Cake" />
<meta name="description" content="A rich, moist chocolate cake recipe." />
```

**Conclusion:**
*   `{{meta:og:title}}` is valid.
*   `{{meta:description}}` is valid.

### Check for CSS Selectors (Fallback)
If Schema and Meta tags are missing, look for HTML structure (classes and IDs) to use with `{{selector:...}}`.

**Example Found in HTML:**
```html
<div class="article-body">
  <h1 id="main-title">Chocolate Cake</h1>
  <span class="author-name">By John Doe</span>
</div>
```

**Conclusion:**
*   `{{selector:h1#main-title}}` or `{{selector:h1}}` can extract the title.
*   `{{selector:.author-name}}` can extract the author.

## 3. Verify Against Base
Compare the available data from your analysis with the properties required by the user's Base (see `references/bases-workflow.md`).

*   If the Base requires `ingredients` but the page has no Schema or clear list structure, warn the user that this field might need manual entry or a prompt variable.

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
