from __future__ import annotations

import hmac
import secrets
import time
from dataclasses import dataclass
from enum import StrEnum
from typing import Callable


class LiveLoginState(StrEnum):
    WAITING_FOR_HUMAN = "waiting_for_human"
    HUMAN_LOGIN_IN_PROGRESS = "human_login_in_progress"
    DRAFT_READY = "draft_ready"
    EXPIRED = "expired"


@dataclass(slots=True)
class LiveLoginSession:
    token: str
    issued_at: float
    expires_at: float
    state: LiveLoginState


class LiveLoginController:
    def __init__(self, ttl_seconds: int = 600, clock: Callable[[], float] = time.time):
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        self.ttl_seconds = ttl_seconds
        self._clock = clock
        self._sessions: dict[str, LiveLoginSession] = {}

    def start(self) -> LiveLoginSession:
        now = self._clock()
        session = LiveLoginSession(
            token=secrets.token_urlsafe(32),
            issued_at=now,
            expires_at=now + self.ttl_seconds,
            state=LiveLoginState.WAITING_FOR_HUMAN,
        )
        self._sessions[session.token] = session
        return session

    def _find_key(self, token: str) -> str | None:
        for candidate in self._sessions:
            if hmac.compare_digest(candidate, token):
                return candidate
        return None

    def get(self, token: str) -> LiveLoginSession | None:
        key = self._find_key(token)
        if key is None:
            return None
        session = self._sessions[key]
        if self._clock() > session.expires_at:
            session.state = LiveLoginState.EXPIRED
            del self._sessions[key]
            return None
        return session

    def mark_in_progress(self, token: str) -> LiveLoginSession:
        session = self.get(token)
        if session is None:
            raise KeyError("live login session not found or expired")
        session.state = LiveLoginState.HUMAN_LOGIN_IN_PROGRESS
        return session

    def mark_ready(self, token: str) -> LiveLoginSession:
        session = self.get(token)
        if session is None:
            raise KeyError("live login session not found or expired")
        session.state = LiveLoginState.DRAFT_READY
        return session

    def invalidate(self, token: str) -> None:
        key = self._find_key(token)
        if key is not None:
            del self._sessions[key]
