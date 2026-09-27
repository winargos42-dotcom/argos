import importlib.util
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ha_dashboard',ROOT/'candidate/src/ha_dashboard.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def entity(name,state,**attrs):
 return {'entity_id':name,'state':state,'attributes':attrs,'last_updated':'2026-09-27T01:00:00Z'}

def test_units_and_unavailable_climate():
 s=m.summarize([entity('sensor.s','1.2',unit_of_measurement='kVA'),entity('climate.floor','unavailable',current_temperature=25)])
 assert s['power']=='1200 ВА'
 assert s['climate']=='—'
 assert s['counts']=={'total':2,'available':1,'unavailable':1,'unknown':0}

def test_active_power_preferred_and_no_child_lock_count():
 s=m.summarize([entity('sensor.s','7',unit_of_measurement='VA'),entity('sensor.p','0.25',unit_of_measurement='kW'),entity('switch.test_child_lock','on'),entity('light.a','on')])
 assert s['power']=='250 Вт';assert s['lights_on']=='1 шт'

def test_catalog_allows_metadata_not_private_attributes():
 s=m.summarize([entity('person.a','home',friendly_name='<img src=x>',latitude=123,access_token='do-not-return'),entity('sensor.bad','unknown'),entity('camera.a','idle',entity_picture='/api/camera_proxy/camera.a?token=secret')])
 assert s['counts']['unknown']==1
 assert s['entities'][0]['name']=='<img src=x>'
 assert 'secret' not in str(s) and 'latitude' not in str(s) and 'do-not-return' not in str(s)
 assert s['domains']=={'camera':1,'person':1,'sensor':1}

@pytest.mark.parametrize('rows', [None, {}, [{'state':'on'}], [entity('light.x',None)]])
def test_invalid_upstream_rejected(rows):
 with pytest.raises(ValueError):m.summarize(rows)

def test_nonfinite_power_not_presented_as_measurement():
 assert m.summarize([entity('sensor.x','nan',unit_of_measurement='W')])['power']=='—'

def test_climate_uses_first_available():
 s=m.summarize([entity('climate.a','unknown',current_temperature=22),entity('climate.b','heat',current_temperature=21)])
 assert s['climate']=='21 (единица не подтверждена) (heat)'

def test_registry_stale_or_missing_token_never_fetches(monkeypatch,tmp_path):
 import sys,types
 registry=types.ModuleType('src.runtime_registry');registry.api_url=lambda *args:''
 monkeypatch.setitem(sys.modules,'src.runtime_registry',registry)
 monkeypatch.setattr(m.requests,'get',lambda *args,**kw:pytest.fail('Should not fetch'))
 assert m.snapshot()['error']=='address_unverified'
 registry.api_url=lambda *args:'http://example.test:8123'
 monkeypatch.setenv('ARGOS_HA_TOKEN_FILE',str(tmp_path/'missing'))
 assert m.snapshot()['error']=='token_missing'

def test_failures_clear_states_and_dont_leak_errors(monkeypatch,tmp_path):
 import sys,types
 registry=types.ModuleType('src.runtime_registry');registry.api_url=lambda *args:'http://example.test:8123'
 monkeypatch.setitem(sys.modules,'src.runtime_registry',registry)
 token=tmp_path/'token';token.write_text('test-token');monkeypatch.setenv('ARGOS_HA_TOKEN_FILE',str(token))
 def fail(*args,**kw):raise m.requests.ConnectionError('url containing private information')
 monkeypatch.setattr(m.requests,'get',fail)
 out=m.snapshot();assert not out['ok'] and out['entities']==[] and out['observed_at'] is None
 assert out['error']=='unreachable' and 'private' not in str(out)

def test_snapshot_follows_resolver_and_is_get_only(monkeypatch,tmp_path):
 import sys,types
 registry=types.ModuleType('src.runtime_registry');registry.api_url=lambda *args:'http://new.test:8123'
 monkeypatch.setitem(sys.modules,'src.runtime_registry',registry)
 token=tmp_path/'token';token.write_text('test-token');monkeypatch.setenv('ARGOS_HA_TOKEN_FILE',str(token))
 calls=[]
 class Response:
  def raise_for_status(self):pass
  def json(self):return [entity('sensor.test','5',unit_of_measurement='W')]
 def get(url,**kw):calls.append((url,kw));return Response()
 monkeypatch.setattr(m.requests,'get',get)
 out=m.snapshot();assert out['ok'] and out['read_only'] and out['observed_at']>0
 assert calls[0][0]=='http://new.test:8123/api/states'
 assert out['url']=='http://new.test:8123' and out['power']=='5 Вт'


def test_climate_fahrenheit_and_invalid_readings():
 assert m.summarize([entity('climate.a','heat',current_temperature=72)], '°F')['climate']=='72°F (heat)'
 for value in [None, 'nan', 'inf', 'not a number', True]:
  assert m.summarize([entity('climate.a','heat',current_temperature=value)], '°C')['climate']=='heat'
