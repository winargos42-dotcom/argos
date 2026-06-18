---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/realtimekit/README.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\realtimekit\README.md
source_ext: .md
source_sha256: 3932d4aa42e333e175e1df7d2e05e4e3c8f308389c17aedf277023687ef5bd41
text_sha256: 190ecae4bb2ed00795cec6b59df4b0b3045cbc07d09b818abe398c239e97d531
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# README.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/realtimekit/README.md`
- Extract: `text`
- SHA256: `3932d4aa42e333e175e1df7d2e05e4e3c8f308389c17aedf277023687ef5bd41`

## Content

# Cloudflare RealtimeKit

Expert guidance for building real-time video and audio applications using **Cloudflare RealtimeKit** - a comprehensive SDK suite for adding customizable live video and voice to web or mobile applications.

## Overview

RealtimeKit is Cloudflare's SDK suite built on Realtime SFU, abstracting WebRTC complexity with fast integration, pre-built UI components, global performance (300+ cities), and production features (recording, transcription, chat, polls).

**Use cases**: Team meetings, webinars, social video, audio calls, interactive plugins

## Core Concepts

- **App**: Workspace grouping meetings, participants, presets, recordings. Use separate Apps for staging/production
- **Meeting**: Re-usable virtual room. Each join creates new **Session**
- **Session**: Live meeting instance. Created on first join, ends after last leave
- **Participant**: User added via REST API. Returns `authToken` for client SDK. **Do not reuse tokens**
- **Preset**: Reusable permission/UI template (permissions, meeting type, theme). Applied at participant creation
- **Peer ID** (`id`): Unique per session, changes on rejoin
- **Participant ID** (`userId`): Persistent across sessions

## Quick Start

### 1. Create App & Meeting (Backend)

```bash
# Create app
curl -X POST 'https://api.cloudflare.com/client/v4/accounts/<account_id>/realtime/kit/apps' \
  -H 'Authorization: Bearer <api_token>' \
  -d '{"name": "My RealtimeKit App"}'

# Create meeting
curl -X POST 'https://api.cloudflare.com/client/v4/accounts/<account_id>/realtime/kit/<app_id>/meetings' \
  -H 'Authorization: Bearer <api_token>' \
  -d '{"title": "Team Standup"}'

# Add participant
curl -X POST 'https://api.cloudflare.com/client/v4/accounts/<account_id>/realtime/kit/<app_id>/meetings/<meeting_id>/participants' \
  -H 'Authorization: Bearer <api_token>' \
  -d '{"name": "Alice", "preset_name": "host"}'
# Returns: { authToken }
```

### 2. Client Integration

**React**:
```tsx
import { RtkMeeting } from '@cloudflare/realtimekit-react-ui';

function App() {
  return <RtkMeeting authToken="<participant_auth_token>" onLeave={() => {}} />;
}
```

**Core SDK**:
```typescript
import RealtimeKitClient from '@cloudflare/realtimekit';

const meeting = new RealtimeKitClient({ authToken: '<token>', video: true, audio: true });
await meeting.join();
```

## Reading Order

| Task | Files |
|------|-------|
| Quick integration | README only |
| Custom UI | README → patterns → api |
| Backend setup | README → configuration |
| Debug issues | gotchas |
| Advanced features | patterns → api |

## RealtimeKit vs Realtime SFU

| Choose | When |
|--------|------|
| **RealtimeKit** | Need pre-built UI, fast integration, React/Angular/HTML |
| **Realtime SFU** | Building from scratch, custom WebRTC, full control |

RealtimeKit is built on Realtime SFU but abstracts WebRTC complexity with UI components and SDKs.

## Which Package?

Need pre-built meeting UI?
- React → `@cloudflare/realtimekit-react-ui` (`<RtkMeeting>`)
- Angular → `@cloudflare/realtimekit-angular-ui`
- HTML/Vanilla → `@cloudflare/realtimekit-ui`

Need custom UI?
- Core SDK → `@cloudflare/realtimekit` (RealtimeKitClient) - full control

Need raw WebRTC control?
- See `realtime-sfu/` reference

## In This Reference

- [Configuration](./configuration.md) - Setup, installation, wrangler config
- [API](./api.md) - Meeting object, REST API, SDK methods
- [Patterns](./patterns.md) - Common workflows, code examples
- [Gotchas](./gotchas.md) - Common issues, troubleshooting

## See Also

- [Workers](../workers/) - Backend integration
- [D1](../d1/) - Meeting metadata storage
- [R2](../r2/) - Recording storage
- [KV](../kv/) - Session management

## Reference Links

- **Official Docs**: https://developers.cloudflare.com/realtime/realtimekit/
- **API Reference**: https://developers.cloudflare.com/api/resources/realtime_kit/
- **Examples**: https://github.com/cloudflare/realtimekit-web-examples
- **Dashboard**: https://dash.cloudflare.com/?to=/:account/realtime/kit

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
