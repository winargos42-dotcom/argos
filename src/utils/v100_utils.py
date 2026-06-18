"""
Утилиты для мониторинга NVIDIA GPU (pynvml) и llama-server процессов.
Работает на локальной машине и через SSH (Orion).
"""
from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import psutil


def _nvml():
    """Ленивый импорт с fallback pynvml → nvidia-ml-py."""
    try:
        import nvidia_ml_py as nvml
    except Exception:
        import pynvml as nvml
    return nvml


@dataclass(frozen=True)
class GPUStat:
    index: int
    name: str
    memory_used_mb: float
    memory_total_mb: float
    temperature_c: Optional[int]
    gpu_util_pct: int
    power_w: Optional[float]
    process_count: int


def get_gpu_stats(index: int = 0) -> GPUStat:
    """Статистика по одному GPU через NVML."""
    nvml = _nvml()
    nvml.nvmlInit()
    handle = nvml.nvmlDeviceGetHandleByIndex(index)

    mem = nvml.nvmlDeviceGetMemoryInfo(handle)
    name = nvml.nvmlDeviceGetName(handle)
    try:
        temp = nvml.nvmlDeviceGetTemperature(handle, nvml.NVML_TEMPERATURE_GPU)
    except Exception:
        temp = None
    try:
        util = nvml.nvmlDeviceGetUtilizationRates(handle)
    except Exception:
        util = None
    try:
        power = nvml.nvmlDeviceGetPowerUsage(handle) / 1000
    except Exception:
        power = None
    try:
        procs = nvml.nvmlDeviceGetComputeRunningProcesses(handle)
    except Exception:
        procs = []

    return GPUStat(
        index=index,
        name=name,
        memory_used_mb=mem.used / 1024**2,
        memory_total_mb=mem.total / 1024**2,
        temperature_c=temp,
        gpu_util_pct=getattr(util, "gpu", 0) if util else 0,
        power_w=power,
        process_count=len(procs),
    )


def list_gpus() -> List[GPUStat]:
    """Список всех NVIDIA GPU."""
    nvml = _nvml()
    nvml.nvmlInit()
    count = nvml.nvmlDeviceGetCount()
    return [get_gpu_stats(i) for i in range(count)]


@dataclass(frozen=True)
class LlamaServerInfo:
    pid: int
    port: Optional[str]
    model: Optional[str]
    memory_mb: float
    cmdline: str


def get_llama_server_processes() -> List[LlamaServerInfo]:
    """Найти все llama-server процессы, извлечь порт и модель."""
    found: List[LlamaServerInfo] = []
    seen_pids = set()

    for proc in psutil.process_iter(["pid", "name", "cmdline", "memory_info"]):
        try:
            pid = proc.info["pid"]
            if pid in seen_pids:
                continue
            name = proc.info["name"] or ""
            cmdline_parts = proc.info["cmdline"] or []
            cmdline_str = " ".join(cmdline_parts)

            # строгая проверка: бинарий должен содержать llama-server, не просто любое упоминание
            if "llama-server" not in name and not any(
                part.endswith("llama-server") or part.endswith("llama-server.exe")
                for part in cmdline_parts
            ):
                continue

            port: Optional[str] = None
            model: Optional[str] = None
            for i, part in enumerate(cmdline_parts):
                if part == "--port" and i + 1 < len(cmdline_parts):
                    port = cmdline_parts[i + 1]
                if part.endswith(".gguf"):
                    model = os.path.basename(part)

            mem = proc.info["memory_info"]
            found.append(
                LlamaServerInfo(
                    pid=pid,
                    port=port,
                    model=model,
                    memory_mb=(mem.rss / 1024**2) if mem else 0,
                    cmdline=cmdline_str[:200],
                )
            )
            seen_pids.add(pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return found


def format_gpu_summary(gpu: GPUStat) -> str:
    return (
        f"[{gpu.index}] {gpu.name}: "
        f"{gpu.memory_used_mb:.0f}/{gpu.memory_total_mb:.0f} MiB, "
        f"{gpu.temperature_c}°C, {gpu.gpu_util_pct}% util, "
        f"{gpu.power_w or 0:.1f}W, {gpu.process_count} procs"
    )


if __name__ == "__main__":
    print("=== GPUs ===")
    try:
        for g in list_gpus():
            print(format_gpu_summary(g))
    except Exception as e:
        print(f"GPU error: {e}")

    print("\n=== llama-server processes ===")
    for s in get_llama_server_processes():
        print(f"PID {s.pid}: port={s.port} model={s.model} mem={s.memory_mb:.0f} MiB")
