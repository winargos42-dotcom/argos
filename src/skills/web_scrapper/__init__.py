"""Навык web_scrapper.

Реализация восстановлена из репозитория winargos42-dotcom/argos-1 после пожара
03.08.2026. Реэкспорт нужен, потому что src/core.py импортирует класс из пакета:
    from src.skills.web_scrapper import ArgosScrapper
"""
from .skill import ArgosScrapper, execute

__all__ = ["ArgosScrapper", "execute"]
