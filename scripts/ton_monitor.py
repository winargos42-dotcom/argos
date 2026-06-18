"""TON мониторинг - проверяет баланс каждые 30 мин и уведомляет."""
import time, urllib.request, json

WALLET = "UQD9K89C7n779rBLWzWY60bhLF7VPSuN1KmTLgdkRSU8kSnx"
TG_TOKEN = open('/home/ava/Projects/argoss/.env').read()
TG_TOKEN = [l.split('=',1)[1].strip().strip('"') for l in TG_TOKEN.split('\n') if l.startswith('TELEGRAM_BOT_TOKEN=')][0]

def get_balance():
    try:
        req = urllib.request.Request(f"https://toncenter.com/api/v2/getAddressBalance?address={WALLET}")
        with urllib.request.urlopen(req, timeout=10) as r:
            return int(json.loads(r.read()).get("result","0")) / 1e9
    except: return 0.0

def get_price():
    try:
        req = urllib.request.Request("https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd,rub")
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read())
            return d["the-open-network"]["usd"], d["the-open-network"]["rub"]
    except: return 1.96, 142

def notify(msg):
    body = json.dumps({"chat_id":"6923777384","text":msg}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
        data=body,headers={"Content-Type":"application/json"})
    try: urllib.request.urlopen(req,timeout=5)
    except: pass

last_balance = get_balance()
usd, rub = get_price()
notify(f"💎 TON Monitor запущен\nКошелёк: {WALLET[:20]}...\nБаланс: {last_balance:.4f} TON\nЦена: ${usd:.2f} (₽{rub:.0f})\nМониторинг: каждые 30 мин")
print(f"TON Monitor: {last_balance:.4f} TON = ${last_balance*usd:.2f}")

while True:
    time.sleep(1800)
    bal = get_balance()
    if bal > last_balance:
        diff = bal - last_balance
        usd, rub = get_price()
        notify(f"💎 TON получен! +{diff:.4f} TON (+${diff*usd:.4f})\nИтого: {bal:.4f} TON = ${bal*usd:.2f}")
        print(f"TON +{diff:.4f}!")
    last_balance = bal
    print(f"TON: {bal:.4f}")
