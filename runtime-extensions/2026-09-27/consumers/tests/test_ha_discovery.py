import time
from types import SimpleNamespace
import pytest
from src.runtime_registry import write_registry
from src.skills import ha_camera_vision, light_vision


@pytest.fixture
def configured(tmp_path, monkeypatch):
    path=tmp_path/'registry.json'
    monkeypatch.setenv('ARGOS_DISCOVERY_REGISTRY',str(path))
    monkeypatch.setenv('ARGOS_HA_URL','http://192.0.2.1:8123')
    token=tmp_path/'token'; token.write_text('fixture-only')
    monkeypatch.setenv('ARGOS_HA_TOKEN_FILE',str(token))
    entry={'url':'http://192.0.2.2:8123','state':'available','last_verified':time.time()}
    registry={'schema':1,'local_id':'local','machines':{'local':{'apis':{'home_assistant':entry}}}}
    write_registry(registry,path)
    return path,registry,entry


def test_camera_list_and_light_request_follow_current_endpoint(configured, monkeypatch):
    import requests
    path,registry,entry=configured
    attempts=[]
    def get(url,**kw):
        attempts.append(url)
        return SimpleNamespace(raise_for_status=lambda:None,json=lambda:[])
    monkeypatch.setattr(requests,'get',get)
    monkeypatch.setattr(requests,'request',lambda method,url,**kw:get(url,**kw))
    assert ha_camera_vision.list_cameras() == []
    assert light_vision._ha_request('GET','states') == []
    assert attempts == ['http://192.0.2.2:8123/api/states']*2
    entry['url']='http://192.0.2.3:8123';write_registry(registry,path)
    ha_camera_vision.list_cameras();light_vision._ha_request('GET','states')
    assert attempts[-2:] == ['http://192.0.2.3:8123/api/states']*2


def test_unavailable_ha_never_calls_old_url_or_claims_no_cameras(configured, monkeypatch):
    import requests
    path,registry,entry=configured
    entry['state']='unavailable';write_registry(registry,path)
    def forbidden(*a,**kw): raise AssertionError('No HTTP attempt to stale URL')
    monkeypatch.setattr(requests,'get',forbidden);monkeypatch.setattr(requests,'request',forbidden)
    with pytest.raises(RuntimeError,match='Home Assistant'):
        ha_camera_vision.snapshot('camera.fixture')
    with pytest.raises(RuntimeError,match='Home Assistant'):
        light_vision._ha_request('GET','states')
    answer=ha_camera_vision.handle('камеры дома')
    assert 'нет камер' not in answer
    assert 'Home Assistant' in answer


def test_camera_transport_failure_is_not_an_empty_camera_inventory(configured, monkeypatch):
    import requests
    def failed(*a,**kw): raise requests.ConnectionError('fixture transport failure')
    monkeypatch.setattr(requests,'get',failed)
    answer=ha_camera_vision.handle('камеры дома')
    assert 'нет камер' not in answer and 'Home Assistant' in answer
