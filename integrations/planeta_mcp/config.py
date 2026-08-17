from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PlanetaConfig:
    base_url: str = "https://planeta.ru"
    draft_url: str | None = None
    headless: bool = True
    submit_ttl_seconds: int = 300
    live_ttl_seconds: int = 600
    state_path: Path = Path("/data/planeta/campaign.json")
    session_dir: Path | None = None

    def __post_init__(self) -> None:
        if self.session_dir is None:
            object.__setattr__(self, "session_dir", self.state_path.parent)

    @classmethod
    def from_env(cls) -> "PlanetaConfig":
        headless_raw = os.getenv("PLANETA_HEADLESS", "true").strip().lower()
        if headless_raw not in {"true", "false", "1", "0", "yes", "no"}:
            raise ValueError("PLANETA_HEADLESS must be a boolean value")

        submit_ttl = int(os.getenv("PLANETA_SUBMIT_TTL_SECONDS", "300"))
        if submit_ttl <= 0:
            raise ValueError("PLANETA_SUBMIT_TTL_SECONDS must be positive")

        live_ttl = int(os.getenv("PLANETA_LIVE_TTL_SECONDS", "600"))
        if live_ttl <= 0:
            raise ValueError("PLANETA_LIVE_TTL_SECONDS must be positive")

        draft_url = os.getenv("PLANETA_DRAFT_URL", "").strip() or None
        state_path = Path(os.getenv("PLANETA_STATE_PATH", "/data/planeta/campaign.json"))
        session_dir_raw = os.getenv("PLANETA_SESSION_DIR", "").strip()
        session_dir = Path(session_dir_raw) if session_dir_raw else state_path.parent
        return cls(
            base_url=os.getenv("PLANETA_BASE_URL", "https://planeta.ru").rstrip("/"),
            draft_url=draft_url,
            headless=headless_raw in {"true", "1", "yes"},
            submit_ttl_seconds=submit_ttl,
            live_ttl_seconds=live_ttl,
            state_path=state_path,
            session_dir=session_dir,
        )
