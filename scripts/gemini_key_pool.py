# Gemini Key Pool Manager for ARGOS
# Usage: python3 gemini_key_pool.py --test-all | --rotate | --status

import os, json, sys, time, random
from pathlib import Path

# Pool config
KEY_NAMES = [f"GEMINI_API_KEY_{i}" for i in range(1, 10)] + ["GEMINI_API_KEY"]
PROXY_URL = "https://argos-core-508337926357.us-central1.run.app/proxy/gemini"
MODEL = "gemini-2.5-flash"

ENV_PATH = os.environ.get("ARGOS_ENV", r"F:\debug\argoss\.env")

def load_env_keys():
    """Load all GEMINI_API_KEY* from .env file"""
    keys = {}
    if not os.path.exists(ENV_PATH):
        print(f"ENV not found: {ENV_PATH}")
        return keys
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            for name in KEY_NAMES:
                if line.startswith(f"{name}="):
                    keys[name] = line.split("=", 1)[1].split("#")[0].strip()
    return keys

def test_key(key, proxy=True):
    """Test single key. Returns (success, latency_ms, error_or_text)"""
    import urllib.request, ssl
    url = f"{PROXY_URL}/v1beta/models/{MODEL}:generateContent?key={key}" if proxy else \
          f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
    body = json.dumps({"contents": [{"parts": [{"text": "hi"}]}]}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    ctx = ssl.create_default_context()
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            data = json.loads(resp.read().decode())
            latency = int((time.time() - start) * 1000)
            text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            return True, latency, text[:50]
    except Exception as e:
        latency = int((time.time() - start) * 1000)
        return False, latency, str(e)

def test_all_keys(keys):
    """Test all keys, print table"""
    results = []
    for name, key in keys.items():
        ok, lat, err = test_key(key)
        status = "✅ OK" if ok else f"❌ FAIL"
        detail = f"{lat}ms {err[:40]}" if ok else err[:60]
        results.append((name, status, detail))
        print(f"{name:20s} {status:10s} {detail}")
        time.sleep(0.5)  # rate limit
    ok_count = sum(1 for r in results if "OK" in r[1])
    print(f"\n--- {ok_count}/{len(results)} keys active ---")
    return results

def rotate_key(keys):
    """Return best working key"""
    for name, key in keys.items():
        ok, lat, _ = test_key(key)
        if ok:
            print(f"ACTIVE: {name} ({lat}ms)")
            return name, key
        time.sleep(0.3)
    print("NO ACTIVE KEYS")
    return None, None

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-all", action="store_true", help="Test all keys")
    parser.add_argument("--rotate", action="store_true", help="Find best working key")
    parser.add_argument("--status", action="store_true", help="Show pool status")
    args = parser.parse_args()

    keys = load_env_keys()
    if not keys:
        print("No keys loaded")
        sys.exit(1)

    print(f"Loaded {len(keys)} keys from {ENV_PATH}")
    print(f"Proxy: {PROXY_URL}")
    print(f"Model: {MODEL}\n")

    if args.test_all:
        test_all_keys(keys)
    elif args.rotate:
        rotate_key(keys)
    elif args.status:
        for name in KEY_NAMES:
            key = keys.get(name)
            print(f"{name:20s} {'SET' if key else 'MISSING'} ({len(key) if key else 0} chars)")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
