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
class ApprovalGrant:
    token: str
    campaign_digest: str
    issued_at: float
    expires_at: float


@dataclass(slots=True)
class _ApprovalRecord:
    token_hash: str
    campaign_digest: str
    issued_at: float
    expires_at: float
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
    def _token_hash(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def issue(self, payload: CampaignPayload) -> ApprovalGrant:
        digest = campaign_digest(payload)
        issued_at = float(self._clock())
        expires_at = issued_at + self._ttl_seconds
        nonce = secrets.token_urlsafe(24)
        message = f"{nonce}|{digest}|{expires_at:.6f}".encode("utf-8")
        signature = hmac.new(self._secret, message, hashlib.sha256).digest()
        token = f"{nonce}.{self._b64(signature)}"
        token_hash = self._token_hash(token)
        self._records[token_hash] = _ApprovalRecord(
            token_hash=token_hash,
            campaign_digest=digest,
            issued_at=issued_at,
            expires_at=expires_at,
            used=False,
        )
        return ApprovalGrant(
            token=token,
            campaign_digest=digest,
            issued_at=issued_at,
            expires_at=expires_at,
        )

    def consume(self, token: str, payload: CampaignPayload) -> ApprovalGrant:
        token_hash = self._token_hash(token)
        record = self._records.get(token_hash)
        if record is None:
            raise ApprovalError("Unknown approval token")
        if record.used:
            raise ApprovalError("Approval token has already been used")
        now = float(self._clock())
        if now > record.expires_at:
            record.used = True
            raise ApprovalError("Approval token has expired")
        digest = campaign_digest(payload)
        if digest != record.campaign_digest:
            raise ApprovalError("Approval token does not match current campaign")
        record.used = True
        return ApprovalGrant(
            token=token,
            campaign_digest=record.campaign_digest,
            issued_at=record.issued_at,
            expires_at=record.expires_at,
        )

    def invalidate_all(self) -> None:
        self._records.clear()
