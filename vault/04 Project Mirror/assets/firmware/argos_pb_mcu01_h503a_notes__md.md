---
argos_import: project_file
source_path: assets/firmware/argos_pb_mcu01_h503a_notes.md
source_abs: F:\debug\argoss\assets\firmware\argos_pb_mcu01_h503a_notes.md
source_ext: .md
source_sha256: 811068e81679f2c745adfe420f26e6103bee12a053a338344423784c50746af2
text_sha256: 811068e81679f2c745adfe420f26e6103bee12a053a338344423784c50746af2
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:16
---

# argos_pb_mcu01_h503a_notes.md

- Source: `assets/firmware/argos_pb_mcu01_h503a_notes.md`
- Extract: `text`
- SHA256: `811068e81679f2c745adfe420f26e6103bee12a053a338344423784c50746af2`

## Content

# PB_MCU01_H503A — ARGOS Integration Notes

## Board: PB_MCU01_H503A (pb-embedded.ru)
**MCU:** STM32H503CBT6 — ARM Cortex-M33 @ 250 MHz
**Flash:** 128 KB | **RAM:** 32 KB | **Package:** LQFP48
**USB:** Full-Speed (VID:0483 PID:5740 CDC / VID:0483 PID:DF11 DFU)

## Quick Start

### 1. Flash via ST-Link v2
```
st-flash write argos_h503a.bin 0x08000000
```
or
```
STM32_Programmer_CLI -c port=SWD -w argos_h503a.bin 0x08000000 -v -rst
```

### 2. Flash via USB DFU (no ST-Link needed)
1. Hold BOOT0 pin while plugging USB
2. Device appears as `STM32 BOOTLOADER` (VID:0483 PID:DF11)
3. `dfu-util -a 0 -D argos_h503a.bin --dfuse-address 0x08000000`

### 3. ARGOS commands
```
прошей stm32h503          — прошить через ST-Link
stm32 статус              — статус интеграции
подключи stm32            — запустить USB мост
stlink статус             — проверить инструменты
```

## Pin Assignments
| Function   | Pin  | Notes                     |
|------------|------|---------------------------|
| LED_GREEN  | PA5  | Active HIGH               |
| BTN_USER   | PC13 | Active LOW, internal PU   |
| USB_DP     | PA12 | Full-Speed USB+           |
| USB_DM     | PA11 | Full-Speed USB-           |
| SWCLK      | PA14 | ST-Link SWD clock         |
| SWDIO      | PA13 | ST-Link SWD data          |
| UART2_TX   | PA2  | Debug UART 115200         |
| UART2_RX   | PA3  | Debug UART                |
| ADC1_VTEMP | CH17 | Internal temp sensor      |

## JSON Protocol (same as ESP32 and RP2350-GEEK)
```json
// Board → PC (hello on startup)
{"type":"hello","device":"ARGOS-H503A","fw":"1.0.0","chip":"STM32H503CBT6","temp":37.2}

// PC → Board (status update, every 2 sec)
{"type":"status","cpu":7.2,"ram":42.1,"disk":"120GB","os":"Windows"}

// Board → PC (user button pressed)
{"type":"user_cmd","cmd":"статус системы"}

// Ping/Pong
{"type":"ping"}  →  {"type":"pong"}

// Commands from PC to board
{"type":"cmd","cmd":"reboot"}
{"type":"cmd","cmd":"led_blink"}
{"type":"cmd","cmd":"temp"}
```

## Building with STM32CubeIDE
1. File → New → STM32 Project → STM32H503CBT6
2. Enable: USB (Device FS), ADC1 (IN17/VTEMP), TIM2
3. Set SYSCLK = 250 MHz via PLL
4. Copy `argos_pb_mcu01_h503a.c` to Core/Src/
5. In `main.c` at end: `extern void ARGOS_Main(void); ARGOS_Main();`
6. In `usbd_cdc_if.c` in `CDC_Receive_FS()`:
   ```c
   extern void ARGOS_CDC_Receive(uint8_t *data, uint32_t len);
   ARGOS_CDC_Receive(Buf, Len);
   ```

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
