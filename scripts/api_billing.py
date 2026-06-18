#!/usr/bin/env python3
"""
ARGOS API Billing — учёт затрат на внешние API.
DeepSeek, OpenAI, Twilio, Avantgarde SMS и т.д.
"""
import json, os, re
from pathlib import Path
from datetime import datetime, timedelta

MEM_DIR = Path("/home/ava/Projects/argoss/data/mempalace")
MEM_DIR.mkdir(parents=True, exist_ok=True)
BILLING_FILE = MEM_DIR / "api_billing.json"

# Цены (USD per 1K токенов / per unit)
RATES = {
    "deepseek-chat": {"input": 0.0001, "output": 0.0005, "unit": "1K"},
    "deepseek-reasoner": {"input": 0.001, "output": 0.005, "unit": "1K"},
    "openai-gpt4o": {"input": 0.005, "output": 0.015, "unit": "1K"},
    "twilio-sms": {"per_msg": 0.0075, "unit": "msg"},
    "avantgarde-sms": {"per_msg": 0.02, "unit": "msg"},
}

class BillingTracker:
    def __init__(self):
        self.data = self.load()

    def load(self):
        if BILLING_FILE.exists():
            return json.loads(BILLING_FILE.read_text(encoding="utf-8"))
        return {"entries": [], "daily_totals": {}, "monthly_budget": 50.0}

    def save(self):
        BILLING_FILE.write_text(json.dumps(self.data, ensure_ascii=False, indent=2))

    def log(self, api: str, units: float, meta=None):
        """Записывает расход. api='deepseek-chat', units=токены/сообщения."""
        rate = RATES.get(api, {})
        cost = 0.0
        if "per_msg" in rate:
            cost = units * rate["per_msg"]
        elif "input" in rate:
            # Assume 2:1 output ratio, average cost per 1K
            avg = (rate["input"] + rate["output"]) / 2
            cost = (units / 1000) * avg

        entry = {
            "ts": datetime.now().isoformat(),
            "api": api,
            "units": units,
            "cost_usd": round(cost, 6),
            "meta": meta or {}
        }
        self.data["entries"].append(entry)

        # Daily total
        day = datetime.now().strftime("%Y-%m-%d")
        self.data["daily_totals"][day] = self.data["daily_totals"].get(day, 0) + cost

        self.save()
        return cost

    def today_cost(self):
        day = datetime.now().strftime("%Y-%m-%d")
        return round(self.data["daily_totals"].get(day, 0), 4)

    def month_cost(self):
        month = datetime.now().strftime("%Y-%m")
        total = 0
        for day, cost in self.data["daily_totals"].items():
            if day.startswith(month):
                total += cost
        return round(total, 4)

    def budget_status(self):
        spent = self.month_cost()
        budget = self.data.get("monthly_budget", 50.0)
        return {"spent": spent, "budget": budget, "pct": round(spent / budget * 100, 2)}

    def estimate_task(self, task_complexity="medium"):
        """Оценка: сколько будет стоить задача."""
        estimates = {
            "low": {"tokens": 2000, "calls": 1},
            "medium": {"tokens": 5000, "calls": 2},
            "high": {"tokens": 15000, "calls": 5}
        }
        e = estimates.get(task_complexity, estimates["medium"])
        avg_cost_per_1k = (RATES["deepseek-chat"]["input"] + RATES["deepseek-chat"]["output"]) / 2
        cost = (e["tokens"] / 1000) * avg_cost_per_1k * e["calls"]
        return round(cost, 4)

    def report(self):
        status = self.budget_status()
        return f"[Billing] Today: ${self.today_cost()} | Month: ${status['spent']}/${status['budget']} ({status['pct']}%)"

if __name__ == "__main__":
    bt = BillingTracker()
    import sys
    if len(sys.argv) > 2:
        cost = bt.log(sys.argv[1], float(sys.argv[2]))
        print(f"Logged: {sys.argv[1]} = ${cost}")
    else:
        print(bt.report())
        print(f"Medium task estimate: ${bt.estimate_task('medium')}")
