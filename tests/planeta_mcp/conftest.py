import pytest


@pytest.fixture(autouse=True)
def clear_private_planeta_region(monkeypatch):
    monkeypatch.delenv("ARGOS_PLANETA_PROJECT_REGION", raising=False)
