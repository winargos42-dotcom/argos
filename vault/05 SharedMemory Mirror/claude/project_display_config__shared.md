---
argos_import: sharedmemory_mirror
source_path: claude/project_display_config.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_display_config.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_display_config.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_display_config.md`
- Category: [[Claude Hub]]

## Content

---
name: Настройка экрана ноутбука X230
description: Отключён screensaver и DPMS — экран не тухнет от сети
type: project
originSessionId: f0e9ecac-e2f3-4284-a912-79646f263ea0
---
## Проблема (решена 2026-05-03)
Экран тух через 5 минут при питании от сети, несмотря на настройки XFCE Power Manager.

## Причина
X11 screensaver timeout = 300 сек (независим от XFCE Power Manager).
XFCE Power Manager не перекрывал системный xset.

## Что сделано

### Немедленно (текущая сессия)
```bash
DISPLAY=:0.0 XAUTHORITY=/home/ava/.Xauthority xset s off
DISPLAY=:0.0 XAUTHORITY=/home/ava/.Xauthority xset s noblank
DISPLAY=:0.0 XAUTHORITY=/home/ava/.Xauthority xset -dpms
```

### Постоянно (autostart)
Файл: `/home/ava/.config/autostart/disable-screensaver.desktop`
```ini
[Desktop Entry]
Type=Application
Name=Disable Screensaver
Exec=xset s off -dpms
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
```

## Результат
- Screen Saver timeout: **0** (отключён)
- DPMS: **Disabled**
- Применяется автоматически при каждом входе в XFCE

## Среда
- DE: XFCE, X11 (:0.0)
- Auth: `/home/ava/.Xauthority`

**Why:** пользователь хочет чтобы экран не гас при питании от сети.
**How to apply:** если снова гаснет — проверить `xset q` и наличие autostart файла.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_display_config.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
