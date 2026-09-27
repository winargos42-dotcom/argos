import importlib.util,sys,types,os
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]

@pytest.mark.skipif(not os.getenv("ARGOS_RUNTIME_SOURCE"), reason="Set ARGOS_RUNTIME_SOURCE to patched runtime for bridge integration test")
def test_existing_bridge_tracks_registry_changes_without_restart(monkeypatch):
 logger=types.ModuleType('src.argos_logger');logger.get_logger=lambda name:types.SimpleNamespace(warning=lambda *a:None)
 registry=types.ModuleType('src.runtime_registry');current=['http://new.test:8123'];registry.api_url=lambda *a:current[0]
 monkeypatch.setitem(sys.modules,'src.argos_logger',logger);monkeypatch.setitem(sys.modules,'src.runtime_registry',registry)
 monkeypatch.setenv('HA_TOKEN','test-token')
 spec=importlib.util.spec_from_file_location('bridge',Path(os.environ['ARGOS_RUNTIME_SOURCE'])/'src/connectivity/home_assistant.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 bridge=m.HomeAssistantBridge();assert bridge.enabled and bridge.base_url==current[0]
 current[0]='http://moved.test:8123';assert bridge.base_url==current[0]
 current[0]='';assert not bridge.enabled
 monkeypatch.setattr(m.requests,'get',lambda *a,**k:pytest.fail('Stale API must not be used'))
 assert 'не настроен' in bridge.health()
