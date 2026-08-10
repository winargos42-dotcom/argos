import pytest
from cryptography.fernet import Fernet

from integrations.planeta_mcp.session_store import SessionStateError, SessionStore


def test_session_state_is_encrypted_at_rest(tmp_path):
    key = Fernet.generate_key()
    store = SessionStore(tmp_path / "session.enc", key)
    state = {"cookies": [{"name": "sid", "value": "sensitive"}], "origins": []}
    store.save_storage_state(state)
    raw = (tmp_path / "session.enc").read_bytes()
    assert b"sensitive" not in raw
    assert store.load_storage_state() == state


def test_clear_removes_browser_state(tmp_path):
    key = Fernet.generate_key()
    store = SessionStore(tmp_path / "session.enc", key)
    store.save_storage_state({"cookies": [], "origins": []})
    store.clear()
    assert store.load_storage_state() is None


def test_rejects_credentials_and_unknown_top_level_keys(tmp_path):
    key = Fernet.generate_key()
    store = SessionStore(tmp_path / "session.enc", key)
    with pytest.raises(SessionStateError):
        store.save_storage_state({"cookies": [], "origins": [], "password": "no"})
    with pytest.raises(SessionStateError):
        store.save_storage_state({"cookies": [], "origins": [], "extra": []})


def test_rejects_identity_fields_nested_in_state(tmp_path):
    key = Fernet.generate_key()
    store = SessionStore(tmp_path / "session.enc", key)
    with pytest.raises(SessionStateError):
        store.save_storage_state({
            "cookies": [],
            "origins": [{"origin": "https://planeta.ru", "passport": "no"}],
        })


def test_rejects_malformed_fernet_key(tmp_path):
    with pytest.raises(ValueError):
        SessionStore(tmp_path / "session.enc", b"not-a-fernet-key")
