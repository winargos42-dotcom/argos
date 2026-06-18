---
argos_import: sharedmemory_mirror
source_path: claude/project_pc_hardware.md
source_abs: C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_pc_hardware.md
mirrored_at: 2026-05-10 14:00:58
---

# SharedMemory: claude/project_pc_hardware.md

- Source: `C:\Users\AvA\OneDrive\ObsidianShared\SharedMemory\claude\project_pc_hardware.md`
- Category: [[Claude Hub]]

## Content

---
name: Железо ПК (Windows, 192.168.1.66)
description: Полные характеристики ПК — материнка, CPU, RAM, GPU, диски, PCIe слоты
type: project
originSessionId: f0e9ecac-e2f3-4284-a912-79646f263ea0
---
## Материнская плата
- **ASUS PRIME X370-PRO** (AM4, X370 chipset)

## CPU
- AMD Ryzen 5 3350G (4 ядра / 8 потоков, 3.8 GHz, встроенный Vega 11)

## RAM
- 48 GB DDR4-2133 (4 планки: 16+8+16+8 GB)

## GPU кластер
| Слот | GPU | VRAM | Порт Ollama |
|------|-----|------|------------|
| PCIEX16_1 (x8) | RX 580 | 4 GB | :8082 |
| PCIEX16_3 (x4) | RX 560 | 4 GB | :8084 |
| встроена в CPU | Vega 11 | 2 GB shared | :8083 |

## Ожидается (~2026-06-03)
- **Tesla V100 PCIe 16GB** → в PCIEX16_1 (x8)
- RX 580 переедет в PCIEX16_3 (x4) или будет убрана

## PCIe слоты
| Слот | Состояние | Ширина |
|------|-----------|--------|
| PCIEX16_1 | Занят (RX 580) | x8 electrical |
| PCIEX16_2 | **Свободен** ← V100 сюда | x8 electrical |
| PCIEX16_3 | Занят (RX 560) | x4 electrical |
| PCIEX1_1/2/3 | Свободны | x1 |

## Диски
| Модель | Тип | Размер |
|--------|-----|--------|
| SPCC M.2 PCIe SSD | NVMe | 512 GB |
| WDC WD10EZEX | HDD | 1 TB |
| TOSHIBA MQ01ABD100 | HDD | 1 TB |
| WDC WD5000AADS | HDD | 500 GB |
| ST9250315AS | HDD | 250 GB |
| KINGSTON SA400S37 | USB SSD | 120 GB |

## Блок питания
- **1000W** — достаточно для V100 (250W) + RX580 (150W) + RX560 (80W) = ~480W пик

## Сеть
- IP локальный: 192.168.1.66
- SSH: `ssh AvA@192.168.1.66` или `ssh argos-pc` (через Cloudflare)
- Хост: DESKTO, пользователь AvA

## После установки V100 — итоговый VRAM кластера
V100 16GB + RX580 4GB + RX560 4GB + Vega11 2GB = **26 GB**

**Why:** нужно знать параметры для планирования установки V100 и расстановки слотов.
**How to apply:** при установке V100 — переставить RX580 в PCIEX16_3, V100 в PCIEX16_1.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Claude Hub]]
- Общая память: [[SharedMemory Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- SharedMemory source: `claude/project_pc_hardware.md`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Claude Hub]]
