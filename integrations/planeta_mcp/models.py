from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


class Reward(BaseModel):
    title: str
    amount: int = Field(gt=0)
    description: str
    physical: bool = False


class BudgetItem(BaseModel):
    title: str
    amount: int = Field(gt=0)


class ValidationReport(BaseModel):
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    error_fields: list[str] = Field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.errors


class CampaignPayload(BaseModel):
    id: str = "argos-reboot"
    title: str
    target_amount: int = Field(gt=0)
    currency: Literal["RUB"] = "RUB"
    end_date: date | None = None
    region: str | None = None
    summary: str
    story: str
    direct_support_url: HttpUrl | None = None
    cover_image_path: str | None = None
    main_image_path: str | None = None
    evidence_links: list[HttpUrl] = Field(default_factory=list)
    rewards: list[Reward] = Field(default_factory=list)
    budget: list[BudgetItem] = Field(default_factory=list)

    def canonical_dict(self) -> dict[str, object]:
        return self.model_dump(mode="json", exclude_none=True)

    def validate_for_planeta(self) -> ValidationReport:
        errors: list[str] = []
        warnings: list[str] = []
        fields: list[str] = []

        def require_text(field_name: str, value: str) -> None:
            if not value.strip():
                errors.append(f"{field_name} must not be empty")
                fields.append(field_name)

        require_text("title", self.title)
        require_text("summary", self.summary)
        require_text("story", self.story)

        if self.end_date is None:
            errors.append("end_date is required")
            fields.append("end_date")

        if not (self.cover_image_path or "").strip():
            errors.append("cover_image_path must not be empty")
            fields.append("cover_image_path")
        if not (self.main_image_path or "").strip():
            errors.append("main_image_path must not be empty")
            fields.append("main_image_path")

        if not self.evidence_links:
            errors.append("At least one evidence link is required")
            fields.append("evidence_links")
        if not self.rewards:
            errors.append("At least one reward is required")
            fields.append("rewards")
        if not self.budget:
            errors.append("At least one budget item is required")
            fields.append("budget")

        budget_total = sum(item.amount for item in self.budget)
        if self.budget and budget_total != self.target_amount:
            warnings.append(
                f"Budget total {budget_total} RUB differs from target {self.target_amount} RUB"
            )
        if any(reward.physical for reward in self.rewards):
            warnings.append("Physical rewards create shipping obligations")

        return ValidationReport(
            errors=errors,
            warnings=warnings,
            error_fields=list(dict.fromkeys(fields)),
        )
