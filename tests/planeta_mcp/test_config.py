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
