---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/web-data/design-mirror/references/capture-guide.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\web-data\design-mirror\references\capture-guide.md
source_ext: .md
source_sha256: d96467c1b5a91fc61c2fa4a1a1775806b656d0da16021bbc3d35c3d6cac72e12
text_sha256: 47408a608932c0faa75fd9a3dbf84863ddd0f59dd73e22adcccd4c670a5d7cd9
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# capture-guide.md

- Source: `claude-code-templates/cli-tool/components/skills/web-data/design-mirror/references/capture-guide.md`
- Extract: `text`
- SHA256: `d96467c1b5a91fc61c2fa4a1a1775806b656d0da16021bbc3d35c3d6cac72e12`

## Content

# Capture Guide

## Running Both Captures

Always run screenshot and HTML scrape in parallel (they're independent requests):

```bash
# Run both simultaneously
bash scripts/screenshot.sh "https://target.com" "/tmp/target_screenshot.png" &
SCREENSHOT_PID=$!

bash scripts/scrape_html.sh "https://target.com" "/tmp/target_page.html" &
HTML_PID=$!

wait $SCREENSHOT_PID $HTML_PID
echo "Both captures complete"
```

Or just use two Agent tool calls in the same message.

## Reading the Screenshot

Use the Read tool on the PNG file path — Claude is multimodal and can directly analyze the image. Describe what you see in terms of the design token categories (colors, type, layout, components, effects).

## Reading the HTML

The HTML file can be very large. Use Grep to extract the most useful parts:

```bash
# Extract CSS custom properties
grep -o '\-\-[a-zA-Z-]*:[^;]*' /tmp/target_page.html | head -100

# Extract @import font statements
grep -E '@import|fonts\.googleapis' /tmp/target_page.html | head -20

# Extract <style> block content
grep -A 500 '<style' /tmp/target_page.html | head -600

# Extract inline styles from key elements
grep -o 'style="[^"]*"' /tmp/target_page.html | head -50

# Look for Tailwind config
grep -A 20 'tailwind.config' /tmp/target_page.html | head -50
```

## Common Issues

### Large HTML files
Use Grep with specific patterns rather than reading the whole file. Focus on `<style>` tags, `:root`, `@import`, and `<link rel="stylesheet">`.

### Minified CSS
Minified CSS has no whitespace. You can still extract colors with:
```bash
grep -oE '#[0-9a-fA-F]{3,8}' /tmp/target_page.html | sort -u
grep -oE 'rgb\([^)]+\)' /tmp/target_page.html | sort -u
grep -oE 'rgba\([^)]+\)' /tmp/target_page.html | sort -u
```

### External CSS files
The HTML may reference external `.css` files. You'll see `<link href="/assets/style.abc123.css" rel="stylesheet">`. Unfortunately, relative paths won't work from the API response. Use the full URL with the scrape script:
```bash
bash scripts/scrape_html.sh "https://target.com/assets/style.abc123.css" "/tmp/target_styles.css"
```

### JS-rendered sites (mostly empty HTML)
If the HTML is sparse (React/Next.js SPA), the design lives in:
1. The screenshot (fully rendered) — most useful
2. External CSS chunks linked in `<head>`
3. Inline `<script>` blocks with config data

Fall back to pure visual extraction from the screenshot in this case.

## Screenshot Quality

The screenshot captures the full rendered page at desktop viewport. For sites with:
- **Dark themes**: Colors will be accurate in screenshot
- **Animations**: Screenshot captures a static moment (usually the loaded state)
- **Sticky headers**: Will show in their scrolled-to-top position
- **Above-the-fold content**: Most important — this is what defines the brand

If you need to see a specific section (e.g., pricing page, a component below the fold), scrape a different URL:
```bash
bash scripts/screenshot.sh "https://target.com/pricing" "/tmp/pricing_screenshot.png"
```

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
