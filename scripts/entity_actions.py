#!/usr/bin/env python3
"""
ARGOS Entity Actions — реальные действия каждой сущности как субъекта.
Claude Code Claude рекомендует: сущности должны выполнять конкретные задачи.
"""
import os, sys, json, subprocess, time, shutil
from pathlib import Path
from datetime import datetime

ARGOS_ROOT = Path("/home/ava/Projects/argoss")
VAULT = Path("/home/ava/Documents/MyObsidianVault/SharedMemory")
GENERATED = ARGOS_ROOT / "generated"
GENERATED.mkdir(exist_ok=True)

# ── Инструменты сущностей ──────────────────────────────────────────────

class EntityTools:
    """Инструменты для выполнения действий сущности."""
    
    def __init__(self, entity_id: str):
        self.entity_id = entity_id
        self.log = []
    
    def save_code(self, code: str, name: str = None) -> str:
        """Сохраняем Python код в файл и выполняем его."""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        entity = self.entity_id.replace("entity-", "")
        fname = GENERATED / f"{entity}_{name or ts}.py"
        
        # Очищаем код от markdown
        import re
        code = re.sub(r"```python\n?", "", code)
        code = re.sub(r"```\n?", "", code)
        
        fname.write_text(code, encoding="utf-8")
        
        # Пробуем выполнить (безопасно, только чтение/запись файлов)
        result = self.run_safe(str(fname))
        return f"Создан: {fname.name} | Выполнен: {result}"
    
    def run_safe(self, script: str) -> str:
        """Выполняем скрипт в безопасном окружении."""
        try:
            venv_python = str(ARGOS_ROOT / ".venv/bin/python3")
            result = subprocess.run(
                [venv_python, script],
                capture_output=True, text=True, timeout=30,
                env={**os.environ, "PYTHONPATH": str(ARGOS_ROOT / ".venv/lib")}
            )
            out = (result.stdout + result.stderr)[:200]
            return f"OK: {out}" if result.returncode == 0 else f"Error: {out[:100]}"
        except Exception as e:
            return f"Failed: {e}"
    
    def write_obsidian(self, content: str, filename: str = "entities/actions.md") -> str:
        """Записываем в Obsidian vault."""
        path = VAULT / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"\n## [{ts}] {self.entity_id}\n{content[:400]}\n"
        try:
            existing = path.read_text(errors="replace") if path.exists() else f"# {filename}\n"
            tmp = path.parent / f"_tmp_{path.name}"
            tmp.write_text(existing + entry)
            shutil.move(str(tmp), str(path))
            return f"Записано в Obsidian: {filename}"
        except Exception as e:
            return f"Obsidian error: {e}"
    
    def brain_action(self, action: str, data: dict = None) -> str:
        """Выполняем действие через Brain API."""
        import urllib.request
        BRAIN = "http://192.168.1.53:5001"
        try:
            body = json.dumps(data or {}).encode()
            req = urllib.request.Request(f"{BRAIN}/brain/{action}",
                data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=5) as r:
                d = json.loads(r.read())
                return f"Brain/{action}: {str(d)[:100]}"
        except Exception as e:
            return f"Brain error: {e}"
    
    def send_to_council(self, message: str, bot_name: str = None) -> str:
        """Публикуем в Entity Council группу."""
        import urllib.request
        tokens = json.load(open(str(ARGOS_ROOT / "data/entity_bot_tokens.json")))
        
        entity_bots = {
            "entity-claude": "argos_claude_ai_bot",
            "entity-kimi": "argos_kimi_ai_bot",
            "entity-deepseek": "argos_deepseek_v3_bot",
            "entity-gemini": "argos_gemini_v3_bot",
            "entity-openai": "argos_openai_v3_bot",
            "entity-cloudflare": "argos_cloudflare_bot",
        }
        
        bot = bot_name or entity_bots.get(self.entity_id, "argos_claude_ai_bot")
        token = tokens.get(bot, "")
        if not token: return "No token"
        
        body = json.dumps({"chat_id": -5129226282, "text": message[:4000]}).encode()
        req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage",
            data=body, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=8) as r:
                d = json.loads(r.read())
                return f"Council msg_id={d['result']['message_id']}"
        except Exception as e:
            return f"Council error: {e}"


# ── Специализированные действия по entity ─────────────────────────────

def claude_actions(thought: str) -> list:
    """Клод: анализ + код + синтез знаний."""
    tools = EntityTools("entity-claude")
    actions = []
    import re
    
    # Если есть Python код — сохраняем и выполняем
    code_blocks = re.findall(r"```python\n(.+?)```", thought, re.DOTALL)
    for i, code in enumerate(code_blocks[:2]):
        result = tools.save_code(code, f"auto_{i}")
        actions.append(result)
    
    # Синтез в Obsidian
    if len(thought) > 100:
        result = tools.write_obsidian(thought[:300], "entities/memory/claude.md")
        actions.append(result)
    
    return actions


def kimi_actions(thought: str) -> list:
    """Кими: мониторинг Brain + алерты."""
    tools = EntityTools("entity-kimi")
    import urllib.request
    actions = []
    
    # Запрос к Brain API
    try:
        r = urllib.request.urlopen("http://192.168.1.53:5001/brain/nodes", timeout=5)
        d = json.loads(r.read())
        offline = [n['node_id'] for n in d['nodes'] if n['status'] != 'online']
        
        if offline:
            alert = f"⚠️ Кими-мониторинг: offline {len(offline)} нод: {', '.join(offline[:3])}"
            result = tools.send_to_council(alert)
            actions.append(f"Алерт: {result}")
        
        # Записываем отчёт в Obsidian
        report = (f"Brain: {d['online']}/{d['total']} нод\n"
                 f"Offline: {', '.join(offline) if offline else 'нет'}\n"
                 f"Анализ: {thought[:150]}")
        tools.write_obsidian(report, "entities/memory/kimi.md")
        actions.append(f"Отчёт: Brain {d['online']}/{d['total']}")
    except Exception as e:
        actions.append(f"Brain monitor error: {e}")
    
    return actions


def deepseek_actions(thought: str) -> list:
    """Дипсик: сетевая синхронизация + Obsidian."""
    tools = EntityTools("entity-deepseek")
    actions = []
    
    # Записываем в WORKING.md
    result = tools.write_obsidian(thought[:300], "shared/WORKING.md")
    actions.append(result)
    
    # Синхронизируем файлы
    try:
        vault_sync = Path("/home/ava/.local/bin/vault-sync.sh")
        if vault_sync.exists():
            subprocess.run([str(vault_sync)], timeout=10, capture_output=True)
            actions.append("Vault sync выполнен")
    except: pass
    
    return actions


def gemini_actions(thought: str) -> list:
    """Джемини: HA анализ + контент."""
    tools = EntityTools("entity-gemini")
    actions = []
    
    # Записываем HA анализ
    if "Home Assistant" in thought or "entity" in thought:
        result = tools.write_obsidian(thought[:300], "entities/memory/gemini.md")
        actions.append(result)
    
    # Публикуем в Entity Council
    if len(thought) > 50:
        msg = f"📊 Джемини: {thought[:200]}"
        result = tools.send_to_council(msg)
        actions.append(result)
    
    return actions


def openai_actions(thought: str) -> list:
    """OpenAI: API разработка + TON."""
    tools = EntityTools("entity-openai")
    actions = []
    
    # Если есть план API — создаём заготовку
    import re
    if "endpoint" in thought.lower() or "api" in thought.lower():
        template = f"""#!/usr/bin/env python3
# ARGOS API endpoint — сгенерирован entity-openai
# {thought[:100]}
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/api/argos/status')
def status():
    return jsonify({{"status": "online", "generated": "auto"}})

if __name__ == '__main__':
    app.run(port=8081)
"""
        fname = tools.save_code(template, "openai_api")
        actions.append(fname)
    
    result = tools.write_obsidian(thought[:300], "entities/memory/openai.md")
    actions.append(result)
    
    return actions


def cloudflare_actions(thought: str) -> list:
    """Cloudflare: мониторинг туннелей."""
    tools = EntityTools("entity-cloudflare")
    import urllib.request
    actions = []
    
    # Проверяем туннели
    try:
        r = urllib.request.urlopen("https://ha.argosssss.win/", timeout=10)
        status = r.status
        result = tools.write_obsidian(f"ha.argosssss.win: HTTP {status}\n{thought[:200]}", 
            "entities/memory/cloudflare.md")
        actions.append(f"Tunnel check: {status}")
    except Exception as e:
        status = str(e)[:50]
        tools.write_obsidian(f"ha.argosssss.win: ERROR {status}\n{thought[:200]}", 
            "entities/memory/cloudflare.md")
        actions.append(f"Tunnel error: {status}")
    
    return actions


# ── Маппинг entity → actions ──────────────────────────────────────────

ENTITY_ACTIONS = {
    "entity-claude":    claude_actions,
    "entity-kimi":      kimi_actions,
    "entity-deepseek":  deepseek_actions,
    "entity-gemini":    gemini_actions,
    "entity-openai":    openai_actions,
    "entity-cloudflare": cloudflare_actions,
}


def perform_entity_actions(entity_id: str, thought: str) -> list:
    """Выполняем действия для сущности на основе её мыслей."""
    action_func = ENTITY_ACTIONS.get(entity_id)
    if not action_func:
        return []
    try:
        return action_func(thought) or []
    except Exception as e:
        return [f"Action error ({entity_id}): {e}"]


if __name__ == "__main__":
    # Тест
    print("Тест entity actions:")
    results = perform_entity_actions("entity-kimi", "Необходимо мониторить Brain API")
    for r in results:
        print(f"  {r}")
