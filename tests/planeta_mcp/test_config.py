import pytest

from integrations.planeta_mcp.config import PlanetaConfig


def test_live_ttl_reads_from_environment(monkeypatch):
    monkeypatch.setenv("PLANETA_LIVE_TTL_SECONDS", "900")
    config = PlanetaConfig.from_env()
    assert config.live_ttl_seconds == 900


def test_live_ttl_must_be_positive(monkeypatch):
    monkeypatch.setenv("PLANETA_LIVE_TTL_SECONDS", "0")
    with pytest.raises(ValueError, match="PLANETA_LIVE_TTL_SECONDS"):
        PlanetaConfig.from_env()


def test_session_dir_can_be_independent_from_campaign_state(monkeypatch, tmp_path):
    state_path = tmp_path / "work" / "campaign.json"
    session_dir = tmp_path / "persistent-session"
    monkeypatch.setenv("PLANETA_STATE_PATH", str(state_path))
    monkeypatch.setenv("PLANETA_SESSION_DIR", str(session_dir))

    config = PlanetaConfig.from_env()

    assert config.state_path == state_path
    assert config.session_dir == session_dir


def test_session_dir_defaults_to_campaign_parent(monkeypatch, tmp_path):
    state_path = tmp_path / "work" / "campaign.json"
    monkeypatch.setenv("PLANETA_STATE_PATH", str(state_path))
    monkeypatch.delenv("PLANETA_SESSION_DIR", raising=False)

    config = PlanetaConfig.from_env()

    assert config.session_dir == state_path.parent


def test_blank_session_dir_defaults_to_campaign_parent(monkeypatch, tmp_path):
    state_path = tmp_path / "work" / "campaign.json"
    monkeypatch.setenv("PLANETA_STATE_PATH", str(state_path))
    monkeypatch.setenv("PLANETA_SESSION_DIR", "   ")

    config = PlanetaConfig.from_env()

    assert config.session_dir == state_path.parent


def test_direct_config_defaults_session_dir_to_state_parent(tmp_path):
    state_path = tmp_path / "campaign.json"

    config = PlanetaConfig(state_path=state_path)

    assert config.session_dir == state_path.parent
