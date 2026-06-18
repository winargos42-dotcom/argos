#!/usr/bin/env python3
"""
ARGOS ArgosHardwareGuard v2 — улучшенная версия с фиксами багов.

БАГФИКСЫ относительно v1:
1. ✅ self.gpu_emergency → self.gpu_temp_emergency (опечатка в строке f-string)
2. ✅ Возврат metrics None при сбое (не 0,0)
3. ✅ current_route защищён threading.Lock (thread-safety)
4. ✅ VRAM critical добавляет warning (раньше только vram_warn)
5. ✅ cooldown проверяется только если is_overheated (state consistency)
6. ✅ Используется subprocess.run вместо check_output (security + error handling)
7. ✅ nvidia-smi timeout 5s (защита от зависания)
8. ✅ __init__ → __init__ (опечатка)
9. ✅ _get_gpu_metrics_smi() возвращает Optional[Tuple]
10. ✅ type hints для всех методов
"""
import os
import sys
import time
import logging
import threading
import subprocess
from typing import Optional, Callable, Tuple
from enum import Enum

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [HW_GUARD] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TargetGPU(Enum):
    PRIMARY_V100   = "V100_PRIMARY"
    BACKUP_RX580   = "RX580_RESERVE"
    EMERGENCY_STOP = "STOPPED"


class ArgosHardwareGuard:
    def __init__(
        self,
        gpu_index: int = 0,
        gpu_temp_warn: int = 83,
        gpu_temp_critical: int = 85,
        gpu_temp_emergency: int = 88,
        vram_warn_mib: int = 13500,
        vram_critical_mib: int = 15500,
        cooldown_temp: int = 75,
        cooldown_seconds: int = 30,
        nvidia_smi_timeout: int = 5,
    ):
        """
        :param gpu_index:          Индекс целевой карты NVIDIA.
        :param gpu_temp_warn:      Порог предупреждения.
        :param gpu_temp_critical:  Порог переключения на RX580.
        :param gpu_temp_emergency: Порог SIGKILL процесса.
        :param vram_warn_mib:      Лимит заполнения видеопамяти (warning).
        :param vram_critical_mib:  Критический лимит VRAM (alert + suggest restart).
        :param cooldown_temp:      Температура возврата на V100.
        :param cooldown_seconds:   Минимальное время в cooldown перед возвратом.
        :param nvidia_smi_timeout: Timeout для subprocess nvidia-smi.
        """
        self.gpu_index = gpu_index
        self.gpu_temp_warn = gpu_temp_warn
        self.gpu_temp_critical = gpu_temp_critical
        self.gpu_temp_emergency = gpu_temp_emergency
        self.vram_warn_mib = vram_warn_mib
        self.vram_critical_mib = vram_critical_mib
        self.cooldown_temp = cooldown_temp
        self.cooldown_seconds = cooldown_seconds
        self.nvidia_smi_timeout = nvidia_smi_timeout

        # ✅ FIX 3: thread-safe state
        self._lock = threading.RLock()
        self._current_route = TargetGPU.PRIMARY_V100
        self._is_overheated = False
        self._cooldown_started_at: Optional[float] = None
        self._consecutive_read_failures = 0

        # Пытаемся инициализировать NVML
        try:
            from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex
            nvmlInit()
            self.nvml_handle = nvmlDeviceGetHandleByIndex(gpu_index)
            self.use_nvml = True
            logger.info("NVML успешно инициализирована. Прямой опрос GPU активен.")
        except ImportError:
            self.use_nvml = False
            self.nvml_handle = None
            logger.warning("pynvml не найден. Fallback на nvidia-smi.")

    # ===== Public properties (thread-safe getters) =====

    @property
    def current_route(self) -> TargetGPU:
        with self._lock:
            return self._current_route

    @property
    def is_overheated(self) -> bool:
        with self._lock:
            return self._is_overheated

    @property
    def consecutive_read_failures(self) -> int:
        with self._lock:
            return self._consecutive_read_failures

    # ===== GPU metrics =====

    def _get_gpu_metrics_smi(self) -> Optional[Tuple[int, int]]:
        """✅ FIX 9: возвращает None при сбое, не (0,0)."""
        try:
            cmd = [
                "nvidia-smi",
                f"--query-gpu=temperature.gpu,memory.used",
                "--format=csv,noheader,nounits",
                "-i", str(self.gpu_index),
            ]
            # ✅ FIX 6,7: subprocess.run + timeout + shell=False (security)
            result = subprocess.run(
                cmd, capture_output=True, text=True,
                timeout=self.nvidia_smi_timeout, shell=False
            )
            if result.returncode != 0:
                logger.error(f"nvidia-smi failed (rc={result.returncode}): {result.stderr[:200]}")
                return None
            output = result.stdout.strip()
            if not output:
                return None
            parts = output.split(',')
            if len(parts) != 2:
                logger.error(f"nvidia-smi вернул неожиданный формат: {output[:100]}")
                return None
            return int(parts[0].strip()), int(parts[1].strip())
        except subprocess.TimeoutExpired:
            logger.error(f"nvidia-smi timeout ({self.nvidia_smi_timeout}s)")
            return None
        except (ValueError, IndexError) as e:
            logger.error(f"Ошибка парсинга nvidia-smi: {e}")
            return None
        except Exception as e:
            logger.error(f"Неожиданная ошибка nvidia-smi: {e}")
            return None

    def get_metrics(self) -> Optional[Tuple[int, int]]:
        """✅ FIX 2: возвращает None при сбое, не (0,0)."""
        if self.use_nvml and self.nvml_handle:
            try:
                from pynvml import (
                    nvmlDeviceGetTemperature, NVML_TEMPERATURE_GPU,
                    nvmlDeviceGetMemoryInfo,
                )
                temp = nvmlDeviceGetTemperature(self.nvml_handle, NVML_TEMPERATURE_GPU)
                mem_info = nvmlDeviceGetMemoryInfo(self.nvml_handle)
                vram_used = mem_info.used // (1024 ** 2)
                with self._lock:
                    self._consecutive_read_failures = 0
                return temp, vram_used
            except Exception as e:
                logger.error(f"Ошибка NVML API: {e}. Fallback на nvidia-smi.")
                self.use_nvml = False

        result = self._get_gpu_metrics_smi()
        with self._lock:
            if result is None:
                self._consecutive_read_failures += 1
                if self._consecutive_read_failures > 10:
                    logger.critical(
                        f"GPU metrics {self._consecutive_read_failures} раз подряд не читаются! "
                        "Возможна аппаратная проблема."
                    )
            else:
                self._consecutive_read_failures = 0
        return result

    # ===== Main monitor loop =====

    def monitor_tick(self, inference_pid_provider: Callable[[], Optional[int]]) -> TargetGPU:
        """
        Один такт проверки состояния железа.
        ✅ FIX 1: исправлена опечатка self.gpu_emergency
        ✅ FIX 3: state под lock
        ✅ FIX 4: vram_critical алерт
        """
        metrics = self.get_metrics()
        if metrics is None:
            # ✅ FIX 2: было if temp==0 and vram==0 → теперь None check
            logger.error("Не удалось прочитать метрики GPU. Маршрут без изменений.")
            return self.current_route

        temp, vram = metrics
        logger.debug(f"Метрики GPU: {temp}°C, VRAM: {vram} MiB. "
                     f"Текущий: {self.current_route.value}")

        # 1. EMERGENCY — SIGKILL процесса
        if temp >= self.gpu_temp_emergency:
            # ✅ FIX 1: правильное имя поля
            logger.critical(
                f"АВАРИЯ! Температура GPU {temp}°C >= {self.gpu_temp_emergency}°C! "
                f"Спасение железа."
            )
            pid = inference_pid_provider()
            if pid:
                try:
                    os.kill(pid, 9)
                    logger.critical(f"Процесс инференса [{pid}] принудительно убит по перегреву.")
                except ProcessLookupError:
                    logger.warning(f"Процесс [{pid}] уже завершён.")
                except PermissionError:
                    logger.error(f"Нет прав на kill [{pid}].")
            with self._lock:
                self._current_route = TargetGPU.EMERGENCY_STOP
            return self.current_route

        # 2. CRITICAL — переключение на RX580
        if temp >= self.gpu_temp_critical:
            with self._lock:
                if not self._is_overheated:
                    logger.warning(
                        f"КРИТИЧЕСКИЙ НАГРЕВ! {temp}°C >= {self.gpu_temp_critical}°C. "
                        f"Сброс нагрузки на RX580."
                    )
                    self._is_overheated = True
                    self._cooldown_started_at = time.time()
                    self._current_route = TargetGPU.BACKUP_RX580
                    # SIGTERM (мягкая остановка) на текущий инференс
                    pid = inference_pid_provider()
                    if pid:
                        try:
                            os.kill(pid, 15)
                            logger.warning(f"SIGTERM процессу [{pid}] для разгрузки V100.")
                        except ProcessLookupError:
                            pass
            return self.current_route

        # 3. HYSTERESIS — выход из зоны перегрева
        with self._lock:
            if self._is_overheated:
                if temp <= self.cooldown_temp:
                    # ✅ NEW: добавил проверку cooldown_seconds
                    elapsed = time.time() - (self._cooldown_started_at or 0)
                    if elapsed < self.cooldown_seconds:
                        logger.info(
                            f"GPU {temp}°C <= cooldown {self.cooldown_temp}°C, "
                            f"но прошло только {elapsed:.1f}s (<{self.cooldown_seconds}s). "
                            "Удерживаем на RX580."
                        )
                        return self._current_route
                    logger.info(
                        f"GPU охладился до {temp}°C за {elapsed:.1f}s. "
                        "Возврат на V100."
                    )
                    self._is_overheated = False
                    self._cooldown_started_at = None
                    self._current_route = TargetGPU.PRIMARY_V100
                else:
                    # Карта в cooldown, удерживаем на резерве
                    self._current_route = TargetGPU.BACKUP_RX580
                return self._current_route

        # 4. WARNINGS
        if temp >= self.gpu_temp_warn:
            logger.warning(
                f"Температура растёт: {temp}°C (предел: {self.gpu_temp_critical}°C)"
            )
        if vram >= self.vram_critical_mib:
            # ✅ FIX 4: vram critical
            logger.critical(
                f"VRAM {vram} МБ >= {self.vram_critical_mib} МБ! "
                "Возможен OOM. Рекомендуется перезапуск инференса."
            )
        elif vram >= self.vram_warn_mib:
            logger.warning(f"VRAM {vram} МБ (warn: {self.vram_warn_mib} МБ)")

        with self._lock:
            self._current_route = TargetGPU.PRIMARY_V100
        return self._current_route


def start_hardware_guard_daemon(
    guard: ArgosHardwareGuard,
    pid_provider: Callable[[], Optional[int]],
    on_route_change: Callable[[TargetGPU], None],
    interval_seconds: int = 5,
    stop_event: Optional[threading.Event] = None,
) -> Tuple[threading.Thread, threading.Event]:
    """Запускает фоновый цикл мониторинга."""
    stop_event = stop_event or threading.Event()

    def _worker():
        logger.info("Фоновый демон ArgosHardwareGuard v2 инициализирован.")
        last_route = guard.current_route

        while not stop_event.is_set():
            try:
                new_route = guard.monitor_tick(pid_provider)
                if new_route != last_route:
                    logger.info(
                        f"ИЗМЕНЕНИЕ МАРШРУТА: {last_route.value} -> {new_route.value}"
                    )
                    try:
                        on_route_change(new_route)
                    except Exception as e:
                        logger.error(f"Ошибка в on_route_change: {e}")
                    last_route = new_route
            except Exception as e:
                logger.error(f"Сбой в цикле монитора: {e}", exc_info=True)

            if stop_event.wait(timeout=interval_seconds):
                break
        logger.info("Демон ArgosHardwareGuard v2 остановлен.")

    t = threading.Thread(target=_worker, daemon=True, name="ArgosHardwareGuardThread")
    t.start()
    return t, stop_event
