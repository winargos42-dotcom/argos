from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from .models import CampaignPayload


class CampaignStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> CampaignPayload | None:
        if not self.path.exists():
            return None
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return CampaignPayload.model_validate(data)

    def load_required(self) -> CampaignPayload:
        payload = self.load()
        if payload is None:
            raise FileNotFoundError(f"Campaign state not found: {self.path}")
        return payload

    def save(self, payload: CampaignPayload) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        serialized = json.dumps(
            payload.canonical_dict(), ensure_ascii=False, indent=2, sort_keys=True
        ) + "\n"
        fd, temp_name = tempfile.mkstemp(
            prefix=f".{self.path.name}.", suffix=".tmp", dir=self.path.parent
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(serialized)
                handle.flush()
                os.fsync(handle.fileno())
            try:
                os.chmod(temp_name, 0o600)
            except OSError:
                pass
            os.replace(temp_name, self.path)
        except Exception:
            try:
                os.unlink(temp_name)
            except FileNotFoundError:
                pass
            raise
