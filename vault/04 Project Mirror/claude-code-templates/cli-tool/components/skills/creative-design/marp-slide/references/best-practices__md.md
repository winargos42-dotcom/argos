---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/creative-design/marp-slide/references/best-practices.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\creative-design\marp-slide\references\best-practices.md
source_ext: .md
source_sha256: f8cbfeda0776b5b7089c82ee7bdbc868f2cdaf6d27612ec477254de699d758c4
text_sha256: 651662ce71673edaa7e0282bf392e5f741b7653dd789d8db08291b18cfe6626c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:35
---

# best-practices.md

- Source: `claude-code-templates/cli-tool/components/skills/creative-design/marp-slide/references/best-practices.md`
- Extract: `text`
- SHA256: `f8cbfeda0776b5b7089c82ee7bdbc868f2cdaf6d27612ec477254de699d758c4`

## Content

# Marp Slide Creation Best Practices

Guidelines for creating "cool" high-quality slides.

## Slide Titles (h2)

### ✅ Good Examples
- **Concise**: About 5-7 characters
- **Clear**: Content is immediately understandable
- **Consistent**: Use the same style at the same hierarchy level

```markdown
## Introduction
## Problem
## Solution
## Results
```

### ❌ Bad Examples
```markdown
## In this section we will explain the introduction
## What are the challenges we are facing
```

## Bullet Points

### ✅ Good Examples
- **3-5 items**: Not too many
- **Concise**: About 15-25 characters per line
- **Parallel**: Same grammatical structure at the same level

```markdown
- Simple and easy to understand
- Unified design
- Effective information delivery
```

### ❌ Bad Examples
```markdown
- This is a very long explanation that doesn't fit on one line and becomes difficult to read
- Short
- The next item is in sentence format. This lack of uniformity makes it hard to read.
```

## Slide Structure

### Basic Structure

1. **Title Slide** (`<!-- _class: lead -->`)
   - Title
   - Presenter name
   - Date

2. **Agenda Slide**
   - Show overall flow
   - About 3-5 items

3. **Content Slides**
   - 1 slide = 1 message
   - Title summarizes content

4. **Summary Slide**
   - Reconfirm key points
   - Words of thanks

### Recommended Slide Count

- 5-minute presentation: 5-8 slides
- 10-minute presentation: 10-15 slides
- 20-minute presentation: 15-25 slides

## Text Amount

### ✅ Good Balance

```markdown
## Product Features

- High-speed processing
- Intuitive UI
- Highly extensible design
```

### ❌ Too Crowded

```markdown
## About the Product

This product was developed using the latest technology.
The main features include the following 7 points:
- Feature 1: Detailed explanation continues at length...
- Feature 2: Even more detailed explanation...
(Continued)
```

## Using Whitespace

- **Adequate whitespace**: Don't cram too much information
- **Visual guidance**: Layout that naturally draws eyes to important information
- **Breathing room**: Appropriate "pauses" between slides

## Using Colors

Leverage colors defined in the theme:
- **Background color**: `#f8f8f4` (light beige)
- **Text color**: `#3a3b5a` (dark navy)
- **Heading color**: `#4f86c6` (blue)
- **Accent color**: `#000000` (black)

### When Using Additional Colors

```markdown
<span style="color: #c62828;">Important point</span>
```

Use sparingly and avoid excessive decoration.

## Using Images

### Effective Usage

- **Clear purpose**: To aid understanding, not just decoration
- **High quality**: Use high-resolution images
- **Appropriate size**: Neither too large nor too small

### Layout Tips

```markdown
# Text on left, image on right
![bg right:40%](image.png)

- Point 1
- Point 2
```

## Font Size Guidelines

Defined in the theme:
- h1: 56px (title slide only)
- h2: 40px (regular slide titles)
- h3: 28px (subheadings)
- Body text: 22px

## Animations and Transitions

Marp does not support animations by default.
Focus on simple slide transitions.

## Checklist

After completing slides, verify:

- [ ] Are titles concise (5-7 characters)?
- [ ] Are bullet points 3-5 items?
- [ ] Is it 1 slide = 1 message?
- [ ] Is the text amount appropriate?
- [ ] Is there sufficient whitespace?
- [ ] Are images used effectively?
- [ ] Is there overall consistency?
- [ ] Is the slide count appropriate?

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
