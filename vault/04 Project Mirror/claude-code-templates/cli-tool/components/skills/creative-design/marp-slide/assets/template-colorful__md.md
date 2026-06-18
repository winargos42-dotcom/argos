---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/creative-design/marp-slide/assets/template-colorful.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\creative-design\marp-slide\assets\template-colorful.md
source_ext: .md
source_sha256: 76dd50b8c070747422a123d594e4c4263ddb652cb206ef6ccfd1772d4df6510c
text_sha256: efaf844952d271184cfb0c895fc2e638b48c94ca19b11accf8cce6457563e53f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:35
---

# template-colorful.md

- Source: `claude-code-templates/cli-tool/components/skills/creative-design/marp-slide/assets/template-colorful.md`
- Extract: `text`
- SHA256: `76dd50b8c070747422a123d594e4c4263ddb652cb206ef6ccfd1772d4df6510c`

## Content

---
marp: true
theme: default
paginate: true
---

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap');

:root {
  --color-background: #fff5f7;
  --color-foreground: #2d2d2d;
  --color-heading: #ff6b9d;
  --color-accent-1: #ffd93d;
  --color-accent-2: #6bcf7f;
  --color-accent-3: #4d96ff;
  --font-default: 'Noto Sans JP', 'Hiragino Kaku Gothic ProN', 'Meiryo', sans-serif;
}

section {
  background: linear-gradient(135deg, var(--color-background) 0%, #ffe5ec 100%);
  color: var(--color-foreground);
  font-family: var(--font-default);
  font-weight: 400;
  box-sizing: border-box;
  border-bottom: 10px solid var(--color-accent-1);
  position: relative;
  line-height: 1.7;
  font-size: 24px;
  padding: 56px;
}

section:last-of-type {
  border-bottom: none;
}

h1, h2, h3, h4, h5, h6 {
  font-weight: 900;
  color: var(--color-heading);
  margin: 0;
  padding: 0;
}

h1 {
  font-size: 64px;
  line-height: 1.3;
  text-align: left;
  background: linear-gradient(135deg, var(--color-heading), var(--color-accent-3));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

h2 {
  position: absolute;
  top: 40px;
  left: 56px;
  right: 56px;
  font-size: 44px;
  padding-top: 0;
  padding-bottom: 20px;
  background: linear-gradient(90deg, var(--color-heading), var(--color-accent-3));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

h2::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 8px;
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, var(--color-accent-1), var(--color-accent-2), var(--color-accent-3));
  border-radius: 2px;
}

h2 + * {
  margin-top: 120px;
}

h3 {
  color: var(--color-accent-3);
  font-size: 30px;
  margin-top: 32px;
  margin-bottom: 12px;
}

ul, ol {
  padding-left: 32px;
}

li {
  margin-bottom: 12px;
}

footer {
  font-size: 0;
  color: transparent;
  position: absolute;
  left: 56px;
  right: 56px;
  bottom: 40px;
  height: 10px;
  background: linear-gradient(90deg, var(--color-accent-1), var(--color-accent-2), var(--color-accent-3));
  border-radius: 5px;
}

section.lead {
  border-bottom: 10px solid var(--color-accent-1);
  background: linear-gradient(135deg, #fff5f7 0%, #ffe5ec 50%, #ffd5e0 100%);
}

section.lead footer {
  display: none;
}

section.lead h1 {
  margin-bottom: 24px;
}

section.lead p {
  font-size: 26px;
  color: var(--color-foreground);
  font-weight: 700;
}

strong {
  color: var(--color-heading);
  font-weight: 900;
}
</style>

<!-- _class: lead -->

# プレゼンテーション

カラフル＆ポップ

---

## アジェンダ

- トピック1
- トピック2
- トピック3

---

## スライド

- ポイント1
- ポイント2
- ポイント3

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
