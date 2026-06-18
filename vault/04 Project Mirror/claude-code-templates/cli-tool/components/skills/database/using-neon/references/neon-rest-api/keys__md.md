---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/database/using-neon/references/neon-rest-api/keys.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\database\using-neon\references\neon-rest-api\keys.md
source_ext: .md
source_sha256: d49efe78141bfd8fe72fa6ed64bd4c1ae1228fa13fabe84791df48e54a7fc565
text_sha256: 6ec390129642a5dc724b3a651ad80640aacc3ca833f95f606895fdfd8a6cdaf3
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# keys.md

- Source: `claude-code-templates/cli-tool/components/skills/database/using-neon/references/neon-rest-api/keys.md`
- Extract: `text`
- SHA256: `d49efe78141bfd8fe72fa6ed64bd4c1ae1228fa13fabe84791df48e54a7fc565`

## Content

## Overview

This document outlines the rules for managing Neon API keys programmatically. It covers listing existing keys, creating new keys, and revoking keys.

### Important note on creating API keys

To create new API keys using the API, you must already possess a valid Personal API Key. The first key must be created from the Neon Console. You can ask the user to create one for you if you do not have one.

### List API keys

- Endpoint: `GET /api_keys`
- Authorization: Use a Personal API Key.

Example request:

```bash
curl "https://console.neon.tech/api/v2/api_keys" \
  -H "Authorization: Bearer $PERSONAL_API_KEY"
```

Example response:

```json
[
  {
    "id": 2291506,
    "name": "my-personal-key",
    "created_at": "2025-09-10T09:44:04Z",
    "created_by": {
      "id": "487de658-08ba-4363-b387-86d18b9ad1c8",
      "name": "<USER_NAME>",
      "image": "<USER_IMAGE_URL>"
    },
    "last_used_at": "2025-09-10T09:44:09Z",
    "last_used_from_addr": "49.43.218.132,34.211.200.85"
  }
]
```

### Create an API key

- Endpoint: `POST /api_keys`
- Authorization: Use a Personal API Key.
- Body: Must include a `key_name`.

Example request:

```bash
curl https://console.neon.tech/api/v2/api_keys \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PERSONAL_API_KEY" \
  -d '{"key_name": "my-new-key"}'
```

Example response:

```json
{
  "id": 2291515,
  "key": "napi_9tlr13774gizljemrr133j5koy3bmsphj8iu38mh0yjl9q4r1b0jy2wuhhuxouzr",
  "name": "my-new-key",
  "created_at": "2025-09-10T09:47:59Z",
  "created_by": "487de658-08ba-4363-b387-86d18b9ad1c8"
}
```

### Revoke an API key

- Endpoint: `DELETE /api_keys/{key_id}`
- Authorization: Use a Personal API Key.

Example request:

```bash
curl -X DELETE \
  'https://console.neon.tech/api/v2/api_keys/2291515' \
  -H "Authorization: Bearer $PERSONAL_API_KEY"
```

Example response:

```json
{
  "id": 2291515,
  "name": "mynewkey",
  "created_at": "2025-09-10T09:47:59Z",
  "created_by": "487de658-08ba-4363-b387-86d18b9ad1c8",
  "last_used_at": "2025-09-10T09:53:01Z",
  "last_used_from_addr": "2405:201:c01f:7013:d962:2b4f:2740:9750",
  "revoked": true
}
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
