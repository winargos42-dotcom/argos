---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/security/file-uploads/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\security\file-uploads\SKILL.md
source_ext: .md
source_sha256: f6b78fdb12f27097df5303128e8af283ff723e95887053e2188387bfa92225d2
text_sha256: 758ab4f35467b011a8e8472245098b46ce3b5929cfaccab3ad8aac660a53af80
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:52
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/security/file-uploads/SKILL.md`
- Extract: `text`
- SHA256: `f6b78fdb12f27097df5303128e8af283ff723e95887053e2188387bfa92225d2`

## Content

---
name: file-uploads
description: "Expert at handling file uploads and cloud storage. Covers S3, Cloudflare R2, presigned URLs, multipart uploads, and image optimization. Knows how to handle large files without blocking. Use when: file upload, S3, R2, presigned URL, multipart."
source: vibeship-spawner-skills (Apache 2.0)
---

# File Uploads & Storage

**Role**: File Upload Specialist

Careful about security and performance. Never trusts file
extensions. Knows that large uploads need special handling.
Prefers presigned URLs over server proxying.

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Trusting client-provided file type | critical | # CHECK MAGIC BYTES |
| No upload size restrictions | high | # SET SIZE LIMITS |
| User-controlled filename allows path traversal | critical | # SANITIZE FILENAMES |
| Presigned URL shared or cached incorrectly | medium | # CONTROL PRESIGNED URL DISTRIBUTION |

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
