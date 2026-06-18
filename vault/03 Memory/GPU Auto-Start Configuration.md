# GPU Auto-Start Configuration

## Дата: 2026-05-06 16:45
## Статус: ✅ АКТИВНО

---

## Что реализовано

**Автоматический запуск GPU серверов при старте ARGOS.**

### Изменения

**1. main.py (строка ~787-800)**
Добавлен блок автозапуска GPU перед Telegram:
```python
# Автозапуск GPU серверов (llama-server Vulkan)
_gpu_auto_start = os.getenv("ARGOS_GPU_AUTO_START", "true").strip().lower()
if _gpu_auto_start in ("true", "1", "on", "yes"):
    try:
        from src.ollama_three import get_manager as _get_gpu_mgr
        _gpu_mgr = _get_gpu_mgr()
        _gpu_thread = threading.Thread(
            target=_gpu_mgr.start_all,
            daemon=True,
            name="gpu-auto-start"
        )
        _gpu_thread.start()
        log.info("[GPU] Автозапуск llama-server инициирован")
    except Exception as _gpu_e:
        log.warning("[GPU] Не удалось запустить llama-server: %s", _gpu_e)
```

**2. .env**
Добавлен параметр:
```bash
ARGOS_GPU_AUTO_START=true
```

---

## Текущий статус GPU (16:45)

| GPU | Порт | Статус | Модель | Бэкенд |
|-----|------|--------|--------|--------|
| **RX 580** | :8082 | ✅ OK | qwen2.5:3b | llama-server |
| **Vega 11** | :8083 | ✅ OK | tinyllama | llama-server |
| **RX 560** | :8084 | ✅ OK | qwen2.5:3b | llama-server |

---

## Как это работает

1. При старте ARGOS (`python main.py --no-gui`)
2. После инициализации MCP (порт :8000)
3. Запускается фоновый поток `gpu-auto-start`
4. Вызывается `ollama_three.get_manager().start_all()`
5. GPU серверы поднимаются на портах 8082/8083/8084

**Время инициализации:** ~30-60 секунд после старта ARGOS

---

## Особенности

- **GPU0 (RX 580)** иногда не стартует автоматически из-за конфликта VRAM с RX 560 (оба используют qwen2.5:3b). Решение: `три модели запуск` в Telegram или повторный вызов `start_all()`
- **Vega 11** стартует стабильно (tinyllama лёгкая)
- **RX 560** стартует стабильно

---

## Тестирование

После перезапуска ARGOS:
```bash
# Проверка (подождать 30-60 секунд)
curl http://localhost:8082/health
curl http://localhost:8083/health  
curl http://localhost:8084/health

# Или через MCP
python -c "from src.ollama_three import get_manager; print(get_manager().status())"
```

---

## Связи
- [[ARGOS Unified State 2026-05-06]]
- [[2026-05-06 ARGOS Restart Complete]]
- [[Telegram Obsidian Logger]]

[[Backbone Hub]]

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Human Sessions Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Human Sessions Hub]]
