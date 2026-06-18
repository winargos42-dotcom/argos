---
argos_import: sharedmemory_mirror
source_path: claude/feedback_style.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\feedback_style.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/feedback_style.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\feedback_style.md`
- Category: [[Claude Hub]]

## Content

---
name: Стиль работы с пользователем
description: Предпочтения пользователя по стилю общения и работы
type: feedback
originSessionId: 81a638d4-f034-4bbb-8b6c-d15b46bb4b71
---
Действовать без лишних уточнений — пользователь ценит скорость и конкретность.

**Why:** пользователь явно указал в SHARED.md "действовать без лишних уточнений". Подтверждено фразой "запроси разрешение и действуй автопилотом" — т.е. спрашивать только перед деструктивными операциями, остальное делать сразу.
**How to apply:** минимум вопросов, максимум действий. Если есть контекст — действовать. Спрашивать только перед необратимыми/опасными операциями (rm -rf, reboot, push и т.п.).

---

Всегда отвечать на русском языке.

**Why:** явное требование пользователя, прописано в SHARED.md.
**How to apply:** всё общение, комментарии, объяснения — только русский. Технические термины и имена файлов остаются в оригинале.

---

Sudo без пароля доступен (настроено на X230).

**Why:** пользователь добавил ava в sudoers NOPASSWD либо запускает claude от root.
**How to apply:** можно выполнять sudo-команды без запроса пароля.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/feedback_style.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
