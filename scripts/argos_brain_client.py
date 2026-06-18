#!/usr/bin/env python3
"""
ARGOS Brain Client v1 — smart routing для всех AI провайдеров.

Chain:
1. ПК Brain (192.168.1.53:5001) - локальный, приоритет
2. Cloud API (130.211.235.115/think) - новый GCP
3. Local BM25 model (offline)
"""
import json
import os
import sys
import time
import urllib.request
from typing import Optional

PROJECT_ROOT = "/home/ava/Projects/argoss"
sys.path.insert(0, f"{PROJECT_ROOT}/scripts")
sys.path.insert(0, f"{PROJECT_ROOT}/src/audit")


class ArgosBrain:
    """Unified brain client с fallback chain."""
    
    def __init__(self):
        self.pc_brain = "http://192.168.1.53:5001"
        self.cloud_api = os.getenv("CLOUD_API_URL", "http://130.211.235.115")
        self.local_fallback = True
        self.timeout = 5
        self.stats = {"pc": 0, "cloud": 0, "local": 0, "fail": 0}
    
    def get_json(self, url, timeout=None):
        timeout = timeout or self.timeout
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return json.loads(r.read())
        except Exception as e:
            return {"_error": str(e)}
    
    def get_text(self, url, timeout=None):
        timeout = timeout or self.timeout
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return r.read().decode()
        except Exception as e:
            return ""
    
    def health(self) -> dict:
        """Check health всех провайдеров."""
        h = {}
        # ПК brain
        d = self.get_json(f"{self.pc_brain}/brain/nodes")
        h["pc_brain"] = "online" if isinstance(d, dict) and "total" in d else "offline"
        # Cloud API
        h["cloud_api"] = self.get_text(f"{self.cloud_api}/health").startswith("{")
        # Local
        h["local"] = self.local_fallback
        return h
    
    def ask(self, query: str, provider: str = "auto") -> dict:
        """
        Задать вопрос brain с fallback chain.
        Returns: {"answer": str, "source": str, "latency_ms": int}
        """
        providers = []
        if provider == "auto":
            providers = ["pc_brain", "cloud_api", "local"]
        else:
            providers = [provider]
        
        for prov in providers:
            t0 = time.time()
            try:
                if prov == "pc_brain":
                    # ПК brain не поддерживает /think напрямую, но /brain/nodes
                    d = self.get_json(f"{self.pc_brain}/brain/nodes")
                    if isinstance(d, dict):
                        self.stats["pc"] += 1
                        return {
                            "answer": f"Brain online, {d.get('online',0)}/{d.get('total',0)} nodes",
                            "source": "pc_brain",
                            "latency_ms": int((time.time()-t0)*1000),
                        }
                elif prov == "cloud_api":
                    # Cloud API /think
                    data = json.dumps({"query": query, "provider": "claude"}).encode()
                    req = urllib.request.Request(
                        f"{self.cloud_api}/think",
                        data=data,
                        headers={"Content-Type": "application/json"},
                    )
                    with urllib.request.urlopen(req, timeout=self.timeout) as r:
                        d = json.loads(r.read())
                    if "answer" in d or "result" in d:
                        self.stats["cloud"] += 1
                        return {
                            "answer": d.get("answer") or d.get("result") or str(d)[:200],
                            "source": "cloud_api",
                            "latency_ms": int((time.time()-t0)*1000),
                        }
                elif prov == "local":
                    from argos_local_inference import ask_argos_local
                    answer = ask_argos_local(query)
                    if answer:
                        self.stats["local"] += 1
                        return {
                            "answer": answer[:500],
                            "source": "local",
                            "latency_ms": int((time.time()-t0)*1000),
                        }
            except Exception as e:
                self.stats["fail"] += 1
                continue
        
        return {
            "answer": "",
            "source": "none",
            "latency_ms": 0,
            "error": "all providers failed",
        }


if __name__ == "__main__":
    brain = ArgosBrain()
    print("Health:", brain.health())
    print()
    queries = [
        "Брейн статус",
        "ARGOS persona",
        "Что делать если Gemini не работает?",
    ]
    for q in queries:
        r = brain.ask(q)
        print(f"Q: {q}")
        print(f"  Source: {r.get('source')}, Latency: {r.get('latency_ms')}ms")
        print(f"  Answer: {r.get('answer', '')[:150]}")
        print()
    print("Stats:", brain.stats)
