# [ARGOS NPU] Микроархитектурный профиль оптимизации

## 1. Борьба с False Sharing (Cache-line alignment)

- Все структуры управляющих стейтов (`_condvar_state_t`) выравнивать на **64 байта**: `alignas(64)`.
- Использовать `static_assert(sizeof(struct_name) == 64)` для контроля размера.
- Внутри структуры заполнять остаток кеш-линии `pad[64 - sizeof(fields)]`, чтобы соседние экземпляры не лежали на одной линии.

## 2. Lock-free ring buffer

- Файлы:
  - `Projects/argoss/src/cas_ring.c` — C extension
  - `Projects/argoss/tools/cas_ring.py` — Python wrapper
  - `Projects/argoss/setup_cas_ring.py` — сборка
  - `Projects/argoss/tests/test_cas_ring.py` — тесты
- Слот кольца: **32 байта данных + 32 байта pad = 64 байта**.
- Head и tail на **разных кеш-линиях**.
- `memory_order_release` для publish, `memory_order_acquire` для consume.
- `__builtin_prefetch(addr, rw, 3)` на `idx + 16` слотов вперёд.
- Fallback на `collections.deque`, если C extension недоступен.

## 3. Spin-loop полиси

- Внутри циклов ожидания CAS/флагов ОБЯЗАТЕЛЬНО `_mm_pause()` / `__builtin_ia32_pause()`.
- Это снижает энергопотребление и тепловыделение при HT-конкуренции.

## 4. Статус

- NPUFSM интегрирован в `xdma_fpga_state_tracer.py`.
- C extension собирается и проходит `pytest` (7/7).
- `driver-prep` приостановлен: Orion ушёл в BSOD (`XDMA.sys`), требуется ручной анализ дампа и безопасная переустановка драйвера `10EE:7022`.

## 5. Следующие шаги

1. Проанализировать `C:\Windows\Minidump\*.dmp` через WinDbg (`!analyze -v`, `lmvm XDMA`).
2. После ребута отключить `10EE:7022`, затем вручную привязать `AXIPCIE.inf` (PIO-only) или найти корректный `XDMA.inf`.
3. Интегрировать `CasRing` в `xdma_ring_trace_logger.py` для zero-copy логирования BAR событий.
4. Прогнать `perf stat -e cache-misses,cycles` на SPSC producer/consumer benchmark.
