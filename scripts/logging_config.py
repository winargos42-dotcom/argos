"""
ARGOS Logging Config — JSON-only structlog, один раз на процесс.
Реализован по рекомендациям @claude_gidbot.
"""
import logging
import structlog
import sys


def configure_logging(level: int = logging.INFO) -> None:
    """Strict JSON logging. No text handlers output."""
    # Защита от повторного вызова
    if getattr(sys, "_LOGGING_CONFIGURED", False):
        return
    sys._LOGGING_CONFIGURED = True

    # Убираем все handlers чтобы не получить двойные JSON/текст
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
    root.handlers.clear()
    root.propagate = False
    root.setLevel(level)

    # JSON handler через structlog
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    root.addHandler(handler)

    # Structlog pipeline
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.ExceptionRenderer(),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str):
    return structlog.get_logger(name)


def log_healing_event(entity: str, action: str, result: str, **kwargs):
    """Логируем auto-healing событие в JSON формате."""
    log = get_logger("argos.healing")
    log.info("healing_event",
             entity=entity,
             action=action,
             result=result,
             **kwargs)


def log_latency(entity: str, provider: str, api_ms: int, outcome: str, **kwargs):
    """Логируем задержки провайдера в JSON формате."""
    log = get_logger("argos.latency")
    log.info("provider_latency",
             entity=entity,
             provider=provider,
             api_ms=api_ms,
             outcome=outcome,
             **kwargs)
