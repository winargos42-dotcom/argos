from __future__ import annotations

from .models import BudgetItem, CampaignPayload, Reward


DEFAULT_TITLE = "ARGOS REBOOT — восстановление независимой AI/FPGA-системы"


def default_argos_reboot_campaign() -> CampaignPayload:
    story = """## Что сохранилось и можно проверить публично

После потери локальной вычислительной среды сохранились публичные исходники ARGOS, история разработки, модели и датасеты. Эти материалы являются проверяемой частью проекта и используются как база восстановления.

## Что известно со слов владельца

Часть более позднего локального состояния ARGOS существовала только на утраченной вычислительной среде. Такие сведения в кампании рассматриваются как свидетельство владельца и не выдаются за независимо подтверждённые факты.

## Что будет восстановлено

Stage 1 восстанавливает минимальный постоянно доступный ARGOS Core: серверную платформу, ECC-память, накопители и резервирование, GPU/FPGA-контур и инфраструктуру для памяти, API, P2P и агентов. Ход восстановления будет документироваться публично."""

    return CampaignPayload(
        id="argos-reboot",
        title=DEFAULT_TITLE,
        target_amount=200000,
        currency="RUB",
        summary=(
            "Восстановление ARGOS Universal OS после потери локальной вычислительной среды: "
            "сервер, хранение, резервирование и GPU/FPGA-инфраструктура."
        ),
        story=story,
        evidence_links=[
            "https://github.com/poilopr57-a11y/Argos",
            "https://github.com/winargos42-dotcom/argos",
            "https://huggingface.co/AvaSiG/argos-v1",
            "https://huggingface.co/datasets/AvaSiG/argos-canonical",
        ],
        rewards=[
            Reward(
                title="Спасибо за поддержку",
                amount=300,
                description="Имя или псевдоним в публичном списке благодарностей ARGOS REBOOT.",
                physical=False,
            ),
            Reward(
                title="Участник ARGOS REBOOT",
                amount=1000,
                description="Благодарность и доступ к сводному техническому отчёту восстановления.",
                physical=False,
            ),
            Reward(
                title="Расширенный технический отчёт",
                amount=3000,
                description="Расширенная версия отчёта с архитектурой, этапами и результатами проверки.",
                physical=False,
            ),
        ],
        budget=[
            BudgetItem(title="Серверная платформа, CPU и ECC-память", amount=85000),
            BudgetItem(title="GPU/FPGA и адаптеры", amount=65000),
            BudgetItem(title="Накопители и резервирование", amount=30000),
            BudgetItem(title="Питание, охлаждение, доставка и монтаж", amount=20000),
        ],
    )
