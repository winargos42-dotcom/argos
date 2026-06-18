---
argos_import: project_file
source_path: tmp/kolibrios/contrib/network/webview_proxy/README.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\network\webview_proxy\README.txt
source_ext: .txt
source_sha256: 9c10b591be407d0f5b3a6ba50e1c9afe75a22884c36ee0e4891f7523d44fa297
text_sha256: 2ed5dd9d4f9e87bf4edee0d65fb404f43cd14700b759e3090f3860347fe10af7
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:27
---

# README.txt

- Source: `tmp/kolibrios/contrib/network/webview_proxy/README.txt`
- Extract: `text`
- SHA256: `9c10b591be407d0f5b3a6ba50e1c9afe75a22884c36ee0e4891f7523d44fa297`

## Content

Web Proxy for WebView Browser (/programs/cmm/browser)
=====================================================

How to use it?
==============

1. Put this proxy.php to your WebServer which:
- supports PHP
- has curl binary which can be called in shell

2. Edit UserAgent in $your_useragent variable in proxy.php if needed

3. Change content of $your_local_page_address:
- you should write path from HTTP-server root to your file (if proxy.php (or any other name) is in /srv/http/dir1/proxy.php on your disk, then use '/dir1/proxy.php')
- if you renamed proxy.php as index.php:
  - if your browser calls something like http://yoursite.domain/dir1/index.php?site=..., then nothing should be changed
  - if your browser calls something like http://yoursite.domain/dir1/?site=..., then remove 'index.php' at path ending (example: '/dir1/')

4. Change a proxy address in WebView source code (line where is something like http://somename.domain/?site=) to your address with '?site=' at the end. Recompile the browser.

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
