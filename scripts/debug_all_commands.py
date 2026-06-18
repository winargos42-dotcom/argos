"""Дебаг всех 40 команд бота + параллельная эволюция."""
import asyncio, time, json

API_ID = 2040; API_HASH = "b18441a1ff607e10a989891a5462e627"
SESSION = "/home/ava/Projects/argoss/data/sessions/ava_main"
GROUP_ID = -5129226282

ALL_CMDS = [
    "/start","/status","/help","/commands","/reasoning","/think",
    "/coding_agent","/model","/models","/providers","/agents","/limits",
    "/skill","/skills","/skills_check","/taskflow","/subagents",
    "/network","/sync","/memory","/history","/context","/session",
    "/compact","/reset","/iot","/smart","/geo","/crypto","/tts",
    "/voice_on","/voice_off","/roles","/alerts","/github","/whoami",
    "/arc_status","/tghealth","/verbose","/fast"
]

WAIT = 18  # сек ожидания ответа

async def main():
    from telethon import TelegramClient
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.connect()
    bot = await client.get_entity("@Argosssbot")

    results = {}
    ok_count = 0
    
    print(f"{'='*50}")
    print(f"ДЕБАГ {len(ALL_CMDS)} КОМАНД @Argosssbot")
    print(f"{'='*50}\n")
    
    for i, cmd in enumerate(ALL_CMDS, 1):
        t = time.time()
        await client.send_message(bot, cmd)
        await asyncio.sleep(WAIT)
        
        msgs = await client.get_messages(bot, limit=8)
        resp = None
        for m in msgs:
            if not m.out and m.date.timestamp() > t - 1:
                resp = m.text or "[медиа]"
                break
        
        if resp:
            ok_count += 1
            status = "✅"
            short = resp[:60].replace('\n',' ')
        else:
            status = "❌"
            short = "нет ответа"
        
        results[cmd] = {"ok": resp is not None, "response": resp or ""}
        print(f"[{i:02d}/40] {status} {cmd:20} → {short}")
    
    # Отчёт
    print(f"\n{'='*50}")
    print(f"ИТОГ: {ok_count}/40 команд работают")
    
    broken = [k for k,v in results.items() if not v["ok"]]
    if broken:
        print(f"\n❌ Не работают ({len(broken)}):")
        for b in broken: print(f"  {b}")
    
    # Сохраняем результат
    json.dump(results, open("/tmp/cmd_debug_full.json","w"), ensure_ascii=False, indent=2)
    
    # Публикуем отчёт в Entity Council
    TOKENS = json.load(open("/home/ava/Projects/argoss/data/entity_bot_tokens.json"))
    main_token = TOKENS.get("argos_claude_ai_bot")
    if main_token:
        report = f"📊 Дебаг @Argosssbot ({ok_count}/40):\n\n"
        for cmd, r in results.items():
            s = "✅" if r["ok"] else "❌"
            report += f"{s} `{cmd}`\n"
        
        import urllib.request
        body = json.dumps({"chat_id":GROUP_ID,"text":report}).encode()
        req = urllib.request.Request(f"https://api.telegram.org/bot{main_token}/sendMessage",
            data=body,headers={"Content-Type":"application/json"})
        try: urllib.request.urlopen(req,timeout=8)
        except: pass
    
    await client.disconnect()
    return ok_count, broken

asyncio.run(main())
