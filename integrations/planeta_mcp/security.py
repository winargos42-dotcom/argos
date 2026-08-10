from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time
from dataclasses import dataclass
from typing import Callable

from .models import CampaignPayload


class ApprovalError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class ApprovalRequest:
    request_id: str
    campaign_digest: str
    issued_at: float
    expires_at: float


@dataclass(frozen=True, slots=True)
class ApprovalChallenge:
    request_id: str
    campaign_digest: str
    issued_at: float
    expires_at: float
    csrf_token: str
    approved_at: float | None


@dataclass(slots=True)
class _ApprovalRecord:
    request_hash: str
    campaign_digest: str
    issued_at: float
    expires_at: float
    approved_at: float | None = None
    used: bool = False


def campaign_digest(payload: CampaignPayload) -> str:
    canonical = json.dumps(
        payload.canonical_dict(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


class ApprovalGate:
    """One-time submit gate that requires a separate human confirmation step.

    MCP callers may create an approval *request*, but only the non-MCP approval
    page can obtain the CSRF challenge and confirm that request. Submission is
    rejected until confirmation has happened, and every request is single-use.
    """

    def __init__(
        self,
        secret: bytes | str,
        ttl_seconds: int = 300,
        clock: Callable[[], float] = time.time,
    ):
        if isinstance(secret, str):
            secret = secret.encode("utf-8")
        if not secret:
            raise ValueError("Approval secret must not be empty")
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        self._secret = secret
        self._ttl_seconds = ttl_seconds
        self._clock = clock
        self._records: dict[str, _ApprovalRecord] = {}

    @staticmethod
    def _b64(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")

    @staticmethod
    def _request_hash(request_id: str) -> str:
        return hashlib.sha256(request_id.encode("utf-8")).hexdigest()

    def _csrf_token(self, request_id: str, record: _ApprovalRecord) -> str:
        message = (
            f"human-confirm|{request_id}|{record.campaign_digest}|{record.expires_at:.6f}"
        ).encode("utf-8")
        return self._b64(hmac.new(self._secret, message, hashlib.sha256).digest())

    def _get_record(self, request_id: str) -> _ApprovalRecord:
        request_hash = self._request_hash(request_id)
        record = self._records.get(request_hash)
        if record is None:
            raise ApprovalError("Unknown approval request")
        if record.used:
            raise ApprovalError("Approval request has already been used")
        if float(self._clock()) > record.expires_at:
            record.used = True
            raise ApprovalError("Approval request has expired")
        return record

    def request(self, payload: CampaignPayload) -> ApprovalRequest:
        digest = campaign_digest(payload)
        issued_at = float(self._clock())
        expires_at = issued_at + self._ttl_seconds
        request_id = secrets.token_urlsafe(32)
        request_hash = self._request_hash(request_id)
        self._records[request_hash] = _ApprovalRecord(
            request_hash=request_hash,
            campaign_digest=digest,
            issued_at=issued_at,
            expires_at=expires_at,
        )
        return ApprovalRequest(
            request_id=request_id,
            campaign_digest=digest,
            issued_at=issued_at,
            expires_at=expires_at,
        )

    def challenge(self, request_id: str) -> ApprovalChallenge:
        record = self._get_record(request_id)
        return ApprovalChallenge(
            request_id=request_id,
            campaign_digest=record.campaign_digest,
            issued_at=record.issued_at,
            expires_at=record.expires_at,
            csrf_token=self._csrf_token(request_id, record),
            approved_at=record.approved_at,
        )

    def confirm(self, request_id: str, csrf_token: str) -> ApprovalChallenge:
        record = self._get_record(request_id)
        expected = self._csrf_token(request_id, record)
        if not hmac.compare_digest(csrf_token, expected):
            raise ApprovalError("Invalid human confirmation token")
        if record.approved_at is None:
            record.approved_at = float(self._clock())
        return self.challenge(request_id)

    def consume(self, request_id: str, payload: CampaignPayload) -> ApprovalRequest:
        record = self._get_record(request_id)
        if record.approved_at is None:
            raise ApprovalError("Approval request requires human confirmation")
        digest = campaign_digest(payload)
        if digest != record.campaign_digest:
            record.used = True
            raise ApprovalError("Approval request does not match current campaign")
        record.used = True
        return ApprovalRequest(
            request_id=request_id,
            campaign_digest=record.campaign_digest,
            issued_at=record.issued_at,
            expires_at=record.expires_at,
        )

    def invalidate_all(self) -> None:
        self._records.clear()
