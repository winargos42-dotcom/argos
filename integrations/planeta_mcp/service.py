from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Protocol

from .audit import AuditLogger
from .browser import BrowserResult
from .models import CampaignPayload, ValidationReport
from .security import ApprovalChallenge, ApprovalGate, ApprovalRequest
from .store import CampaignStore


class CampaignValidationError(ValueError):
    def __init__(self, errors: list[str]):
        super().__init__("; ".join(errors))
        self.errors = errors


class BrowserAdapter(Protocol):
    async def fill_draft(self, campaign: CampaignPayload) -> BrowserResult: ...
    async def fill_rewards(self, campaign: CampaignPayload) -> BrowserResult: ...
    async def read_draft(self) -> BrowserResult: ...
    async def read_rewards(self) -> BrowserResult: ...
    async def submit_for_moderation(self) -> BrowserResult: ...


class PlanetaCampaignService:
    def __init__(
        self,
        store: CampaignStore,
        browser: BrowserAdapter,
        approval_gate: ApprovalGate,
        audit: AuditLogger,
    ):
        self.store = store
        self.browser = browser
        self.approval_gate = approval_gate
        self.audit = audit
        self._last_sync_at: str | None = None
        self._last_browser_status: str | None = None

    async def campaign_status(self) -> dict[str, Any]:
        campaign = self.store.load()
        if campaign is None:
            return {
                "campaign_exists": False,
                "validation": None,
                "last_sync_at": self._last_sync_at,
                "last_browser_status": self._last_browser_status,
            }
        report = campaign.validate_for_planeta()
        return {
            "campaign_exists": True,
            "campaign_id": campaign.id,
            "title": campaign.title,
            "validation": report.model_dump(mode="json"),
            "last_sync_at": self._last_sync_at,
            "last_browser_status": self._last_browser_status,
        }

    async def campaign_preview(self) -> dict[str, Any]:
        campaign = self.store.load_required()
        return {
            "campaign": campaign.canonical_dict(),
            "validation": campaign.validate_for_planeta().model_dump(mode="json"),
        }

    async def validate_campaign(self) -> ValidationReport:
        return self.store.load_required().validate_for_planeta()

    async def prepare_campaign(self, payload: CampaignPayload | dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, CampaignPayload):
            payload = CampaignPayload.model_validate(payload)
        self.store.save(payload)
        self.approval_gate.invalidate_all()
        report = payload.validate_for_planeta()
        result = {
            "campaign_id": payload.id,
            "saved": True,
            "validation": report.model_dump(mode="json"),
        }
        self.audit.record("planeta_prepare_campaign", payload.id, "ok", result)
        return result

    async def fill_draft(self) -> BrowserResult:
        campaign = self.store.load_required()
        report = campaign.validate_for_planeta()
        if report.errors:
            result = BrowserResult(
                status="validation_failed",
                reason="; ".join(report.errors),
            )
            self.audit.record(
                "planeta_fill_draft", campaign.id, result.status, result.safe_dict()
            )
            return result

        draft_result = await self.browser.fill_draft(campaign)
        if draft_result.status != "ok":
            self._last_browser_status = draft_result.status
            self.audit.record(
                "planeta_fill_draft", campaign.id, draft_result.status, draft_result.safe_dict()
            )
            return draft_result

        rewards_result = await self.browser.fill_rewards(campaign)
        if rewards_result.status != "ok":
            self._last_browser_status = rewards_result.status
            self.audit.record(
                "planeta_fill_draft", campaign.id, rewards_result.status, rewards_result.safe_dict()
            )
            return rewards_result

        result = BrowserResult(
            status="ok",
            reason="draft fields and digital rewards filled and saved",
            draft_snapshot={**draft_result.draft_snapshot, **rewards_result.draft_snapshot},
        )
        self._last_browser_status = result.status
        self.audit.record("planeta_fill_draft", campaign.id, result.status, result.safe_dict())
        return result

    @staticmethod
    def _expected_rewards(campaign: CampaignPayload) -> list[dict[str, Any]]:
        return [
            {
                "title": reward.title,
                "amount": str(reward.amount),
                "description": reward.description,
                "physical": reward.physical,
            }
            for reward in campaign.rewards
        ]

    async def sync_draft(self) -> dict[str, Any]:
        campaign = self.store.load_required()
        result = await self.browser.read_draft()
        self._last_browser_status = result.status
        differences: dict[str, Any] = {}
        reason = result.reason
        final_status = result.status

        if result.status == "ok":
            expected = {
                "title": campaign.title,
                "target_amount": str(campaign.target_amount),
                "summary": campaign.summary,
                "story": campaign.story,
            }
            if "end_date" in result.draft_snapshot:
                expected["end_date"] = (
                    campaign.end_date.strftime("%d.%m.%Y")
                    if campaign.end_date
                    else None
                )
            if "cover_image" in result.draft_snapshot:
                expected["cover_image"] = (
                    campaign.cover_image_path.rsplit("/", 1)[-1]
                    if campaign.cover_image_path
                    else None
                )
            if "main_image" in result.draft_snapshot:
                expected["main_image"] = (
                    campaign.main_image_path.rsplit("/", 1)[-1]
                    if campaign.main_image_path
                    else None
                )
            for field, local_value in expected.items():
                remote_value = result.draft_snapshot.get(field)
                if remote_value != local_value:
                    differences[field] = {"local": local_value, "planeta": remote_value}

            rewards_result = await self.browser.read_rewards()
            final_status = rewards_result.status
            reason = rewards_result.reason if rewards_result.status != "ok" else result.reason
            self._last_browser_status = final_status
            if rewards_result.status == "ok":
                expected_rewards = self._expected_rewards(campaign)
                remote_rewards = rewards_result.draft_snapshot.get("rewards", [])
                if remote_rewards != expected_rewards:
                    differences["rewards"] = {
                        "local": expected_rewards,
                        "planeta": remote_rewards,
                    }
            if final_status == "ok":
                self._last_sync_at = datetime.now(timezone.utc).isoformat()

        payload = {
            "status": final_status,
            "reason": reason,
            "differences": differences,
            "last_sync_at": self._last_sync_at,
        }
        self.audit.record("planeta_sync_draft", campaign.id, final_status, payload)
        return payload

    async def request_submit_approval(self) -> ApprovalRequest:
        campaign = self.store.load_required()
        report = campaign.validate_for_planeta()
        if report.errors:
            raise CampaignValidationError(report.errors)
        request = self.approval_gate.request(campaign)
        self.audit.record(
            "planeta_request_submit_approval",
            campaign.id,
            "pending_human_confirmation",
            {
                "request_fingerprint": self.approval_gate.request_fingerprint(request.request_id),
                "campaign_digest": request.campaign_digest,
                "issued_at": request.issued_at,
                "expires_at": request.expires_at,
            },
        )
        return request

    def get_submit_approval_challenge(self, request_id: str) -> ApprovalChallenge:
        return self.approval_gate.challenge(request_id)

    def confirm_submit_approval(self, request_id: str, csrf_token: str) -> ApprovalChallenge:
        campaign = self.store.load_required()
        challenge = self.approval_gate.confirm(request_id, csrf_token)
        self.audit.record(
            "planeta_confirm_submit_approval",
            campaign.id,
            "human_confirmed",
            {
                "request_fingerprint": self.approval_gate.request_fingerprint(request_id),
                "campaign_digest": challenge.campaign_digest,
                "approved_at": challenge.approved_at,
                "expires_at": challenge.expires_at,
            },
        )
        return challenge

    async def submit_for_moderation(self, request_id: str) -> BrowserResult:
        campaign = self.store.load_required()
        report = campaign.validate_for_planeta()
        if report.errors:
            raise CampaignValidationError(report.errors)
        self.approval_gate.consume(request_id, campaign)
        result = await self.browser.submit_for_moderation()
        self._last_browser_status = result.status
        self.audit.record(
            "planeta_submit_for_moderation",
            campaign.id,
            result.status,
            result.safe_dict(),
        )
        return result
