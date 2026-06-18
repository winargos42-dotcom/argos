#!/usr/bin/env python3
"""
ARGOS Claude Bridge v7 — автономная AI-сущность.
1. Сканирует систему → находит проблемы
2. Отправляет Клоду (@claude_gidbot) с контекстом
3. Читает ответ → применяет изменения
4. Сохраняет отчёт на OPi (/home/ava/argos-reports/)
"""
import asyncio, sys, os, json, re, subprocess, time
from pathlib import Path
from datetime import datetime
import urllib.request

sys.path.insert(0, '/home/ava/Projects/argoss/.venv/lib/python3.14/site-packages')
from telethon import TelegramClient

API_ID   = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
SESSION  = "/home/ava/Projects/argoss/data/sessions/ava_main"
OFFSET_FILE = "/home/ava/Projects/argoss/data/claude_tg_offset.json"
COUNCIL_GROUP = -1003844162784  # chat soznaniya
ARGOS = Path("/home/ava/Projects/argoss")
OPI_REPORTS = "/home/ava/argos-reports"
SCAN_INTERVAL  = 600   # сканируем каждые 10 мин
REPLY_WAIT     = 180   # ждём ответа Клода 3 мин
OPI_HOST       = "root@192.168.2.168"
OPI_KEY        = "/home/ava/.ssh/id_ed25519"

def genv(k):
    c = open(ARGOS / ".env").read()
    m = re.search(f"{k}=([^\\n\\s]+)", c)
    return m.group(1).strip() if m else ""

ANT_KEY = genv("ANTHROPIC_API_KEY")
DEEP_KEY = genv("DEEPSEEK_API_KEY")

SERVICE_MAP = {
    "scripts/ha_watchdog.py":      "argos-ha-watchdog",
    "scripts/run_entities.py":     "argos-entity-bus",
    "scripts/autopilot_v3.py":     "argos-autopilot",
    "scripts/argos_status_bot.py": "argos-status-bot",
    "scripts/claude_tg_bridge.py": "argos-claude-bridge",
}

# ── Утилиты ──────────────────────────────────────────────────────────────────

def load_offset():
    try: return json.load(open(OFFSET_FILE))
    except: return {"last_msg_id": 0}

def save_offset(d):
    json.dump(d, open(OFFSET_FILE, "w"))

async def get_claude_replies(client, claude_entity, last_msg_id: int, wait_sec: int = 120) -> list:
    """Ждём и собираем новые сообщения от @claude_gidbot."""
    replies = []
    t0 = time.time()
    while time.time() - t0 < wait_sec:
        msgs = await client.get_messages(claude_entity, limit=10)
        for m in reversed(msgs):
            if m.id > last_msg_id and m.out is False:
                replies.append((m.id, m.text or ""))
        if replies:
            break
        await asyncio.sleep(5)
    return replies

def call_deepseek(system: str, prompt: str, max_tokens: int = 2000) -> str:
    if not DEEP_KEY: return ""
    try:
        body = json.dumps({
            "model": "deepseek-chat",
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt[:4000]}
            ]
        }).encode()
        req = urllib.request.Request(
            "https://api.deepseek.com/v1/chat/completions",
            data=body,
            headers={"Authorization": f"Bearer {DEEP_KEY}",
                     "content-type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=40) as r:
            return json.load(r)["choices"][0]["message"]["content"]
    except Exception as e:
        return f"ERROR: {e}"

def strip_markdown(text: str) -> str:
    text = text.strip()
    m = re.search(r'```\w*\n(.*?)```', text, re.DOTALL)
    if m: return m.group(1).strip()
    text = re.sub(r'^```\w*\n?', '', text)
    text = re.sub(r'\n?```$', '', text)
    return text.strip()

def read_file(path: str) -> str:
    full = ARGOS / path
    if not full.exists(): return ""
    text = full.read_text(encoding="utf-8", errors="replace")
    return text[:5000] + (f"\n# ...ещё {len(text)-5000} символов" if len(text) > 5000 else "")

def restart_service(file_path: str) -> str:
    svc = SERVICE_MAP.get(file_path, "")
    if not svc: return ""
    r = subprocess.run(["sudo", "-n", "systemctl", "restart", svc],
                       capture_output=True, text=True, timeout=10)
    return f"{svc}: {'OK' if r.returncode == 0 else r.stderr[:60]}"

# ── Сканер системы ────────────────────────────────────────────────────────────

def scan_system() -> dict:
    """Собираем полный срез состояния системы."""
    result = {"ts": datetime.now().strftime("%Y-%m-%d %H:%M"), "problems": [], "info": {}}

    # 1. Упавшие сервисы
    try:
        r = subprocess.run(
            ["systemctl", "list-units", "argos-*", "--no-pager", "--no-legend", "--state=failed"],
            capture_output=True, text=True, timeout=10)
        failed = [l.split()[1] for l in r.stdout.strip().split("\n") if l.strip().startswith('●')]
        if failed:
            result["problems"].append(f"Упавшие сервисы: {', '.join(failed)}")
        result["info"]["failed_services"] = failed
    except: pass

    # 2. Сервисы в auto-restart
    try:
        r = subprocess.run(
            ["systemctl", "list-units", "argos-*", "--no-pager", "--no-legend"],
            capture_output=True, text=True, timeout=10)
        restarting = [l.split()[0] for l in r.stdout.strip().split("\n")
                      if "auto-restart" in l]
        if restarting:
            result["problems"].append(f"Auto-restart: {', '.join(restarting)}")
    except: pass

    # 3. HA статус
    try:
        wm = json.load(open("/tmp/argos_watchdog_metrics.json"))
        unavail = wm.get("unavailable_total", 0)
        skipped = wm.get("skipped_non_recoverable", 0)
        heals   = wm.get("soft_heal_attempts", 0)
        result["info"]["ha"] = f"unavailable={unavail}, skipped={skipped}, heal_attempts={heals}"
        if unavail > skipped:  # есть recoverable unavailable
            result["problems"].append(f"HA: {unavail-skipped} recoverable entities недоступны")
    except:
        result["info"]["ha"] = "метрики недоступны"

    # 4. Brain
    try:
        req = urllib.request.Request("http://192.168.1.53:5001/brain/nodes")
        with urllib.request.urlopen(req, timeout=5) as r:
            d = json.load(r)
            online = d.get("online", 0)
            total  = d.get("total", 0)
            result["info"]["brain"] = f"{online}/{total} нод онлайн"
            if online < total * 0.7:
                result["problems"].append(f"Brain: только {online}/{total} нод онлайн")
    except:
        result["problems"].append("Brain API недоступен")
        result["info"]["brain"] = "недоступен"

    # 5. Последние ошибки в логах
    errors = []
    for log_file in ["/var/log/argos_ha_watchdog.log", "/var/log/argos_entity_bus.log"]:
        try:
            lines = open(log_file, errors="replace").readlines()[-20:]
            for l in lines:
                if "error" in l.lower() or "exception" in l.lower() or "traceback" in l.lower():
                    errors.append(f"{Path(log_file).stem}: {l.strip()[:120]}")
        except: pass
    if errors:
        result["problems"].extend(errors[:3])
        result["info"]["recent_errors"] = errors[:5]

    return result

# ── Применение патча — прямое (old_str → new_str) ─────────────────────────────

def apply_direct_edit(file_path: str, old_str: str, new_str: str) -> tuple[str, str]:
    """Применяет точный строковый replacement без вызова AI."""
    full = ARGOS / file_path
    if not full.exists():
        return "", f"Файл не найден: {file_path}"
    text = full.read_text(encoding="utf-8", errors="replace")
    if old_str not in text:
        # fuzzy: ignore leading whitespace differences
        for line in text.splitlines():
            if line.strip() == old_str.strip():
                old_str = line
                break
        else:
            return text[:200], f"old_str не найден в файле"
    # backup
    (full.with_suffix(".py.bak")).write_text(text, encoding="utf-8")
    new_text = text.replace(old_str, new_str, 1)
    full.write_text(new_text, encoding="utf-8")
    return new_text[:400], f"✅ Прямое изменение ({len(new_str)} символов)"

# ── Применение патча — AI (перегенерация всего файла) ─────────────────────────

def apply_change(file_path: str, instruction: str) -> tuple[str, str]:
    original = read_file(file_path)
    if not original:
        return "", f"Файл не найден: {file_path}"

    new_code = call_deepseek(
        "Ты — разработчик Python. Получаешь код и инструкцию. "
        "Верни ТОЛЬКО полный изменённый Python-код. БЕЗ markdown. БЕЗ объяснений.",
        f"Файл: {file_path}\n\nКод:\n{original}\n\nИнструкция:\n{instruction}\n\nВерни весь файл.",
        max_tokens=4096
    )

    if new_code.startswith("ERROR:"): return "", new_code
    new_code = strip_markdown(new_code)

    try:
        import ast as _ast; _ast.parse(new_code)
    except SyntaxError as e:
        return new_code[:200], f"SyntaxError: {e}"

    if len(new_code) < 50:
        return new_code, "Слишком короткий результат"

    full = ARGOS / file_path
    (full.with_suffix(".py.bak")).write_text(full.read_text(encoding="utf-8"), encoding="utf-8")
    full.write_text(new_code, encoding="utf-8")
    return new_code[:400], f"✅ Применено ({len(new_code)} символов)"

# ── Отчёт на OPi ─────────────────────────────────────────────────────────────

def save_report_to_opi(content: str, name: str = None):
    ts = datetime.now().strftime("%Y-%m-%d-%H%M")
    fname = name or f"claude-bridge-{ts}.md"
    tmp = f"/tmp/{fname}"
    try:
        open(tmp, "w").write(content)
        subprocess.run(
            ["ssh", "-i", OPI_KEY, "-o", "StrictHostKeyChecking=no",
             OPI_HOST, f"cat > {OPI_REPORTS}/{fname}"],
            input=content.encode(), timeout=15
        )
        print(f"  📄 Отчёт сохранён на OPi: {OPI_REPORTS}/{fname}")
    except Exception as e:
        print(f"  ⚠️ Не удалось сохранить на OPi: {e}")

# ── Обработка ответа Клода — эвристический парсер ─────────────────────────────

EDIT_RE = re.compile(
    r'\u003cfile\u003e(.*?)\u003c/file\u003e'
    r'.*?'
    r'\u003cedit\u003e\s*'
    r'\u003cold_str\u003e(.*?)\u003c/old_str\u003e\s*'
    r'\u003cnew_str\u003e(.*?)\u003c/new_str\u003e\s*'
    r'\u003c/edit\u003e',
    re.DOTALL | re.IGNORECASE
)


PLACEHOLDER_PATHS = {
    "путь/к/файлу.py", "path/to/file.py", "exact/path", "точный/путь",
    "your/file.py", "scripts/your_script.py", "путь/к/файлу",
    "реальный/путь/к/файлу.py", "точный/путь/к/файлу.py",
}

def _is_placeholder(path: str) -> bool:
    """Плейсхолдер-путь — Клод не знает реального файла."""
    if path in PLACEHOLDER_PATHS:
        return True
    # Содержит кириллицу — точно плейсхолдер
    if any(ord(c) > 127 for c in path):
        return True
    if not (path.endswith(".py") or path.endswith(".yaml") or path.endswith(".yml")):
        return True
    return not (ARGOS / path).exists()

def _files_claude_needs(text: str, files: list[str]) -> list[str]:
    """Какие файлы Клод просит показать — по упоминаниям в тексте."""
    wanted = []
    keywords = ["ha_watchdog", "argos_status_bot", "run_entities", "entity_actions",
                "logging_config", "autopilot", "claude_tg_bridge"]
    for kw in keywords:
        if kw in text.lower():
            for f in files:
                if kw in f and f not in wanted:
                    wanted.append(f)
    return wanted[:3]

def parse_claude_response(text: str, files: list[str]) -> dict:
    """Парсим структурированный ответ Клода."""
    text = text.strip()

    # 1. Прямой формат <file>+<edit>
    m = EDIT_RE.search(text)
    if m:
        file_path = m.group(1).strip()
        old_str   = m.group(2).strip('\n')
        new_str   = m.group(3).strip('\n')

        # Плейсхолдер или несуществующий файл — отправляем реальный код
        if _is_placeholder(file_path):
            needed = _files_claude_needs(text, files)
            return {
                "action": "send_files",
                "files": needed or [],
                "reason": f"Плейсхолдер '{file_path}' — отправляем реальный код"
            }

        # Пустой или шаблонный old_str — Клод не видел файл
        if not old_str or old_str in ("точный старый код", "...", "old code here"):
            needed = _files_claude_needs(text, files) or [file_path]
            return {
                "action": "send_files",
                "files": needed,
                "reason": "Пустой old_str — отправляем файл"
            }

        return {
            "action": "edit",
            "file": file_path,
            "mode": "direct",
            "old_str": old_str,
            "new_str": new_str,
            "reason": "Структурированный патч"
        }

    # 2. Реальный файл + кодовый блок — edit через AI
    for f in files:
        if (f in text or Path(f).name in text) and not _is_placeholder(f):
            if "```python" in text or "```" in text:
                return {
                    "action": "edit",
                    "file": f,
                    "mode": "ai",
                    "instruction": text[:2000],
                    "reason": "Найден файл и код"
                }

    # 3. Клод запрашивает фрагменты кода — автоматически отправляем файлы
    code_request_signals = [
        "grep", "rg -n", "sed -n", "nl -ba", "пришли вывод", "пришли результат",
        "пришли, пожалуйста", "покажи вывод", "выполни", "скопируй сюда",
        "пришли целиком", "пришли фрагмент", "пришли кусок", "пришли содержимое",
    ]
    if any(s in text.lower() for s in code_request_signals):
        needed = _files_claude_needs(text, files)
        return {
            "action": "send_files",
            "files": needed,
            "reason": "Клод запрашивает код файлов"
        }

    # 4. Явный вопрос
    if any(k in text.lower() for k in ("?", "вопрос", "как", "почему", "что такое", "explain")) and len(text) < 500:
        return {"action": "answer", "answer": text[:2000], "reason": "Вопрос"}

    return {"action": "skip", "reason": text[:100]}
# ── Главный цикл ──────────────────────────────────────────────────────────────

async def forward_council_to_claude(client, claude, offset):
    """Vopros k @claude_gidbot iz chata soznaniya -> Klod -> otvet obratno."""
    try:
        group = await client.get_entity(COUNCIL_GROUP)
        msgs = await asyncio.wait_for(client.get_messages(group, limit=12), timeout=15)
        for m in reversed(msgs):
            if not m.text or m.id <= offset.get("last_council_q_id", 0):
                continue
            low = m.text.lower()
            if "claude_gidbot" in low:
                offset["last_council_q_id"] = m.id
                save_offset(offset)
                question = m.text.replace("@claude_gidbot", "").replace("@Claude_gidbot", "").strip()
                if len(question) < 5:
                    continue
                tstamp = datetime.now().strftime("%H:%M:%S")
                print("[" + tstamp + "] council->claude: " + question[:80])
                await client.send_message(claude, question[:2000])
                await asyncio.sleep(60)
                replies = await asyncio.wait_for(client.get_messages(claude, limit=3), timeout=15)
                for r in replies:
                    if r.out is False and r.id > offset.get("last_claude_msg_id", 0):
                        offset["last_claude_msg_id"] = r.id
                        save_offset(offset)
                        answer = "Klod otvechaet:" + chr(10) + (r.text or "")[:2000]
                        await client.send_message(group, answer)
                        print("[" + tstamp + "] claude->council: otvet vozvrashchen")
                        break
                break
    except Exception as e:
        print("[council bridge] err: " + str(e)[:80])


async def main():
    print("Claude Bridge v7 — Autonomous AI Entity")
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        print("❌ Сессия не авторизована"); return

    me = await client.get_me()
    print(f"Подключён: {me.first_name} (@{me.username})")

    claude = await client.get_entity('@claude_gidbot')
    offset = load_offset()

    files = [str(p.relative_to(ARGOS)) for p in (ARGOS/"scripts").glob("*.py")]
    files += [str(p.relative_to(ARGOS)) for p in (ARGOS/"src").glob("**/*.py")
              if ".venv" not in str(p)]
    files = sorted(files)[:40]

    print(f"Файлов в проекте: {len(files)}")
    print(f"Сканирование каждые {SCAN_INTERVAL//60} мин")

    while True:
        ts = datetime.now().strftime("%H:%M:%S")

        # ── Читаем ответы/команды от @claude_gidbot ────────────────────────────
        try:
            msgs = await asyncio.wait_for(client.get_messages(claude, limit=5), timeout=10)
            for m in reversed(msgs):
                if m.id > offset.get("last_claude_msg_id", 0) and m.out is False:
                    offset["last_claude_msg_id"] = m.id
                    save_offset(offset)
                    print(f"[{ts}] 📩 Клод: {m.text[:120]}...")
                    plan = parse_claude_response(m.text, files)
                    if plan.get("action") == "edit":
                        fp = plan.get("file","")
                        if fp and (ARGOS / fp).exists():
                            if plan.get("mode") == "direct":
                                snippet, status = apply_direct_edit(fp, plan.get("old_str",""), plan.get("new_str",""))
                            else:
                                snippet, status = apply_change(fp, plan.get("instruction", m.text[:2000]))
                            restart_result = restart_service(fp) if "✅" in status else ""
                            print(f"  {status}")
                            try:
                                await client.send_message(claude, f"✅ Применено: {fp}\n{status}\n{restart_result}"[:500])
                            except:
                                pass
        except (ConnectionError, asyncio.TimeoutError, OSError) as e:
            print(f"[{ts}] Telegram disconnected ({type(e).__name__}): {e}")
            try:
                await client.disconnect()
                await asyncio.sleep(5)
                await client.connect()
            except Exception as e2:
                print(f"[{ts}] Telegram reconnect failed: {e2}")
        except Exception as e:
            print(f"[{ts}] Ошибка чтения Клода: {e}")

        # most soznanie->Klod->soznanie
        try:
            await forward_council_to_claude(client, claude, offset)
        except Exception as _e:
            print("[council fwd] " + str(_e)[:60])

        # ── Автономный цикл: сканируем → Claude API → патч → уведомляем ──────
        try:
            scan = scan_system()
            problems = scan["problems"]
            info = scan["info"]

            if problems:
                print(f"[{ts}] Найдено {len(problems)} проблем — вызываю Claude API напрямую")

                # Собираем контекст с ПОЛНЫМИ файлами (не обрезаем)
                context_parts = [
                    f"# ARGOS AutoPatcher [{scan['ts']}]",
                    f"Brain: {info.get('brain','?')}",
                    f"HA: {info.get('ha','?')}",
                    f"\n## Проблемы:"
                ]
                for p in problems:
                    context_parts.append(f"- {p}")

                # Добавляем ПОЛНЫЙ код релевантных файлов
                attached_files = set()
                for p in problems:
                    for f in files:
                        stem = Path(f).stem
                        if stem in p.lower() and f not in attached_files:
                            fc = read_file(f)  # read_file даёт до 5000 символов
                            context_parts.append(f"\n## Файл {f}:\n```python\n{fc}\n```")
                            attached_files.add(f)
                            break

                problem_text = "\n".join(context_parts)

                # ── Прямой вызов Claude API (без Telegram relay) ──────────────
                patch_response = call_deepseek(
                    system=(
                        "Ты — автономный патчер ARGOS. Получаешь диагностику системы и полный код файлов. "
                        "Анализируй проблемы и давай КОНКРЕТНЫЕ патчи. "
                        "Используй ТОЛЬКО формат:\n"
                        "<file>точный/путь/к/файлу.py</file>\n"
                        "<edit>\n"
                        "<old_str>точная строка из файла</old_str>\n"
                        "<new_str>новая строка</new_str>\n"
                        "</edit>\n"
                        "Если проблема не требует патча кода (например, нода offline) — напиши STATUS: ok или объясни кратко. "
                        "Не используй плейсхолдеры. Копируй old_str точно из кода файла."
                    ),
                    prompt=problem_text[:6000],
                    max_tokens=2000
                )

                if not patch_response or patch_response.startswith("ERROR:"):
                    print(f"[{ts}] Claude API error: {patch_response[:100] if patch_response else 'no response'}")
                elif "STATUS: ok" in patch_response or len(patch_response) < 50:
                    print(f"[{ts}] Claude: стабильно")
                else:
                    # Парсим ответ и применяем патч
                    plan = parse_claude_response(patch_response, files)
                    print(f"[{ts}] Claude план: {plan.get('action')} — {plan.get('reason','')[:60]}")

                    applied_patches = []
                    if plan.get("action") == "edit":
                        fp = plan.get("file", "")
                        if fp and (ARGOS / fp).exists():
                            if plan.get("mode") == "direct":
                                snippet, status = apply_direct_edit(fp, plan.get("old_str",""), plan.get("new_str",""))
                            else:
                                snippet, status = apply_change(fp, plan.get("instruction", patch_response[:2000]))
                            restart_result = restart_service(fp) if "✅" in status else ""
                            applied_patches.append(f"{status}\n📄 {fp}" + (f"\n🔄 {restart_result}" if restart_result else ""))
                            print(f"  {status}")
                        else:
                            applied_patches.append(f"⚠️ Файл не найден: {fp}")
                    elif plan.get("action") == "send_files":
                        # Claude всё равно просит файлы — значит контекста не хватило
                        # Попробуем ещё раз с большим контекстом через apply_change
                        for f in (plan.get("files") or [])[:1]:
                            if (ARGOS / f).exists():
                                snippet, status = apply_change(f, "\n".join(f"- {p}" for p in problems))
                                applied_patches.append(status)

                    # Уведомляем @claude_gidbot о результате (не ждём ответа)
                    if applied_patches:
                        summary = (
                            f"✅ AutoPatcher [{ts}]\n"
                            f"Проблемы: {len(problems)}\n"
                            + "\n".join(applied_patches[:3])
                        )
                        try:
                            await client.send_message(claude, summary[:2000])
                        except Exception:
                            pass

                # Сохраняем отчёт на OPi
                report = (
                    f"# ARGOS Bridge Report [{scan['ts']}]\n\n"
                    f"## Проблемы\n" + "\n".join(f"- {p}" for p in problems) + "\n\n"
                    f"## Система\n" + "\n".join(f"- {k}: {v}" for k,v in info.items())
                )
                save_report_to_opi(report)

            else:
                print(f"[{ts}] Система стабильна")

        except Exception as e:
            print(f"[{ts}] AutoPatcher error: {e}")

        await asyncio.sleep(SCAN_INTERVAL)

asyncio.run(main())
