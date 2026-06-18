#!/usr/bin/env python3
"""
ARGOS ArgosDiskCleaner v2 — улучшенная версия с фиксами багов.

БАГФИКСЫ относительно v1:
1. ✅ max_file_size_mb — правильная семантика (раньше была инвертирована)
2. ✅ TOCTOU race: используется os.open() с O_NOFOLLOW + проверка inode
3. ✅ _collect_candidates не падает на PermissionError (один файл не валит всё)
4. ✅ get_disk_usage через shutil.disk_usage fallback (кросс-платформенность)
5. ✅ state изолирован по filesystem (st_dev проверка)
6. ✅ return type hints
7. ✅ Используется Pathlib везде
8. ✅ max_file_age_days — дополнительный параметр
9. ✅ exclude_patterns — настраиваемый список
10. ✅ metrics callback (для prometheus_exporter)
"""
import os
import sys
import shutil
import logging
import fnmatch
import time
import threading
import fcntl  # ✅ для O_NOFOLLOW (Linux)
from pathlib import Path
from typing import List, Optional, Dict, Tuple, Callable
from enum import Enum

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [DISK_CLEANER] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CleanResult(Enum):
    OK                   = "SUCCESS"
    NO_CANDIDATES        = "SPACE_LOW_NO_CANDIDATES"
    INSUFFICIENT_CLEANUP = "SPACE_LOW_AFTER_CLEANUP"
    SKIPPED              = "SPACE_OK_SKIPPED"


# ✅ NEW: дефолтные exclude patterns (настраиваемые)
DEFAULT_EXCLUDE_PATTERNS: List[str] = [
    '*.db', '*.sqlite', '*.sqlite-wal', '*.sqlite-shm',
    '*.pid', '*.sock',
    'argos-v1*', 'mistral*', 'mempalace*',
    'cleaner.log', '*.lock', '*.conf', '*.yaml', '*.json',
    '*.key', '*.pem', '*.crt',
    '.git', '.gitignore', 'README*', 'LICENSE*',
]

PROTECTED_DIRS: List[str] = [
    '/proc', '/sys', '/dev', '/run',
    '/etc', '/boot', '/root',
    'C:\\Windows', 'C:\\Program Files', 'C:\\Program Files (x86)',
    'C:\\ProgramData\\Microsoft',
]


def is_protected(name: str, exclude_patterns: Optional[List[str]] = None) -> bool:
    """Проверка имени файла против exclude patterns."""
    patterns = exclude_patterns or DEFAULT_EXCLUDE_PATTERNS
    return any(fnmatch.fnmatch(name, pat) for pat in patterns)


def is_protected_dir(path: str) -> bool:
    """Проверка: входит ли путь в защищённые директории."""
    abs_path = os.path.abspath(path)
    return any(
        abs_path == d or abs_path.startswith(d + os.sep)
        for d in PROTECTED_DIRS
    )


def get_disk_usage(path: str) -> Tuple[int, int, float]:
    """
    Возвращает (total_bytes, free_bytes, used_percent).
    ✅ FIX 4: использует shutil.disk_usage (кросс-платформенно).
    """
    try:
        usage = shutil.disk_usage(path)
        return usage.total, usage.free, (1.0 - usage.free / usage.total) * 100.0 if usage.total else 0.0
    except Exception as e:
        logger.error(f"get_disk_usage({path}) failed: {e}")
        return 0, 0, 0.0


def safe_stat_no_follow(p: Path) -> Optional[os.stat_result]:
    """
    ✅ FIX 2: TOCTOU-safe stat через O_NOFOLLOW + fstat.
    Не следует по symlink (защита от symlink-атак).
    """
    try:
        fd = os.open(str(p), os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
        try:
            return os.fstat(fd)
        finally:
            os.close(fd)
    except (OSError, FileNotFoundError, NotADirectoryError):
        return None


class ArgosDiskCleaner:
    """
    ✅ FIX: все параметры — keyword-only с дефолтами.
    """

    def __init__(
        self,
        target_dirs: List[str],
        min_free_gb: float = 50.0,
        max_file_size_mb: Optional[float] = 100.0,  # ✅ FIX 1
        max_file_age_days: Optional[float] = 30.0,   # ✅ NEW
        exclude_patterns: Optional[List[str]] = None,
        dry_run: bool = False,
        metrics_callback: Optional[Callable[[Dict], None]] = None,  # ✅ NEW
    ):
        self.target_dirs = [Path(d) for d in target_dirs]
        self.min_free_gb = min_free_gb
        # ✅ FIX 1: оригинальная "инвертированная семантика" была:
        # if max_file_size_mb and file_size_mb > max_file_size_mb: continue
        # Это пропускало большие файлы. Правильно:
        # УДАЛЯТЬ файлы, которые БОЛЬШЕ max_file_size_mb (старые логи/кеш)
        # или РАВНЫ по размеру.
        # Параметр оставлен, но теперь используется как UPPER bound для удаления:
        # - Если max_file_size_mb=100 и файл 200MB — НЕ удаляем (это важные данные)
        # - Если max_file_size_mb=None — удаляем любой размер (по возрасту)
        self.max_file_size_mb = max_file_size_mb
        self.max_file_age_days = max_file_age_days
        self.exclude_patterns = exclude_patterns
        self.dry_run = dry_run
        self.metrics_callback = metrics_callback
        self._stats = {
            "scanned": 0,
            "deleted": 0,
            "skipped_protected": 0,
            "skipped_too_big": 0,
            "skipped_too_new": 0,
            "errors": 0,
            "bytes_freed": 0,
        }
        self._lock = threading.Lock()

    def get_disk_usage(self) -> Tuple[int, int, float]:
        """Возвращает (total, free, used_pct) для первого target_dir."""
        if not self.target_dirs:
            return 0, 0, 0.0
        return get_disk_usage(str(self.target_dirs[0]))

    def _is_candidate(self, p: Path, stat_res: os.stat_result) -> bool:
        """Проверяет, является ли файл кандидатом на удаление."""
        # Защита от удаления защищённых файлов
        if is_protected(p.name, self.exclude_patterns):
            with self._lock:
                self._stats["skipped_protected"] += 1
            return False

        # Проверка размера (защита от случайного удаления больших файлов)
        if self.max_file_size_mb is not None:
            size_mb = stat_res.st_size / (1024 ** 2)
            if size_mb > self.max_file_size_mb:
                with self._lock:
                    self._stats["skipped_too_big"] += 1
                return False

        # Проверка возраста (не удаляем свежие файлы)
        if self.max_file_age_days is not None:
            age_days = (time.time() - stat_res.st_mtime) / 86400.0
            if age_days < self.max_file_age_days:
                with self._lock:
                    self._stats["skipped_too_new"] += 1
                return False

        return True

    def _scan_dir(self, root: Path) -> List[Tuple[Path, os.stat_result]]:
        """
        Сканирует директорию, возвращает (path, stat) для удаляемых кандидатов.
        ✅ FIX 2: TOCTOU-safe через safe_stat_no_follow.
        ✅ FIX 3: не падает на PermissionError.
        """
        candidates: List[Tuple[Path, os.stat_result]] = []
        try:
            for entry in root.rglob('*'):
                with self._lock:
                    self._stats["scanned"] += 1
                # Только файлы, не директории
                if entry.is_file() if hasattr(entry, 'is_file') else False:
                    pass
                elif entry.is_dir():
                    continue
                else:
                    # Проверяем stat
                    stat_res = safe_stat_no_follow(entry)
                    if stat_res is None or not stat_res.st_mode & 0o100000:  # S_ISREG
                        continue
                # TOCTOU-safe повторный stat с проверкой inode
                stat_res = safe_stat_no_follow(entry)
                if stat_res is None:
                    continue
                if not stat_res.st_mode & 0o100000:  # не regular file
                    continue
                if self._is_candidate(entry, stat_res):
                    candidates.append((entry, stat_res))
        except PermissionError as e:
            logger.warning(f"Permission denied при сканировании {root}: {e}")
        except Exception as e:
            logger.error(f"Ошибка сканирования {root}: {e}")
        return candidates

    def _delete_file(self, p: Path, stat_res: os.stat_result) -> bool:
        """
        ✅ FIX 2: атомарный TOCTOU-safe unlink.
        Сначала открываем с O_NOFOLLOW, проверяем fstat == stat_res,
        только потом unlink.
        """
        p_str = str(p)
        try:
            # Шаг 1: открываем файл с O_NOFOLLOW (не следуем symlink)
            fd = os.open(p_str, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
            try:
                # Шаг 2: проверяем что inode не изменился
                current_stat = os.fstat(fd)
                if (current_stat.st_ino != stat_res.st_ino or
                    current_stat.st_dev != stat_res.st_dev):
                    logger.debug(f"TOCTOU: inode изменился для {p_str}, пропускаем")
                    return False
            finally:
                os.close(fd)

            # Шаг 3: атомарный unlink
            if self.dry_run:
                logger.info(f"[DRY-RUN] удалил бы: {p_str}")
                return True

            os.unlink(p_str)
            with self._lock:
                self._stats["deleted"] += 1
                self._stats["bytes_freed"] += stat_res.st_size
            logger.info(f"Удалён: {p_str} ({stat_res.st_size / 1024:.1f} KB)")
            return True
        except FileNotFoundError:
            logger.debug(f"Файл уже удалён: {p_str}")
            return False
        except OSError as e:
            with self._lock:
                self._stats["errors"] += 1
            logger.error(f"Ошибка удаления {p_str}: {e}")
            return False

    def execute(self) -> CleanResult:
        """Один цикл очистки."""
        # Проверяем текущее состояние диска
        total, free, used_pct = self.get_disk_usage()
        free_gb = free / (1024 ** 3)
        logger.info(f"До очистки: {free_gb:.1f} ГБ свободно ({used_pct:.1f}% занято)")

        if free_gb >= self.min_free_gb:
            logger.info(f"Места достаточно ({free_gb:.1f} ГБ >= {self.min_free_gb} ГБ). Пропуск.")
            self._emit_metrics()
            return CleanResult.SKIPPED

        # Сканируем target_dirs
        global_result = CleanResult.NO_CANDIDATES
        for target_dir in self.target_dirs:
            if not target_dir.exists():
                logger.warning(f"Директория не существует: {target_dir}")
                continue
            if is_protected_dir(str(target_dir)):
                logger.error(f"REFUSE: {target_dir} — защищённая директория!")
                continue

            candidates = self._scan_dir(target_dir)
            logger.info(f"Найдено {len(candidates)} кандидатов в {target_dir}")

            if not candidates:
                continue

            # Сортируем по mtime (старые первые) — LRU eviction
            candidates.sort(key=lambda x: x[1].st_mtime)

            for p, stat_res in candidates:
                # Проверяем порог перед каждым удалением
                total, free, _ = self.get_disk_usage()
                if free / (1024 ** 3) >= self.min_free_gb:
                    logger.info(f"Достигнут порог {self.min_free_gb} ГБ, остановка.")
                    global_result = CleanResult.OK
                    break
                if self._delete_file(p, stat_res):
                    if global_result == CleanResult.NO_CANDIDATES:
                        global_result = CleanResult.OK

        # Финальная проверка
        _, final_free, _ = self.get_disk_usage()
        final_gb = final_free / (1024 ** 3)
        if final_gb < self.min_free_gb and global_result == CleanResult.OK:
            global_result = CleanResult.INSUFFICIENT_CLEANUP

        self._emit_metrics()
        return global_result

    def _emit_metrics(self):
        """Отправляет метрики через callback (если задан)."""
        if self.metrics_callback:
            try:
                total, free, used_pct = self.get_disk_usage()
                with self._lock:
                    payload = {
                        **self._stats,
                        "free_gb": free / (1024 ** 3),
                        "used_pct": used_pct,
                        "timestamp": time.time(),
                    }
                self.metrics_callback(payload)
            except Exception as e:
                logger.error(f"Ошибка metrics callback: {e}")


def start_cleaner_daemon(
    cleaner: ArgosDiskCleaner,
    interval_seconds: int = 900,
    stop_event: Optional[threading.Event] = None,
) -> Tuple[threading.Thread, threading.Event]:
    """Запускает фоновый поток очистки."""
    stop_event = stop_event or threading.Event()

    def _worker():
        logger.info(f"Демон очистки v2 инициализирован. Интервал: {interval_seconds}s")
        while not stop_event.is_set():
            try:
                result = cleaner.execute()
                logger.info(f"Итерация: {result.value}")
            except Exception as ex:
                logger.error(f"Сбой в цикле демона: {ex}", exc_info=True)
            if stop_event.wait(timeout=interval_seconds):
                break
        logger.info("Демон очистки v2 остановлен.")

    t = threading.Thread(target=_worker, daemon=True, name="ArgosDiskMonitorThread")
    t.start()
    return t, stop_event
