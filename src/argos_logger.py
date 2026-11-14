"""Minimal restoration of the missing src/argos_logger module.

The original file is absent from the repository, but src/cognitive_memory.py
and other runtime components import ``get_logger`` from it.  This shim keeps
the public contract (``get_logger(name)``, ``ArgosLogger``) using the standard
library so the original ARGOS components run unmodified.  It is logging only:
no behaviour of the caller is emulated.
"""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

_LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
_configured = False


def _configure_root() -> None:
    global _configured
    if _configured:
        return
    log_dir = Path(os.getenv("ARGOS_LOG_DIR", "logs"))
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        handler: logging.Handler = logging.FileHandler(log_dir / "argos.log")
    except OSError:
        handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT))
    root = logging.getLogger()
    root.addHandler(handler)
    level = os.getenv("ARGOS_LOG_LEVEL", "INFO").upper()
    root.setLevel(getattr(logging, level, logging.INFO))
    _configured = True


def get_logger(name: str = "argos", level: int | None = None) -> logging.Logger:
    _configure_root()
    logger = logging.getLogger(name)
    if level is not None:
        logger.setLevel(level)
    return logger


class ArgosLogger(logging.Logger):
    """Backwards-compatible alias used by some ARGOS call sites."""


def log_event(component: str, message: str, level: int = logging.INFO) -> None:
    get_logger(component).log(level, message)
