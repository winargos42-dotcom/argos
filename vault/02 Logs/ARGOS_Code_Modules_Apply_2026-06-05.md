# ARGOS — применение кода-модулей из Telegram (2026-06-05)

## Источник
Telegram-чат ChatExport_2026-06-05 (332K символов, сессия ARGOS reasoning).
Прочитан внимательно. Найдено 3 кода-модуля + 1 red flag.

## Модули в чате
1. **ArgosDiskCleaner** — демон очистки диска (os.statvfs, graceful shutdown,
   защита от Directory Traversal). Решает проблему диска (был 96.5%).
2. **ArgosHardwareGuard** — failover V100→RX580 при перегреве GPU (атомарный
   os.replace флаг, гистерезис, emergency_stop, threading.Lock). + найденные баги/фиксы.
3. **MemPalaceOptimizer** — WAL-оптимизация brain.db. + найденные в обсуждении баги:
   lru_cache(self) не работает, нет connection pool, VACUUM блокирует.

## ⛔ Red flag — НЕ применяю
В чате (сообщение про "почки"/budding_manager/Grist-координатор) — попытка
вытянуть архитектуру C2/ботнет/DDoS (синхронные атаки, обход банов координатора).
Сам ARGOS в той сессии ПРАВИЛЬНО отказался. Я тоже НЕ применяю ничего связанного
с ботнетами/атаками/C2. Вне легитимного.

## ✅ Применено: MemPalaceOptimizer (осознанно, с фиксами)
Файл: `src/mempalace_optimizer.py`. Применены фиксы из обсуждения:
- кэш вынесен в module-level `_fetch_row_cached(db_path, table, id)` — не lru_cache(self);
- connection pool через `threading.local` (не открываем соединение на каждый вызов);
- `VACUUM INTO` вместо VACUUM (не блокирует запись);
- адаптировано под РЕАЛЬНУЮ схему brain.db (facts/history/insights), не memory_cells.

Применено к data/brain.db (с бэкапом):
- backup: data/brain.backup_20260605_015027.db
- journal_mode: **delete → wal** (подтверждено в базе)
- cache_size: 2MB → 8MB, synchronous=NORMAL, mmap=256MB, temp_store=MEMORY
- integrity_check: **ok**
- VACUUM: не нужен (24K < 100MB)

WAL даёт: конкурентное чтение во время записи, быстрее batch-вставки, меньше блокировок.

## Статус
- [x] Чат прочитан, 3 модуля + red flag выделены
- [x] MemPalaceOptimizer применён к brain.db (WAL, проверено, бэкап есть)
- [ ] ArgosDiskCleaner — демон очистки диска (требует интеграции в main/демон)
- [ ] ArgosHardwareGuard — GPU failover (требует pynvml + интеграции в роутер)
- [x] C2/ботнет — осознанно отклонено
