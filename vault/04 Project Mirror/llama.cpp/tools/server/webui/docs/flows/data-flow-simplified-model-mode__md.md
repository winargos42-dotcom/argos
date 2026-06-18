---
argos_import: project_file
source_path: llama.cpp/tools/server/webui/docs/flows/data-flow-simplified-model-mode.md
source_abs: F:\debug\argoss\llama.cpp\tools\server\webui\docs\flows\data-flow-simplified-model-mode.md
source_ext: .md
source_sha256: 1a5ea2790bde14917b56deba530ce42533d9635e0a31c184801a9a8105be06aa
text_sha256: 731fab9a3fc0d2df4589dc7a9156f8900c015c5a34fafaf8ca5b4d22080cf7ef
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# data-flow-simplified-model-mode.md

- Source: `llama.cpp/tools/server/webui/docs/flows/data-flow-simplified-model-mode.md`
- Extract: `text`
- SHA256: `1a5ea2790bde14917b56deba530ce42533d9635e0a31c184801a9a8105be06aa`

## Content

```mermaid
%% MODEL Mode Data Flow (single model)
%% Detailed flows: ./flows/server-flow.mmd, ./flows/models-flow.mmd, ./flows/chat-flow.mmd

sequenceDiagram
    participant User as 👤 User
    participant UI as 🧩 UI
    participant Stores as 🗄️ Stores
    participant DB as 💾 IndexedDB
    participant API as 🌐 llama-server

    Note over User,API: 🚀 Initialization (see: server-flow.mmd, models-flow.mmd)

    UI->>Stores: initialize()
    Stores->>DB: load conversations
    Stores->>API: GET /props
    API-->>Stores: server config + modalities
    Stores->>API: GET /v1/models
    API-->>Stores: single model (auto-selected)

    Note over User,API: 💬 Chat Flow (see: chat-flow.mmd)

    User->>UI: send message
    UI->>Stores: sendMessage()
    Stores->>DB: save user message
    Stores->>API: POST /v1/chat/completions (stream)
    loop streaming
        API-->>Stores: SSE chunks
        Stores-->>UI: reactive update
    end
    API-->>Stores: done + timings
    Stores->>DB: save assistant message

    Note over User,API: 🔁 Regenerate

    User->>UI: regenerate
    Stores->>DB: create message branch
    Note right of Stores: same streaming flow

    Note over User,API: ⏹️ Stop

    User->>UI: stop
    Stores->>Stores: abort stream
    Stores->>DB: save partial response
```

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Training Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Training Hub]]
