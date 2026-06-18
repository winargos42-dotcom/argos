# ARGOS Architecture

## Overview
ARGOS Universal OS v2.1.3 — self-reproducing cross-platform AI ecosystem.

## Topology
```
ПК (СЕРВЕР) 192.168.1.66                    Ноутбук (Arch Linux)
─────────────────────────                  ──────────────────────
F:\debug\аргос\ ←──SSH──→  ARGOS vault     
C:\Users\AvA\OneDrive\     ←──SCP──→       SharedMemory/
Ollama 3x GPU              ←──sync──→       /home/ava/Projects/argoss/
Home Assistant :8123                        .venv Python env
Zigbee2MQTT                                 
```

## Obsidian (Единая система)
```
ARGOS vault (главный)
├── /home/ava/Projects/argoss/vault/  ← ноутбук
├── F:\debug\аргос\                    ← ПК (сервер)
├── 00 Memory Web / 01 Projects / 02 Logs
├── 03 Memory / 04 Project Mirror / 05 SharedMemory Mirror
├── 06 Link Stubs / 07 Duplicates Archive
├── Daily / Excalidraw / SharedMemory (→ MyObsidianVault)
├── SERVER.md — конфигурация сервера
├── Architecture.md — этот файл
└── Tasks.md — задачи

Точки входа:
  Obsidian Vault/ARGOS → /Projects/argoss/vault/
  MyObsidianVault/ARGOS → /Projects/argoss/vault/
  SharedMemory → MyObsidianVault/SharedMemory/
```

## Синхронизация
| Скрипт | Интервал | Что |
|--------|----------|-----|
| sync-obsidian-memory.py | 2 мин | SharedMemory + ARGOS vault ↔ ПК |
| vault-sync.sh | 5 мин | claude/, shared/, argos/, opencode/ → ПК |

## Components
- **AWA-Core** — central module coordinator
- **ColibriAsmEngine** — real-time microcode assembler/disassembler
- **Ollama Three GPU** — 3-GPU local inference (src/ollama_three.py)
- **AI Failover** — circuit breaker pattern (3 failures -> fallback)
- **Web Learn** — DuckDuckGo search module

## AI Provider Stack
```
Cloud providers (7 active):
  DeepSeek, Gemini, Grok, OpenAI, WatsonX, Kimi
  + GigaChat, YandexGPT, Groq, Cloudflare (keys pending)

Local inference (3 GPU):
  RX 580:8082  -> qwen2.5:3b (smart)
  Vega11:8083  -> tinyllama (fast)
  RX 560:8084  -> qwen2.5-coder:7b (code)
```

## Key Files
- `main.py` — оркестратор (входная точка)
- `src/core.py` — ядро ARGOS
- `src/ollama_three.py` — 3-GPU менеджер
- `src/ai_failover.py` — failover логика
- `src/consciousness.py` — ArgosConsciousness
- `src/awareness.py` — ArgosAwareness
- `src/curiosity.py` — ArgosCuriosity
- `src/self_sustain.py` — SelfSustainEngine

## Tags
#argos #architecture #gpu #ollama #server
