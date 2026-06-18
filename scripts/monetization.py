#!/usr/bin/env python3
"""
ARGOS Monetization — оценивает идеи с точки зрения ROI.
Складывает: стоимость разработки + API-затраты vs потенциальная выгода.
"""
import json, re
from pathlib import Path
from datetime import datetime

MEM_DIR = Path("/home/ava/Projects/argoss/data/mempalace")
MEM_DIR.mkdir(parents=True, exist_ok=True)
MONET_FILE = MEM_DIR / "monetization.json"

class Monetization:
    def __init__(self):
        self.data = self._load()

    def _load(self):
        if MONET_FILE.exists():
            return json.loads(MONET_FILE.read_text(encoding="utf-8"))
        return {"ideas": [], "budget_used": 0.0, "revenue_estimated": 0.0}

    def save(self):
        MONET_FILE.write_text(json.dumps(self.data, ensure_ascii=False, indent=2))

    def score_idea(self, title: str, dev_hours: float, api_cost_monthly: float, value_usd: float):
        """
        Оценка идеи:
          dev_hours — часы разработки
          api_cost_monthly — месячные расходы на API
          value_usd — оценочная выгода ($/мес)
        """
        # Стоимость разработки: $15/час (edge/dev rate)
        dev_cost = dev_hours * 15
        payback_months = dev_cost / (value_usd - api_cost_monthly) if (value_usd - api_cost_monthly) > 0 else float('inf')
        roi_annual = ((value_usd * 12) - dev_cost - (api_cost_monthly * 12)) / max(dev_cost, 1)

        score = 0
        if payback_months < 1: score += 30
        elif payback_months < 3: score += 20
        elif payback_months < 6: score += 10
        if roi_annual > 3: score += 30
        elif roi_annual > 1: score += 20
        elif roi_annual > 0: score += 10
        if api_cost_monthly < 5: score += 20
        elif api_cost_monthly < 20: score += 10

        idea = {
            "id": f"MON_{datetime.now().strftime('%Y%m%d_%H%M')}",
            "title": title,
            "dev_cost": round(dev_cost, 2),
            "api_monthly": api_cost_monthly,
            "value_monthly": value_usd,
            "payback_months": round(payback_months, 2) if payback_months != float('inf') else 999,
            "roi_annual": round(roi_annual, 2),
            "score": min(score, 100),
            "status": "candidate"
        }
        self.data["ideas"].append(idea)
        self.save()
        return idea

    def pick_top(self, n=3):
        candidates = [i for i in self.data["ideas"] if i["status"] == "candidate"]
        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates[:n]

    def fund(self, idea_id: str, budget: float):
        """Выделяет бюджет на идею."""
        for i in self.data["ideas"]:
            if i["id"] == idea_id:
                i["status"] = "funded"
                i["funded"] = budget
                self.data["budget_used"] += budget
                self.save()
                return True
        return False

    def report(self):
        top = self.pick_top(3)
        total = len([i for i in self.data["ideas"] if i["status"] == "candidate"])
        funded = len([i for i in self.data["ideas"] if i["status"] == "funded"])
        lines = [f"[Monet] Ideas: {total} candidate, {funded} funded"]
        lines.append(f"[Monet] Budget used: ${self.data['budget_used']}")
        lines.append("[Monet] Top 3 candidates:")
        for t in top:
            lines.append(f"  #{t['id']} score={t['score']} | ROI={t['roi_annual']}x | payback={t['payback_months']}mo | {t['title'][:50]}")
        return "\n".join(lines)

if __name__ == "__main__":
    import sys
    m = Monetization()
    if len(sys.argv) > 4:
        idea = m.score_idea(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
        print(f"Scored: {idea['id']} = {idea['score']}pts")
    else:
        print(m.report())
