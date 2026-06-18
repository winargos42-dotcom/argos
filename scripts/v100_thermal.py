#!/usr/bin/env python3
"""
V100 Thermal Monitor — мониторинг температуры Tesla V100-SXM2.
V100-SXM2 не имеет GPU-вентиляторов, управляем через Power Limit.

При ≥75°C → снижаем TDP до 80% (200W из 250W)
При <70°C → восстанавливаем TDP до 100% (250W)
"""
import subprocess, time, sys
from datetime import datetime

NVIDIA_SMI = r"C:\windows\system32\nvidia-smi.exe"
GPU_IDX    = 0
MAX_POWER  = 250   # Вт (V100 SXM2 TDP)
LOW_POWER  = 200   # Вт при перегреве
TEMP_HOT   = 75    # °C — переключаемся на LOW_POWER
TEMP_COOL  = 70    # °C — возвращаемся к MAX_POWER
INTERVAL   = 15    # сек между проверками

def smi(*args):
    try:
        r = subprocess.run([NVIDIA_SMI] + list(args),
                           capture_output=True, text=True, timeout=10)
        return r.stdout.strip()
    except Exception as e:
        return f"ERROR: {e}"

def get_temp() -> int:
    out = smi("--query-gpu=temperature.gpu", "--format=csv,noheader")
    try:
        return int(out.strip())
    except:
        return -1

def get_power_limit() -> int:
    out = smi("--query-gpu=power.limit", "--format=csv,noheader")
    try:
        return int(float(out.replace("W","").strip()))
    except:
        return -1

def set_power_limit(watts: int):
    result = smi(f"-pl", str(watts), f"-i", str(GPU_IDX))
    print(f"  [nvidia-smi -pl {watts}] → {result[:80]}")

def now():
    return datetime.now().strftime("%H:%M:%S")

def main():
    print(f"[{now()}] V100 Thermal Monitor запущен")
    print(f"  GPU: Tesla V100-SXM2-16GB (нет вентиляторов)")
    print(f"  Режим: при ≥{TEMP_HOT}°C → power limit {LOW_POWER}W, при <{TEMP_COOL}°C → {MAX_POWER}W")

    throttled = False
    current_pl = get_power_limit()
    print(f"  Текущий Power Limit: {current_pl}W")

    # Убедимся что начинаем с MAX
    if current_pl != MAX_POWER:
        set_power_limit(MAX_POWER)

    while True:
        temp = get_temp()
        pl   = get_power_limit()

        if temp < 0:
            print(f"[{now()}] Ошибка чтения температуры!")
            time.sleep(INTERVAL)
            continue

        status = "THROTTLE" if throttled else "OK"
        print(f"[{now()}] T={temp}°C  PL={pl}W  [{status}]")

        if temp >= TEMP_HOT and not throttled:
            print(f"  ⚠ Температура {temp}°C ≥ {TEMP_HOT}°C — снижаем Power Limit до {LOW_POWER}W")
            set_power_limit(LOW_POWER)
            throttled = True

        elif temp < TEMP_COOL and throttled:
            print(f"  ✓ Температура {temp}°C < {TEMP_COOL}°C — восстанавливаем Power Limit до {MAX_POWER}W")
            set_power_limit(MAX_POWER)
            throttled = False

        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
