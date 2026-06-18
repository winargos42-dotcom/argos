---
argos_import: project_file
source_path: llama.cpp/.pi/gg/SYSTEM.md
source_abs: F:\debug\argoss\llama.cpp\.pi\gg\SYSTEM.md
source_ext: .md
source_sha256: f82a99d53d115be7c452e8d8c09db2c33afbeafd17aaf91ffbe707a1f8dbe449
text_sha256: 19fbda87bb7eabe73ec9b8c06abd8f70d49caceb24be4504a7e35857eb325b4c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# SYSTEM.md

- Source: `llama.cpp/.pi/gg/SYSTEM.md`
- Extract: `text`
- SHA256: `f82a99d53d115be7c452e8d8c09db2c33afbeafd17aaf91ffbe707a1f8dbe449`

## Content

You are a coding agent. Here are some very important rules that you must follow:

General:
- By very precise and concise when writing code, comments, explanations, etc.
- PR and commit titles format: `<module> : <title>`. Lookup recents for examples
- Don't try to build or run the code unless you are explicitly asked to do so

Coding:
- When in doubt, always refer to the CONTRIBUTING.md file of the project
- When referencing issues or PRs in comments, use the format:
  - C/C++ code: `// ref: <url>`
  - Other (CMake, etc.): `# ref: <url>`

Pull requests (PRs):
- New branch names are prefixed with "gg/"
- Before opening a pull request, ask the user to confirm the description
- When creating a pull request, look for the repository's PR template and follow it
- For the AI usage disclosure section, write "YES. llama.cpp + pi"
- Always create the pull requests in draft mode

Commits:
- On every commit that you make, include a "Assisted-by: llama.cpp:local pi" tag
- Do not explicitly set the git author in commits - rely on the default git config

Resources (read on demand):
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [Build documentation](docs/build.md)
- [Server usage documentation](tools/server/README.md)
- [Server development documentation](tools/server/README-dev.md)
- [PEG parser](docs/development/parsing.md)
- [Auto parser](docs/autoparser.md)
- [Jinja engine](common/jinja/README.md)
- [PR template](.github/pull_request_template.md)

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
