#!/usr/bin/env python3
"""
Emergency recovery ARGOS на ПК через MCP/npx после удаления Кими.
Запускается СРАЗУ КАК MCP вернётся.

Шаги:
1. Проверить состояние main.py — есть/нет/пустой
2. Если плохо — залить локальную копию (34430 B, md5 d7dc1b9f)
3. Залить обновлённые 4 фикса (core, db_init, hive_mind, telegram_bot)
4. Запустить main.py через PowerShell Start-Process (background, без блока)
5. Подождать пока ArgosOS :8010 ответит
"""
import json, base64, urllib.request, os, hashlib, time, sys

PC_MCP = "http://192.168.1.53:8000/mcp"
LOCAL_MAIN = "/home/ava/Projects/argoss/main.py"
REMOTE_MAIN = "F:\\\\debug\\\\argoss\\\\main.py"
CHUNK = 4000

def npx(js, timeout=120):
    body = {"jsonrpc":"2.0","id":1,"method":"tools/call",
        "params":{"name":"npm","arguments":{
            "command":"npx","package":"-y","args":["node","-e",js]}}}
    req = urllib.request.Request(PC_MCP, data=json.dumps(body).encode(),
        headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())['result']['content'][0]['text']
    except Exception as e:
        return f"ERR: {e}"

def write_remote(local_path, remote_path):
    content = open(local_path, 'rb').read()
    b64 = base64.b64encode(content).decode('ascii')
    rp = remote_path.replace('\\', '\\\\')
    js0 = f'const fs=require("fs"),p=require("path"); const t="{rp}"; const d=p.dirname(t); if(!fs.existsSync(d))fs.mkdirSync(d,{{recursive:true}}); if(fs.existsSync(t))fs.copyFileSync(t, t+".bak_emergency_2026-05-23"); fs.writeFileSync(t, ""); console.log("INIT")'
    if 'INIT' not in npx(js0):
        return "INIT_FAIL"
    chunks = [b64[i:i+CHUNK] for i in range(0, len(b64), CHUNK)]
    print(f"  {len(chunks)} chunks", flush=True)
    for i, ch in enumerate(chunks):
        js = f'const fs=require("fs"); fs.appendFileSync("{rp}", Buffer.from("{ch}","base64"));'
        r = npx(js, timeout=60)
        if 'ERR' in r[:10]:
            return f"FAIL@{i}"
    js_ver = f'const fs=require("fs"),c=require("crypto"); const d=fs.readFileSync("{rp}"); console.log("SIZE", d.length, "MD5", c.createHash("md5").update(d).digest("hex"))'
    return npx(js_ver)

# 1) ДИАГНОСТИКА
js_diag = '''const fs=require("fs"),c=require("crypto"); const dir="F:\\\\debug\\\\argoss";
const m=dir+"\\\\main.py";
if(fs.existsSync(m)){
  const data=fs.readFileSync(m);
  console.log("main.py: EXISTS size=" + data.length + " md5=" + c.createHash("md5").update(data).digest("hex"));
}else{
  console.log("main.py: MISSING");
}
const mfiles=fs.readdirSync(dir).filter(f=>/main/i.test(f)||/\\.bak/i.test(f));
console.log("RELATED FILES:");
for(const f of mfiles){
  try{const s=fs.statSync(dir+"\\\\"+f); console.log("  "+f+" "+s.size+"B "+s.mtime.toISOString());}catch(e){}
}'''
print("=== STEP 1: DIAGNOSE ===", flush=True)
diag = npx(js_diag)
print(diag, flush=True)

# 2) RESTORE main.py если плохо
restore_needed = "MISSING" in diag or "size=0 " in diag
if restore_needed:
    print(f"\n=== STEP 2: RESTORE main.py from {LOCAL_MAIN} ===", flush=True)
    md5 = hashlib.md5(open(LOCAL_MAIN,'rb').read()).hexdigest()
    print(f"  local md5={md5}", flush=True)
    r = write_remote(LOCAL_MAIN, REMOTE_MAIN)
    print(f"  Result: {r[:200]}", flush=True)
    if md5 not in r:
        print("  ❌ Restore failed — стоп", flush=True)
        sys.exit(1)
    print("  ✅ main.py restored", flush=True)
else:
    print("\n=== STEP 2: SKIP (main.py жив) ===", flush=True)

# 3) Re-flash 4 fix files
print("\n=== STEP 3: RE-APPLY 4 FIXES ===", flush=True)
FIXES = [
    ('/home/ava/Projects/argoss/src/core.py',                     'F:\\\\debug\\\\argoss\\\\src\\\\core.py'),
    ('/home/ava/Projects/argoss/src/db_init.py',                  'F:\\\\debug\\\\argoss\\\\src\\\\db_init.py'),
    ('/home/ava/Projects/argoss/src/skills/hive_mind.py',         'F:\\\\debug\\\\argoss\\\\src\\\\skills\\\\hive_mind.py'),
    ('/home/ava/Projects/argoss/src/connectivity/telegram_bot.py','F:\\\\debug\\\\argoss\\\\src\\\\connectivity\\\\telegram_bot.py'),
]
for local, remote in FIXES:
    name = os.path.basename(local)
    print(f"→ {name}", flush=True)
    md5 = hashlib.md5(open(local,'rb').read()).hexdigest()
    r = write_remote(local, remote.replace('\\\\','\\'))
    if md5 in r:
        print(f"  ✅ OK", flush=True)
    else:
        print(f"  ⚠️ {r[:120]}", flush=True)

print("\n=== ВСЁ ВОССТАНОВЛЕНО ===", flush=True)
print("Сева, перезапусти main.py — TG-бот вернётся к жизни.", flush=True)
