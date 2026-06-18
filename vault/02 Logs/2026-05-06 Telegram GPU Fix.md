# Диагностика Telegram + GPU 2026-05-06

## Проблема
**Ошибка в Telegram:** `No API provider registered for api: ollama`

**Когда:** 2026-05-06 14:56-15:05

## Диагностика

### 1. Проверка GPU серверов
**Статус:** GPU llama-server НЕ были запущены
- :8082 RX 580 — НЕТ ОТВЕТА
- :8083 Vega 11 — НЕТ ОТВЕТА  
- :8084 RX 560 — НЕТ ОТВЕТА

### 2. Причина
ARGOS запустился, но GPU серверы (llama-server Vulkan) не были инициализированы. При получении сообщения в Telegram, ARGOS пытался использовать AI_MODE=local-gpu, но провайдер Ollama не был доступен.

### 3. Решение
Запуск GPU серверов через `ollama_three.py`:
```python
from src.ollama_three import get_manager
mgr = get_manager()
mgr.start_all()
```

**Результат:**
- ✅ :8082 RX 580 → qwen2.5:3b (Умная)
- ✅ :8083 Vega 11 → tinyllama (Быстрая)
- ✅ :8084 RX 560 → qwen2.5:3b (Код)

### 4. Проверка MCP
- ✅ MCP: http://127.0.0.1:8000 (ONLINE)
- ✅ AI_MODE: Auto
- ✅ Uptime: 176s
- ✅ CPU: 93.9%
- ✅ RAM: 60.9%

### 5. Проверка llama-server
- ✅ :8082 — Listen (llama-server)
- ✅ :8083 — Listen (llama-server)
- ✅ :8084 — Listen (llama-server)

## Вывод
Проблема решена. GPU серверы запущены, Telegram должен работать корректно.

## Рекомендация
Добавить автозапуск GPU серверов при старте ARGOS, чтобы избежать подобных проблем в будущем.

---

## Команды для проверки

```bash
# Проверка GPU
python -c "from src.ollama_three import get_manager; print(get_manager().status())"

# Проверка MCP
curl http://127.0.0.1:8000/health

# Запуск GPU
python -c "from src.ollama_three import get_manager; print(get_manager().start_all())"
```

[[ARGOS Unified State 2026-05-06]]

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Logs Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Logs Hub]]
