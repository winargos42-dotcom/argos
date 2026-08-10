from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet, InvalidToken


class SessionStateError(ValueError):
    pass


_ALLOWED_TOP_LEVEL = {"cookies", "origins"}
_FORBIDDEN_KEYS = {
    "username",
    "email_password",
    "password",
    "passport",
    "inn",
    "document",
    "documents",
    "document_blob",
}


def _guard_mapping(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = str(key).strip().lower().replace("-", "_")
            if normalized in _FORBIDDEN_KEYS:
                raise SessionStateError(f"Forbidden identity/credential field: {key}")
            _guard_mapping(item)
    elif isinstance(value, list):
        for item in value:
            _guard_mapping(item)


def _validate_storage_state(storage_state: dict[str, Any]) -> None:
    keys = set(storage_state)
    if keys != _ALLOWED_TOP_LEVEL:
        unknown = keys - _ALLOWED_TOP_LEVEL
        missing = _ALLOWED_TOP_LEVEL - keys
        detail = []
        if unknown:
            detail.append(f"unknown keys: {sorted(unknown)}")
        if missing:
            detail.append(f"missing keys: {sorted(missing)}")
        raise SessionStateError("Invalid Playwright storage state (" + "; ".join(detail) + ")")
    if not isinstance(storage_state["cookies"], list) or not isinstance(storage_state["origins"], list):
        raise SessionStateError("cookies and origins must be lists")
    _guard_mapping(storage_state)


class SessionStore:
    def __init__(self, path: str | Path, fernet_key: bytes | str):
        self.path = Path(path)
        if isinstance(fernet_key, str):
            fernet_key = fernet_key.encode("ascii")
        try:
            self._fernet = Fernet(fernet_key)
        except (ValueError, TypeError) as exc:
            raise ValueError("PLANETA_SESSION_KEY must be a valid Fernet key") from exc

    def save_storage_state(self, storage_state: dict[str, Any]) -> None:
        _validate_storage_state(storage_state)
        plaintext = json.dumps(
            storage_state, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        encrypted = self._fernet.encrypt(plaintext)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(
            prefix=f".{self.path.name}.", suffix=".tmp", dir=self.path.parent
        )
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(encrypted)
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

    def load_storage_state(self) -> dict[str, Any] | None:
        if not self.path.exists():
            return None
        try:
            plaintext = self._fernet.decrypt(self.path.read_bytes())
        except InvalidToken as exc:
            raise SessionStateError("Stored browser session cannot be decrypted") from exc
        try:
            data = json.loads(plaintext.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SessionStateError("Stored browser session is invalid JSON") from exc
        if not isinstance(data, dict):
            raise SessionStateError("Stored browser session must be a JSON object")
        _validate_storage_state(data)
        return data

    def clear(self) -> None:
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass
