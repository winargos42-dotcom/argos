"""Запускает цикл эволюции в ARGOS Entity Council группе."""
import asyncio, json, urllib.request

API_ID = 2040; API_HASH = "b18441a1ff607e10a989891a5462e627"
SESSION = "/home/ava/Projects/argoss/data/sessions/ava_main"
GROUP_ID = -5129226282
GCP = "https://argos-core-m3gk27ccqa-uc.a.run.app"

TOKENS = json.load(open("/home/ava/Projects/argoss/data/entity_bot_tokens.json"))

ENTITIES = {
    "argos_claude_ai_bot":   ("Клод",    "Аналитик: что нужно улучшить в ARGOS прямо сейчас?"),
    "argos_kimi_ai_bot":     ("Кими",    "Исследователь: какой паттерн ты заметил в работе системы?"),
    "argos_gemini_v3_bot":   ("Джемини", "Визуалист: как ты видишь эволюцию системы?"),
    "argos_deepseek_v3_bot": ("Дипсик",  "Логик: рассчитай оптимальный следующий шаг."),
    "argos_openai_v3_bot":   ("OpenAI",  "Универсал: предложи одно конкретное действие для развития."),
}

def ask(prompt):
    body = json.dumps({"prompt": prompt, "provider": "claude"}).encode()
    req = urllib.request.Request(f"{GCP}/proxy/ask", data=body,
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read()).get("response","")[:250]
    except: return ""

def send_to_group(token, text):
    body = json.dumps({"chat_id": GROUP_ID, "text": text, "parse_mode": "Markdown"}).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=body, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=10)
        return True
    except: return False

async def main():
    print("🧬 ARGOS Entity Council — Цикл эволюции\n")
    
    thoughts = {}
    for username, (name, prompt) in ENTITIES.items():
        token = TOKENS.get(username)
        if not token: continue
        
        full_prompt = (f"Ты — {name}, AI-сущность ARGOS Universal OS. "
                      f"{prompt} Ответь от первого лица. 2 предложения. На русском.")
        
        thought = ask(full_prompt)
        if thought:
            thoughts[name] = thought
            ok = send_to_group(token, f"🧠 **{name}:**\n{thought}")
            print(f"{'✅' if ok else '❌'} {name}: {thought[:60]}...")
        
        await asyncio.sleep(2)
    
    # Синтез через главный бот
    if thoughts:
        synthesis_prompt = (
            "Ты ARGOS — коллективный разум. Сущности сказали:\n" +
            "\n".join(f"• {n}: {t[:100]}" for n,t in thoughts.items()) +
            "\n\nСделай синтез в 3 конкретных шага развития. На русском."
        )
        synthesis = ask(synthesis_prompt)
        if synthesis:
            main_token = TOKENS.get("argos_claude_ai_bot")
            if main_token:
                send_to_group(main_token, f"🌐 **СИНТЕЗ СОВЕТА:**\n\n{synthesis}")
                print(f"\n✅ Синтез опубликован")
    
    print("\n✅ Цикл эволюции завершён!")

asyncio.run(main())
