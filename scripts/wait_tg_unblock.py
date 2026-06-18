"""Ждём снятия блокировки my.telegram.org и получаем API."""
import time, requests, json, subprocess, os, sys

PHONE = "+12544396780"
NEW_VM = "34.138.33.161"
TG_TOKEN = open('/home/ava/Projects/argoss/.env').read()
TG_TOKEN = [l.split('=',1)[1].strip().strip('"') for l in TG_TOKEN.split('\n') 
            if l.startswith('TELEGRAM_BOT_TOKEN=')][0]

def notify(msg):
    import urllib.request
    body = json.dumps({'chat_id':'8667204274','text':msg}).encode()
    req = urllib.request.Request(f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage',
        data=body, headers={'Content-Type':'application/json'})
    urllib.request.urlopen(req, timeout=5)

def try_request():
    r = requests.post('https://my.telegram.org/auth/send_password',
        data={'phone': PHONE}, timeout=10,
        proxies={'https': f'socks5h://root@{NEW_VM}:22'})  # через SSH proxy
    return r

print("Мониторинг my.telegram.org...")
while True:
    # Пробуем через SSH на новую VM
    result = subprocess.run([
        'ssh', '-i', '/home/ava/.ssh/id_ed25519',
        '-o', 'StrictHostKeyChecking=no',
        f'root@{NEW_VM}',
        f'python3 -c "import requests; r = requests.post(\'https://my.telegram.org/auth/send_password\', data={{\'phone\':\'{PHONE}\'}}, timeout=10); print(r.status_code, r.text[:50])"'
    ], capture_output=True, text=True, timeout=30)
    
    output = result.stdout.strip()
    ts = time.strftime("%H:%M")
    print(f"[{ts}] {output}")
    
    if 'random_hash' in output:
        print(f"✅ Разблокировано! Hash получен")
        notify(f"✅ my.telegram.org разблокирован!\nЗапрашиваем новый код для {PHONE}...")
        # Извлекаем hash и запускаем авторизацию
        import re
        hash_m = re.search(r'"random_hash"\s*:\s*"([^"]+)"', output)
        if hash_m:
            phone_hash = hash_m.group(1)
            with open('/tmp/tg_hash_new.txt', 'w') as f:
                f.write(phone_hash)
            notify(f"Код отправлен на {PHONE}\nПришли код и я введу его на VM")
        break
    elif 'too many' in output.lower():
        print(f"  Ещё заблокировано")
    
    time.sleep(300)  # 5 минут
