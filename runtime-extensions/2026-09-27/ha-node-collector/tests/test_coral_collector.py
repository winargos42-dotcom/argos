import copy,importlib.util,json,sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
import pytest

ROOT=Path(__file__).resolve().parents[1]
CANDIDATE=ROOT/'candidate'
sys.path.insert(0,str(CANDIDATE))
import collectors as c
import main
import entities
from publisher import Bridge

NODE='coral-fixture'
def snapshot(url='http://127.0.0.2:8770'):
 return {'schema':1,'machines':{NODE:{'id':NODE,'roles':['coral'],'state':'available','last_verified':1000.,
   'apis':{'coral':{'url':url,'state':'available','last_verified':1000.}}}}}

@pytest.fixture
def dep():
 snap=snapshot()
 registry=SimpleNamespace(read_registry=Mock(side_effect=lambda:copy.deepcopy(snap)),
     fresh=lambda entry:entry.get('state')=='available' and 0<=1000.-entry.get('last_verified',0)<=900.)
 client=Mock();client.status.return_value={'ok':True,'uptime_s':123.,'models':{}}
 factory=Mock(return_value=client)
 return SimpleNamespace(snap=snap,registry=registry,client=client,factory=factory,
     load=lambda:(registry,factory,b'k'*48))

def collect(dep): return c.collect_coral(NODE,dependencies=dep.load)

def test_main_uses_accelerator_collector_and_never_old_p2p(monkeypatch):
 signed=Mock(return_value={'connected':True,'role':'accelerator','service_ready':True})
 monkeypatch.setattr(main,'collect_coral',signed,raising=False)
 monkeypatch.setattr(main,'collect_p2p',Mock(side_effect=AssertionError('legacy P2P was contacted')),raising=False)
 assert main.observe(main.NODES[1])['role']=='accelerator'
 signed.assert_called_once_with(main.NODES[1]['id'])

def test_verified_endpoint_signed_status_and_truthful_scope(dep):
 result=collect(dep)
 dep.factory.assert_called_once_with('http://127.0.0.2:8770',b'k'*48,timeout=3.)
 dep.client.status.assert_called_once_with()
 assert result=={'connected':True,'service_ready':True,'role':'accelerator','node_id':NODE,
   'uptime_seconds':123.,'authenticated':True,'status_source':'coral_accelerator_api',
   'readiness_scope':'signed_status','inference_verified':False}
 dep.client.infer.assert_not_called()

def test_ip_change_uses_new_verified_endpoint_each_observation(dep):
 collect(dep)
 dep.snap['machines'][NODE]['apis']['coral']['url']='http://127.0.0.3:8770'
 collect(dep)
 assert dep.factory.call_args.args[0]=='http://127.0.0.3:8770'

@pytest.mark.parametrize('change,error',[
 (lambda s:s.clear(),'not_configured'),
 (lambda s:s['machines'][NODE].update(last_verified=99.),'stale'),
 (lambda s:s['machines'][NODE].update(last_verified=1001.),'stale'),
 (lambda s:s['machines'][NODE].update(state='unavailable'),'stale'),
 (lambda s:s['machines'][NODE]['apis']['coral'].update(last_verified=99.),'stale'),
 (lambda s:s['machines'][NODE]['apis']['coral'].update(state='unavailable'),'stale'),
 (lambda s:s['machines'][NODE].update(id='different'),'not_configured')])
def test_unverified_or_stale_registry_fails_closed_before_connection(dep,change,error):
 change(dep.snap);r=collect(dep)
 assert r['connected'] is False and r['service_ready'] is False and r['error']==error
 dep.factory.assert_not_called()

def test_registry_invalidated_during_request_discards_success(dep):
 def status():
  dep.snap['machines'][NODE]['state']='unavailable'
  return {'ok':True,'uptime_s':12.,'models':{}}
 dep.client.status.side_effect=status
 assert collect(dep)['error']=='stale'

def test_registry_address_changed_during_request_discards_success(dep):
 def status():
  dep.snap['machines'][NODE]['apis']['coral']['url']='http://127.0.0.3:8770'
  return {'ok':True,'uptime_s':12.,'models':{}}
 dep.client.status.side_effect=status
 assert collect(dep)['error']=='stale'

@pytest.mark.parametrize('payload',[None,{},[],{'ok':True,'uptime_s':float('nan'),'models':{}},
 {'ok':False,'uptime_s':1,'models':{}},{'ok':True,'uptime_s':1,'models':[]}])
def test_invalid_status_cannot_mark_ready(dep,payload):
 dep.client.status.return_value=payload
 assert collect(dep)['error']=='invalid_response'

def test_error_classification_is_sanitized_and_does_not_guess_auth(dep):
 dep.client.status.side_effect=RuntimeError('private IP token details')
 r=collect(dep)
 assert r['error']=='service_unavailable' and 'private' not in json.dumps(r)
 dep.client.status.side_effect=TimeoutError('private details')
 assert collect(dep)['error']=='timeout'

def test_credentials_missing_are_not_configured():
 def missing(): raise ValueError('private credential file')
 assert c.collect_coral(NODE,dependencies=missing)['error']=='not_configured'

def test_mqtt_exposes_new_source_scope_without_claiming_inference(dep):
 raw=collect(dep);state=entities.normalize_state(raw)
 assert state['status_source']=='coral_accelerator_api'
 assert state['readiness_scope']=='signed_status' and state['inference_verified'] is False
 configs=entities.discovery({'id':NODE,'name':'Coral','kind':'coral_accel'})
 assert all('json_attributes_topic' in x for x in configs.values())
 ready=next(v for k,v in configs.items() if '/service_ready/' in k)
 assert ready['name']=='Signed status ready'
 assert all(x['expire_after']==90 for x in configs.values())

def test_stale_probe_offlines_previous_mqtt_success(dep):
 node={'id':NODE,'name':'Coral','kind':'coral_accel'};messages=[]
 bridge=Bridge([node],lambda *args:messages.append(args),clock=lambda:100.)
 epoch=bridge.connect();assert bridge.update(node,collect(dep),epoch,100.)
 dep.snap['machines'][NODE]['last_verified']=1.
 assert bridge.update(node,collect(dep),epoch,100.)
 state=json.loads(messages[-2][1]);assert state['connected'] is False
 assert state['service_ready'] is None and state['uptime_seconds'] is None
 assert messages[-1][1]=='OFFLINE'
