import importlib.util,sys,types
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location('review_ha_dashboard',Path(__file__).resolve().parents[1]/'candidate/src/ha_dashboard.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

@pytest.mark.parametrize('config_ok',[True,False])
def test_snapshot_config_controls_temperature_unit_without_inventing_celsius(monkeypatch,tmp_path,config_ok):
    registry=types.ModuleType('src.runtime_registry');registry.api_url=lambda *a:'http://fixture.test:8123'
    monkeypatch.setitem(sys.modules,'src.runtime_registry',registry)
    token=tmp_path/'test-token';token.write_text('fixture-only');monkeypatch.setenv('ARGOS_HA_TOKEN_FILE',str(token))
    calls=[]
    def get(url,**kw):
        calls.append(url)
        if url.endswith('/api/states'):
            value=[{'entity_id':'climate.fixture','state':'heat','attributes':{'current_temperature':72}}]
        else:
            assert url.endswith('/api/config')
            if not config_ok:raise m.requests.ConnectionError('fixture error')
            value={'unit_system':{'temperature':'°F'}}
        return types.SimpleNamespace(raise_for_status=lambda:None,json=lambda:value)
    monkeypatch.setattr(m.requests,'get',get)
    result=m.snapshot()
    assert result['ok'] and len(calls)==2
    assert result['climate']==('72°F (heat)' if config_ok else '72 (единица не подтверждена) (heat)')
