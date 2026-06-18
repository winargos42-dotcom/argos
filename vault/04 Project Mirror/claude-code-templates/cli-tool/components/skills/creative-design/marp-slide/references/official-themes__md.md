---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/creative-design/marp-slide/references/official-themes.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\creative-design\marp-slide\references\official-themes.md
source_ext: .md
source_sha256: 2a235a0ef7ebf3adda964318f08bd6ccf242e8a5bd33b4bd6fd002653546215a
text_sha256: ada377579fa97c87c5b4dfa40ee728a598d4bd6b13460ca572003be3afc5a9ab
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:35
---

# official-themes.md

- Source: `claude-code-templates/cli-tool/components/skills/creative-design/marp-slide/references/official-themes.md`
- Extract: `text`
- SHA256: `2a235a0ef7ebf3adda964318f08bd6ccf242e8a5bd33b4bd6fd002653546215a`

## Content

# Marp Official Themes Reference

Explanation of the 3 official themes included in Marp Core.

Official implementation: https://github.com/marp-team/marp-core/tree/main/themes

## Official Theme List

1. **default** - Simple and versatile theme
2. **gaia** - Modern and colorful theme
3. **uncover** - Minimal and elegant theme

## Default Theme

### Features

- **Colors**: White background, black text, blue accent
- **Font**: Simple sans-serif
- **Use for**: General presentations
- **Style**: Clean, readable

### Usage

```markdown
---
marp: true
theme: default
---

# Title

Content
```

### Available Classes

#### lead (Title Slide)

```markdown
<!-- _class: lead -->

# Presentation

Subtitle or description
```

Centered, large text.

#### invert (Inverted Colors)

```markdown
<!-- _class: invert -->

# Black Background · White Text
```

Background becomes black, text becomes white.

#### Combined

```markdown
<!-- _class: lead invert -->

# Inverted Title Slide
```

Multiple classes can be applied simultaneously.

### Customization Example

```markdown
---
theme: default
---

<style>
section {
  background-color: #f5f5f5;
}

h1 {
  color: #1e40af;
}
</style>
```

## Gaia Theme

### Features

- **Colors**: Colorful, vibrant accent colors
- **Font**: Modern sans-serif
- **Use for**: Creative presentations, design showcases
- **Style**: Energetic, visually appealing

### Usage

```markdown
---
marp: true
theme: gaia
---

# Title
```

### Color Variations

The Gaia theme has multiple color schemes:

```markdown
<!-- _class: lead -->
# Default Colors

---

<!-- _class: lead invert -->
# Inverted Colors

---

<!-- _class: lead gaia -->
# Gaia Colors
```

### Distinctive Styles

- **Gradient backgrounds**: Used in title slides
- **Colorful accents**: Headings and links
- **Large typography**: Impactful headings

### Customization Example

```markdown
---
theme: gaia
---

<style>
section {
  --color-background: #fff;
  --color-foreground: #333;
  --color-highlight: #e91e63;
}
</style>
```

## Uncover Theme

### Features

- **Colors**: Minimal, white or black base
- **Font**: Elegant serif font
- **Use for**: Formal presentations, academic talks
- **Style**: Refined, simple, elegant

### Usage

```markdown
---
marp: true
theme: uncover
---

# Title
```

### Available Classes

#### lead (Title Slide)

```markdown
<!-- _class: lead -->

# Presentation
```

Centered, large serif font.

#### invert (Inverted Colors)

```markdown
<!-- _class: invert -->

# Black Background Slide
```

Black background, white text.

### Distinctive Styles

- **Serif font**: Used for headings
- **Wide margins**: Minimal layout
- **Center alignment**: Content tends to be centered

### Customization Example

```markdown
---
theme: uncover
---

<style>
section {
  font-family: 'Georgia', serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}
</style>
```

## Theme Comparison Table

| Feature | default | gaia | uncover |
|---------|---------|------|---------|
| **Background** | White | Colorful | White/Black |
| **Font** | Sans-serif | Sans-serif | Serif |
| **Colors** | Simple | Vibrant | Minimal |
| **Use Case** | General | Creative | Formal |
| **Style** | Clean | Energetic | Elegant |

## Common Class Specifications

Available in all official themes:

### lead

```markdown
<!-- _class: lead -->
```

- For title slides
- Centered
- Large text
- Hides footer/page numbers

### invert

```markdown
<!-- _class: invert -->
```

- Inverts colors
- Swaps background and text colors
- Dark mode style

## Theme Selection Guidelines

### When to Choose default

- General presentations
- Business use
- Need simple, readable design
- As a base for customization

### When to Choose gaia

- Creative presentations
- Design-related talks
- Youth-oriented audiences
- Need visual impact

### When to Choose uncover

- Formal presentations
- Academic talks
- Minimal design preference
- Want elegant impression

## Combining with Custom Themes

### Extending Official Themes

```css
/* @theme my-custom-default */

@import-theme 'default';

section {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

h1 {
  color: #1e3a8a;
}
```

### Switching Between Multiple Themes

```markdown
---
marp: true
theme: default
---

# Section 1 (default theme)

---

<!-- theme: gaia -->

# Section 2 (gaia theme)

---

<!-- theme: uncover -->

# Section 3 (uncover theme)
```

Note: Theme switching within the same file has limited support.

## Practical Examples

### Using default Theme

```markdown
---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# Project Report

October 2024

---

## Agenda

1. Progress Status
2. Challenges and Solutions
3. Future Plans

---

## Progress Status

- Task A: Completed
- Task B: In Progress
- Task C: On Schedule
```

### Using gaia Theme

```markdown
---
marp: true
theme: gaia
---

<!-- _class: lead -->

# New Product Launch

Innovative Design

---

## Concept

**Three Pillars**

1. 🎨 Beauty
2. 🚀 Speed
3. 💡 Usability
```

### Using uncover Theme

```markdown
---
marp: true
theme: uncover
---

<!-- _class: lead -->

# Research Presentation

Deep Learning Applications

---

## Research Background

Recent technological advances...

---

<!-- _class: invert -->

## Experimental Results

Accuracy: 95.3%
```

## Official References

- **Official Theme Implementation**: https://github.com/marp-team/marp-core/tree/main/themes
- **Marp Core README**: https://github.com/marp-team/marp-core
- **Theme CSS Specification**: https://marpit.marp.app/theme-css

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
