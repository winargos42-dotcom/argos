#!/usr/bin/env python3
"""
Curiosity Module — автономная генерация задач из Prometheus алертов.
Если узел падает, RAM растёт, диск заполняется — система сама ставит задачу в WORKING.md.
"""
import json, os, re, datetime

WORKING_MD = "/home/ava/Documents/MyObsidianVault/SharedMemory/shared/WORKING.md"

def add_task(title: str, desc: str, priority: str = "medium"):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"\n- [ ] **{ts}** [{priority.upper()}] {title}\n  - {desc}\n"
    with open(WORKING_MD, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"[Curiosity] Task added: {title}")

def handle_alert(alert: dict):
    """Превращает Prometheus алерт в задачу"""
    name = alert.get("labels", {}).get("alertname", "Unknown")
    summary = alert.get("annotations", {}).get("summary", "")
    instance = alert.get("labels", {}).get("instance", "")

    rules = {
        "HighMemoryUsage": ("Оптимизировать RAM на {instance}", "Память >90%. Пересмотреть кэш/логи/сервисы."),
        "HighDiskUsage":   ("Очистить диск на {instance}", "Диск >85%. Удалить старые логи docker system prune."),
        "ServiceDown":     ("Поднять сервис на {instance}", "Сервис упал. Проверить systemd/docker."),
        "NodeOffline":     ("Восстановить узел {instance}", "Heartbeat потерян. Проверить питание/сеть."),
    }

    if name in rules:
        title_tpl, desc_tpl = rules[name]
        add_task(title_tpl.format(instance=instance), desc_tpl.format(instance=instance), priority="high")
    else:
        add_task(f"Разобраться: {name} на {instance}", summary or "Новый алерт без правила — нужен анализ.", "medium")

# === Webhook receiver ===
from fastapi import FastAPI, Request
app = FastAPI()

@app.post("/webhook/alertmanager")
async def alertmanager_webhook(request: Request):
    data = await request.json()
    alerts = data.get("alerts", [])
    for a in alerts:
        if a.get("status") == "firing":
            handle_alert(a)
    return {"status": "ok", "tasks_created": len(alerts)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3457)
