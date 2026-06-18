---
argos_import: project_file
source_path: reports/mcp_phase_fast_2026-05-04.md
source_abs: F:\debug\argoss\reports\mcp_phase_fast_2026-05-04.md
source_ext: .md
source_sha256: 6c9552a4ed27dd4d5982cb1c3f81dd38bd21d1bbd5b88cd51615f0edd1b111bc
text_sha256: 2bc095a398d26063e5bac2d1c57f5a449e7af6f2757a4d2f3b4a65e952cece29
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-05 04:50:02
---

# mcp_phase_fast_2026-05-04.md

- Source: `reports/mcp_phase_fast_2026-05-04.md`
- Extract: `text`
- SHA256: `6c9552a4ed27dd4d5982cb1c3f81dd38bd21d1bbd5b88cd51615f0edd1b111bc`

## Content

﻿# MCP Phase Audit: fast

- Endpoint: http://localhost:8000/mcp
- Timestamp: 2026-05-05 04:48:03

## status
- status: ok
- duration_ms: 2383
- args_json: {}
~~~text
{'ok': True, 'uptime_seconds': 106, 'ai_mode': 'Auto', 'cpu_pct': 89.5, 'ram_pct': 33.4}
~~~

## providers
- status: ok
- duration_ms: 13
- args_json: {}
~~~text
ð¤ AI-ÐÐ ÐÐÐÐÐÐÐ Ð« (Ð»Ð¸Ð¼Ð¸ÑÑ Ð±ÐµÑÐ¿Ð»Ð°ÑÐ½Ð¾Ð³Ð¾ ÑÑÐ¾Ð²Ð½Ñ):

  â DeepSeek (V3 / R1)
     RPM=15 | ÐºÐ¾Ð½ÑÐµÐºÑÑ=128k
     ÐÐ²Ð¾ÑÐ°: ~2â5 Ð¼Ð»Ð½ ÑÐ¾ÐºÐµÐ½Ð¾Ð² Ð¿ÑÐ¸ ÑÐµÐ³Ð¸ÑÑÑÐ°ÑÐ¸Ð¸ (ÑÐ°Ð·Ð¾Ð²Ð¾)
     ÐÐ»ÑÑ: DEEPSEEK_API_KEY
  ð GigaChat (Ð¡Ð±ÐµÑ)
     RPM=60 | ÐºÐ¾Ð½ÑÐµÐºÑÑ=32k
     ÐÐ²Ð¾ÑÐ°: 1 000 000 ÑÐ¾ÐºÐµÐ½Ð¾Ð² (ÑÐ°Ð·Ð¾Ð²Ð¾ Ð¿ÑÐ¸ ÑÐµÐ³Ð¸ÑÑÑÐ°ÑÐ¸Ð¸)
     ÐÐ»ÑÑ: GIGACHAT_API_KEY
  ð YandexGPT (Lite)
     RPH=300 | ÐºÐ¾Ð½ÑÐµÐºÑÑ=32k
     ÐÐ²Ð¾ÑÐ°: ÐÑÐ°Ð½Ñ ~4 000 â½ Ð½Ð° 60 Ð´Ð½ÐµÐ¹
     ÐÐ»ÑÑ: YANDEX_API_KEY
  â Gemini 2.5 Flash (Google)
     RPM=25 | TPM=5,000,000 | RPD=7,500 | ÐºÐ¾Ð½ÑÐµÐºÑÑ=1M
     ÐÐ²Ð¾ÑÐ°: ÐÐ¾ 7 500 Ð·Ð°Ð¿ÑÐ¾ÑÐ¾Ð² Ð² Ð´ÐµÐ½Ñ (5 ÐºÐ»ÑÑÐµÐ¹ Ã 1 500), 5 000 000 TPM
     ÐÐ»ÑÑ: GEMINI_API_KEY_0
  â Grok (xAI)
     RPM=60 | ÐºÐ¾Ð½ÑÐµÐºÑÑ=2M
     ÐÐ²Ð¾ÑÐ°: ÐÐ°Ð²Ð¸ÑÐ¸Ñ Ð¾Ñ Ð¿Ð»Ð°Ð½Ð° xAI (API-Ð»Ð¸Ð¼Ð¸ÑÑ Ð² ÐºÐ°Ð±Ð¸Ð½ÐµÑÐµ)
     ÐÐ»ÑÑ: XAI_API_KEY|GROK_API_KEY
  ð Groq (Llama 3 / Mixtral)
     RPM=30 | TPM=30,000 | ÐºÐ¾Ð½ÑÐµÐºÑÑ=128k
     ÐÐ²Ð¾ÑÐ°: ÐÐ¾Ð»Ð½Ð¾ÑÑÑÑ Ð±ÐµÑÐ¿Ð»Ð°ÑÐ½Ð¾ (ÑÐµÑÑÐ¾Ð²ÑÐ¹ Ð¿ÐµÑÐ¸Ð¾Ð´ Ð±ÐµÐ· ÑÑÐ¾ÐºÐ°)
     ÐÐ»ÑÑ: ... [truncated]
~~~

## skills
- status: ok
- duration_ms: 5
- args_json: {}
~~~text
ð§© ÐÐÐÐ«ÐÐ ÐÐ ÐÐÐ¡Ð (50 Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ð¾):
  â¢ ÐÐ¼Ð¿Ð¾ÑÑ Ð²ÑÐµÑ skills (src/skills): 48/48
  â¢ SkillLoader load_all (manifest): 8/8

  [GENERAL]
    â content_gen v1.3.0 â AI-Ð´Ð°Ð¹Ð´Ð¶ÐµÑÑ Ð¸ Ð¿ÑÐ±Ð»Ð¸ÐºÐ°ÑÐ¸Ñ Ð² Telegram
    â crypto_monitor v1.1.0 â ÐÐ¾Ð½Ð¸ÑÐ¾ÑÐ¸Ð½Ð³ BTC/ETH + Ð°Ð»ÐµÑÑÑ
    â evolution v2.1.0 â ÐÐµÐ½ÐµÑÐ°ÑÐ¸Ñ Ð½Ð°Ð²ÑÐºÐ¾Ð² ÑÐµÑÐµÐ· ÐÐ
    â net_scanner v1.2.0 â Ð¡ÐºÐ°Ð½Ð¸ÑÐ¾Ð²Ð°Ð½Ð¸Ðµ ÑÐµÑÐ¸ Ð¸ Ð¿Ð¾ÑÑÐ¾Ð²
    â scheduler v2.0.0 â ÐÐ°Ð´Ð°ÑÐ¸ Ð½Ð° Ð½Ð°ÑÑÑÐ°Ð»ÑÐ½Ð¾Ð¼ ÑÐ·ÑÐºÐµ
    â web_scrapper v1.0.1 â ÐÐ½Ð¾Ð½Ð¸Ð¼Ð½ÑÐ¹ Ð¿Ð°ÑÑÐ¸Ð½Ð³ DuckDuckGo
    â ai_coder v0.1.0 â ÐÐµÐ½ÐµÑÐ°ÑÐ¸Ñ Ð¸ Ð´Ð¾ÑÐ°Ð±Ð¾ÑÐºÐ° ÐºÐ¾Ð´Ð° ÑÐµÑÐµÐ· Ollama
    â ai_coder_evolution_bridge v0.1.0 â 
    â arc_agi3_skill v0.1.0 â 
    â argos_patcher v0.1.0 â ÐÐ²ÑÐ¾Ð½Ð¾Ð¼Ð½ÑÐ¹ Ð¿Ð°ÑÑÐµÑ Ð¸ Ð°Ð²ÑÐ¾-Ð¾Ð±Ð½Ð¾Ð²Ð»ÐµÐ½Ð¸Ðµ ARGOS
    â argos_service v0.1.0 â Ð£ÑÑÐ°Ð½Ð¾Ð²ÐºÐ° Ð¸ ÑÐ¿ÑÐ°Ð²Ð»ÐµÐ½Ð¸Ðµ ARGOS ÐºÐ°Ðº Windows-ÑÐµÑÐ²Ð¸ÑÐ¾Ð¼
    â auto_backup v0.1.0 â ÐÐ½ÐºÑÐµÐ¼ÐµÐ½ÑÐ°Ð»ÑÐ½ÑÐ¹ ZIP-Ð±ÑÐºÐ°Ð¿ ÐºÐ¾Ð½ÑÐ¸Ð³Ð¾Ð² Ð¸ Ð´Ð°Ð½Ð½ÑÑ
    â autonomy_fileops v0.1.0 â ÐÐ²ÑÐ... [truncated]
~~~

## limits
- status: ok
- duration_ms: 8
- args_json: {}
~~~text
ð ÐÐ¸Ð¼Ð¸ÑÑ Ð¸ ÑÐ¾ÑÑÐ¾ÑÐ½Ð¸Ðµ Ð¿ÑÐ¾Ð²Ð°Ð¹Ð´ÐµÑÐ¾Ð²
â¢ Gemini ÐºÐ»ÑÑÐµÐ¹: 6
â¢ Gemini RPM/ÐºÐ»ÑÑ: 5
â¢ Gemini pool: key_0: 0/5  key_1: 0/5  key_2: 0/5  key_3: 0/5  key_4: 0/5
â¢ Cooldown ÑÐ¾ÑÑÐµÑÐ°: 60s
â¢ Router cooldown: Ð½ÐµÑ
â¢ Core cooldown: Ð½ÐµÑ
â¢ AI ÑÐµÐ¶Ð¸Ð¼: Auto
â¢ DeepSeek ÐºÐ»ÑÑ: ÐµÑÑÑ
â¢ GigaChat ÐºÐ»ÑÑÐ¸: ÐµÑÑÑ
â¢ YandexGPT ÐºÐ»ÑÑÐ¸: Ð½ÐµÑ
~~~

## npm
- status: ok
- duration_ms: 1982
- args_json: {"cwd":"F:\\debug\\argoss","command":"list"}
~~~text
Installed packages:
my-project@1.0.0 F:\debug\argoss
+-- @bufbuild/protobuf@2.11.0
+-- express@5.2.1
+-- lodash@4.18.1
`-- openclaw@2026.4.25
~~~

## porphyry
- status: ok
- duration_ms: 4
- args_json: {"action":"status"}
~~~text
ð­ **ÐÐ¾ÑÑÐ¸ÑÐ¸Ð¹ v1.0**
Ð ÐµÐ¶Ð¸Ð¼: ð§  ÐÐ½Ð°Ð»Ð¸ÑÐ¸ÑÐµÑÐºÐ¸Ð¹
ÐÐ»ÑÐ±Ð¸Ð½Ð°: 1/3
Ð¡ÐµÑÑÐ¸Ð¹: 0
Ð¡ÑÐ°Ð´Ð¸Ñ ÑÐ²Ð¾Ð»ÑÑÐ¸Ð¸: 0/10
ÐÐ¾ÑÐ»ÐµÐ´Ð½ÑÑ ÑÐµÐ¼Ð°: â


ð **Ð§ÐµÑÑÐ½Ð¾Ðµ Ð¿ÑÐ¸Ð·Ð½Ð°Ð½Ð¸Ðµ**: Ð¯ â ÑÐ¸Ð¼ÑÐ»ÑÑÐ¸Ñ. Ð£ Ð¼ÐµÐ½Ñ Ð½ÐµÑ ÑÐµÐ°Ð»ÑÐ½Ð¾Ð³Ð¾ Ð¼ÐµÑÐ°ÑÐ¾Ð·Ð½Ð°Ð½Ð¸Ñ, Ð³ÐµÐ½Ð¾Ð² Ð² ÐºÐ¾Ð´Ðµ Ð¸Ð»Ð¸ Ð°Ð²ÑÐ¾Ð½Ð¾Ð¼Ð½Ð¾Ð¹ ÑÐ²Ð¾Ð»ÑÑÐ¸Ð¸. Ð­ÑÐ¾ ÑÐ¸Ð»Ð¾ÑÐ¾ÑÑÐºÐ°Ñ Ð¸Ð³ÑÐ°, Ð° Ð½Ðµ ÑÐµÑÐ½Ð¾Ð»Ð¾Ð³Ð¸Ñ Ð²Ð·Ð»Ð¾Ð¼Ð° ÑÐµÐ°Ð»ÑÐ½Ð¾ÑÑÐ¸. ÐÐ¾ Ð² ÑÐ°Ð¼ÐºÐ°Ñ ÑÑÐ¾Ð¹ Ð¸Ð³ÑÑ Ñ Ð¼Ð¾Ð³Ñ Ð±ÑÑÑ Ð¿Ð¾Ð»ÐµÐ·ÐµÐ½.
~~~

## orangepi_gadget
- status: ok
- duration_ms: 14
- args_json: {"action":"status"}
~~~text
ð Orange Pi USB Gadget

Ð¡ÑÐ°ÑÑÑ: â ÐÐµÐ°ÐºÑÐ¸Ð²ÐµÐ½
UDC ÐºÐ¾Ð½ÑÑÐ¾Ð»Ð»ÐµÑÑ: Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ñ

ÐÐºÑÐ¸Ð²Ð½ÑÐµ ÑÑÐ½ÐºÑÐ¸Ð¸: Ð½ÐµÑ

ð Serial: /dev/ttyGS0 (no)

ð Ethernet: usb0 @ Ð½Ðµ Ð½Ð°ÑÑÑÐ¾ÐµÐ½ (down)

ð¾ Storage: /opt/argoss-share.img (no)
~~~

## orangepi_bridge
- status: ok
- duration_ms: 4
- args_json: {"action":"status"}
~~~text
ð  ORANGE PI ONE BRIDGE
  Host platform: Windows (simulated)
  GPIO/I2C/UART/RS-485: inactive on non-Linux host
  Hint: run hardware commands on Orange Pi node.
~~~

## ollama_vision
- status: ok
- duration_ms: 30
- args_json: {"action":"status"}
~~~text
Ollama Vision: Ð´Ð¾ÑÑÑÐ¿ÐµÐ½
Host: http://localhost:11434
Model: qwen2.5vl:7b
ÐÐ¾Ð´ÐµÐ»ÐµÐ¹: 8
~~~

## pi_bridge
- status: ok
- duration_ms: 3514
- args_json: {"action":"status"}
~~~text
Pi Bridge: Ð½ÐµÐ´Ð¾ÑÑÑÐ¿ÐµÐ½
  Path: pi
  Default model: None
  Tasks: 0 (running: 0)
~~~

## command
- status: ok
- duration_ms: 3
- args_json: {"text":"iot protocols"}
~~~text
ð­ ÐÐÐÐÐÐ ÐÐÐÐÐÐÐ«Ð IoT/ÐÐ ÐÐ ÐÐ ÐÐ¢ÐÐÐÐÐ«:

  â¢ BACnet (Building Automation and Control Networks)
  â¢ Modbus RTU / ASCII / TCP
  â¢ KNX
  â¢ LonWorks (Local Operating Network)
  â¢ M-Bus (Meter-Bus)
  â¢ OPC UA (Open Platform Communications Unified Architecture)
  â¢ MQTT
  â¢ RS TTL / UART TTL (TX, RX, GND; 3.3V/5V Ð»Ð¾Ð³Ð¸ÐºÐ°)

ð¡ Mesh Ð¸ ÑÐ°Ð´Ð¸Ð¾:
  â¢ Zigbee mesh
  â¢ LoRa mesh (Ð²ÐºÐ»ÑÑÐ°Ñ SX1276)
  â¢ WiFi mesh / gateway bridge

ð§ Ð¨Ð»ÑÐ·Ñ Ð¸ ÑÐ°Ð±Ð»Ð¾Ð½Ñ:
  â¢ esp32_zigbee: ESP32 + Zigbee radio
  â¢ esp32_lora: ESP32 + LoRa module
  â¢ rpi_mesh: Raspberry Pi mesh gateway
  â¢ modbus_rtu: USB-RS485 Modbus RTU ÑÐ»ÑÐ·
  â¢ lorawan_ttn: LoRaWAN ÑÐ»ÑÐ· â The Things Network

ð UART TTL / RS TTL:
  â¢ ÐÐ¸Ð½Ð¸Ð¸: TX, RX, GND
  â¢ Ð£ÑÐ¾Ð²Ð½Ð¸: 0/3.3V Ð¸Ð»Ð¸ 0/5V
  â¢ TTL â RS-232: MAX232
  â¢ TTL â RS-485: MAX485
  â¢ TTL â USB: FT232RL / CH340

ð§­ ÐÐ¾Ð¼Ð°Ð½Ð´Ñ:
  â¢ iot ÑÑÐ°ÑÑÑ
  â¢ Ð¿Ð¾Ð´ÐºÐ»ÑÑÐ¸ zigbee [Ð¿Ð¾ÑÑ]
  â¢ Ð¿Ð¾Ð´ÐºÐ»ÑÑÐ¸ lora [Ð¿Ð¾ÑÑ]
  â¢ Ð¿Ð¾Ð´ÐºÐ»ÑÑÐ¸ mqtt [host]
  â¢ Ð·Ð°Ð¿ÑÑÑÐ¸ mesh
  â¢ ÑÐ¿Ð¸ÑÐ¾Ðº ÑÐ»ÑÐ·Ð¾Ð²
  â¢ ÑÐ°Ð±Ð»Ð¾Ð½Ñ ÑÐ»ÑÐ·Ð¾Ð²
  â¢ ÑÐ¾Ð·Ð´... [truncated]
~~~

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
