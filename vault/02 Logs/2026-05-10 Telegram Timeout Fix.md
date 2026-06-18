# ARGOS Telegram Timeout Fix — 2026-05-10

## Problem
Telegram бот таймаутил на 50%+ запросов. Причина: `ai_router.py` перебирал провайдеры в порядке Gemini → Groq → DeepSeek..., но Gemini (5 просроченных ключей) и Groq (невалидный ключ) висели по 30-60 секунд каждый перед фейловером. Telegram отваливался раньше, чем доходила очередь до рабочего DeepSeek.

## Root Cause
1. **Provider order** в `ai_router.py:156` — мёртвые провайдеры шли первыми
2. **Timeout 30s** на каждый мёртвый провайдер
3. **`.env` дубликаты** — `ARGOS_AI_MODE=openai` ×3 + `ARGOS_AI_MODE=auto`, первый выигрывал (openai)
4. **Fake DeepSeek key** — `DEEPSEEK_API_KEY=your_key_here` на строке 68 перекрывала реальный ключ на строке 270

## Changes Made

### 1. ai_router.py
- **Provider order** (строка 156): `deepseek` перемещён на первое место
  ```python
  PROVIDERS = ["deepseek", "xai", "watsonx", "gigachat", "yandexgpt", "groq", "gemini", "ollama"]
  ```
- **Timeout reduced** 30s → 10s для Groq, DeepSeek, xAI (строки 277, 301, 391)
  - Даже если 2 мёртвых провайдера подряд — макс. 20s, укладываемся в терпение Telegram

### 2. .env
- Закомментирован фейковый `DEEPSEEK_API_KEY=your_key_here` (строка 68)
- Закомментированы 3 дубликата `ARGOS_AI_MODE=openai` (строки 53, 211, 327)
- Оставлен только `ARGOS_AI_MODE=auto` (строка 337) — последний, он теперь активен

## Expected Result
- Telegram отвечает сразу через DeepSeek (единственный рабочий облачный провайдер)
- Fallback на другие провайдеры при ошибке DeepSeek — быстрый (10s таймаут)
- `ARGOS_AI_MODE=auto` позволяет core выбирать провайдер адаптивно

## Status
✅ Готово к тестированию. Нужен рестарт ARGOS для применения .env изменений.
