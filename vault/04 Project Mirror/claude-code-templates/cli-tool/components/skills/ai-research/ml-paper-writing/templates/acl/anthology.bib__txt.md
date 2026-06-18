---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/ml-paper-writing/templates/acl/anthology.bib.txt
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\ml-paper-writing\templates\acl\anthology.bib.txt
source_ext: .txt
source_sha256: 8c46ed0e8516e3d96caba9fffda9d2fc2054becf08245ff9032cbde82bdf0927
text_sha256: 2b78d2d9aeda62e14c4e46099e8225b5fc116387d8e0a54aad776485e249ceff
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:32
---

# anthology.bib.txt

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/ml-paper-writing/templates/acl/anthology.bib.txt`
- Extract: `text`
- SHA256: `8c46ed0e8516e3d96caba9fffda9d2fc2054becf08245ff9032cbde82bdf0927`

## Content

For citing papers in the ACL Anthology, we provide a single consolidated
BibTeX file containing all of its papers. The bibkeys in these papers are
designed to be semantic in nature: {names}-{year}-{words}, where
- `names` is the concatenated last names of the authors when there is just
  one or two authors, or `lastname-etal` for 3+
- `year` is the four-digit year
- `words` is the first significant word in the title, or more, if necessary,
  to preserve uniqueness

For example, https://aclanthology.org/N04-1035 can be cited as \cite{galley-etal-2004-whats}.

The consolidated file can be downloaded from here:
- https://aclanthology.org/anthology.bib

Unfortunately, as of 2024 or so, this file is now larger than 50 MB, which is Overleaf's
bib file size limit. Consequently, the Anthology shards the file automatically into
49 MB shards.

There are currently (2025) two files:
- https://aclanthology.org/anthology-1.bib
- https://aclanthology.org/anthology-2.bib

You can download these directly from Overleaf from New File -> From External URL,
and then adding them to the \bibliography line in acl_latex.tex:

    \bibliography{custom,anthology-1,anthology-2}

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
