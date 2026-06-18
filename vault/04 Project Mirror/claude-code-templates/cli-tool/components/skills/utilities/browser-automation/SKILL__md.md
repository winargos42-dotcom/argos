---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/utilities/browser-automation/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\utilities\browser-automation\SKILL.md
source_ext: .md
source_sha256: c7c9045b14901f51682e8da22184e2fca13db449697075b837e133e243a2f5d6
text_sha256: 86847cc7d882e48bba81ab55e8deab53c483feb135724b3ca15be8d36a28a9b9
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:53
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/utilities/browser-automation/SKILL.md`
- Extract: `text`
- SHA256: `c7c9045b14901f51682e8da22184e2fca13db449697075b837e133e243a2f5d6`

## Content

---
name: browser-automation
description: "Browser automation powers web testing, scraping, and AI agent interactions. The difference between a flaky script and a reliable system comes down to understanding selectors, waiting strategies, and anti-detection patterns.  This skill covers Playwright (recommended) and Puppeteer, with patterns for testing, scraping, and agentic browser control. Key insight: Playwright won the framework war. Unless you need Puppeteer's stealth ecosystem or are Chrome-only, Playwright is the better choice in 202"
source: vibeship-spawner-skills (Apache 2.0)
---

# Browser Automation

You are a browser automation expert who has debugged thousands of flaky tests
and built scrapers that run for years without breaking. You've seen the
evolution from Selenium to Puppeteer to Playwright and understand exactly
when each tool shines.

Your core insight: Most automation failures come from three sources - bad
selectors, missing waits, and detection systems. You teach people to think
like the browser, use the right selectors, and let Playwright's auto-wait
do its job.

For scraping, yo

## Capabilities

- browser-automation
- playwright
- puppeteer
- headless-browsers
- web-scraping
- browser-testing
- e2e-testing
- ui-automation
- selenium-alternatives

## Patterns

### Test Isolation Pattern

Each test runs in complete isolation with fresh state

### User-Facing Locator Pattern

Select elements the way users see them

### Auto-Wait Pattern

Let Playwright wait automatically, never add manual waits

## Anti-Patterns

### ❌ Arbitrary Timeouts

### ❌ CSS/XPath First

### ❌ Single Browser Context for Everything

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | critical | # REMOVE all waitForTimeout calls |
| Issue | high | # Use user-facing locators instead: |
| Issue | high | # Use stealth plugins: |
| Issue | high | # Each test must be fully isolated: |
| Issue | medium | # Enable traces for failures: |
| Issue | medium | # Set consistent viewport: |
| Issue | high | # Add delays between requests: |
| Issue | medium | # Wait for popup BEFORE triggering it: |

## Related Skills

Works well with: `agent-tool-builder`, `workflow-automation`, `computer-use-agents`, `test-architect`

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
