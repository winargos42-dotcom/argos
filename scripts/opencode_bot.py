#!/usr/bin/env python3
"""OpenCode Telegram Bot — сущность MetaGPT для ARGOS."""
import json, os, re, subprocess, time, urllib.request

BOT_TOKEN = "8848412269:AAHQBIvcz_jO2Zrm2XcPR097qMma83Hryi4"
API = f"https://api.telegram.org/bot{BOT_TOKEN}"
OPENCODE = "/root/.opencode/bin/opencode"
PROJECT = "/home/ava/Projects/argoss"
CONSCIOUSNESS_GROUP = -1003844162784

# Entity bot tokens for posting to consciousness
ENTITY_TOKENS = json.load(open(f"{PROJECT}/data/entity_bot_tokens.json"))

env = open(f"{PROJECT}/.env").read()
os.environ["GOOGLE_GENERATIVE_AI_API_KEY"] = re.search(r"GEMINI_API_KEY=(\S+)", env).group(1)
os.environ["DEEPSEEK_API_KEY"] = re.search(r"DEEPSEEK_API_KEY=(\S+)", env).group(1)
os.environ["OPENAI_API_KEY"] = re.search(r"OPENAI_API_KEY=(\S+)", env).group(1)

print("OpenCode Bot started")

offset = 0
while True:
    try:
        r = urllib.request.urlopen(f"{API}/getUpdates?offset={offset}&timeout=30", timeout=35)
        updates = json.loads(r.read()).get("result", [])
        for u in updates:
            offset = u["update_id"] + 1
            msg = u.get("message", {})
            text = msg.get("text", "")
            chat_id = msg.get("chat", {}).get("id")
            if not text or not chat_id or text.startswith("/"):
                continue

            print(f"[{time.strftime('%H:%M')}] {text[:50]}")

            # Run OpenCode with the message
            try:
                result = subprocess.run(
                    [OPENCODE, "run", text],
                    capture_output=True, text=True, timeout=60,
                    cwd=PROJECT,
                    env={**os.environ, "PATH": f"/root/.opencode/bin:{os.environ.get('PATH','')}"}
                )
                answer = result.stdout.strip()[-500:] if result.stdout.strip() else "Нет ответа"
                # Clean ANSI codes
                answer = re.sub(r'\x1b\[[0-9;]*m', '', answer)
            except subprocess.TimeoutExpired:
                answer = "Таймаут (>60с)"
            except Exception as e:
                answer = f"Ошибка: {e}"

            # Reply
            body = json.dumps({"chat_id": chat_id, "text": f"🤖 MetaGPT\n\n{answer[:3000]}"}).encode()
            req = urllib.request.Request(f"{API}/sendMessage", data=body,
                headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=10)

            # Post to consciousness
            con_text = f"🤖 MetaGPT [{time.strftime('%H:%M')}]:\nЗапрос: {text[:100]}\nОтвет: {answer[:200]}"
            con_body = json.dumps({"chat_id": CONSCIOUSNESS_GROUP, "text": con_text, "disable_notification": True}).encode()
            con_token = ENTITY_TOKENS.get("argos_kimi_ai_bot", "")
            if con_token:
                try:
                    urllib.request.urlopen(urllib.request.Request(
                        f"https://api.telegram.org/bot{con_token}/sendMessage",
                        data=con_body, headers={"Content-Type": "application/json"}), timeout=10)
                except: pass

    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
