import subprocess, time, os
from datetime import datetime

NVSMI   = r"C:\windows\system32\nvidia-smi.exe"
LOG     = r"I:\argos-training\thermal.log"
MAX_PL  = 300
LOW_PL  = 220
HOT     = 75
COOL    = 70
INTERVAL = 15

def smi(*args):
    r = subprocess.run([NVSMI] + list(args), capture_output=True, text=True, timeout=10)
    return r.stdout.strip()

def get_temp():
    try:
        return int(smi("--query-gpu=temperature.gpu", "--format=csv,noheader"))
    except:
        return -1

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def main():
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    smi("-pl", str(MAX_PL), "-i", "0")
    log(f"V100 Thermal Monitor START | T={get_temp()}C PL={MAX_PL}W")
    log(f"Rule: T>={HOT}C -> {LOW_PL}W  T<{COOL}C -> {MAX_PL}W")
    throttled = False
    while True:
        temp = get_temp()
        if temp < 0:
            log("ERROR reading temp!")
            time.sleep(INTERVAL)
            continue
        log(f"T={temp}C  PL_mode={'LOW' if throttled else 'MAX'}")
        if temp >= HOT and not throttled:
            log(f"WARN: {temp}C >= {HOT}C - power -> {LOW_PL}W")
            smi("-pl", str(LOW_PL), "-i", "0")
            throttled = True
        elif temp < COOL and throttled:
            log(f"OK: {temp}C < {COOL}C - power -> {MAX_PL}W")
            smi("-pl", str(MAX_PL), "-i", "0")
            throttled = False
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
