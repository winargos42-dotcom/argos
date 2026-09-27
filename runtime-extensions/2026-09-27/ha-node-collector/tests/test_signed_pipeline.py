import copy,hashlib,hmac,importlib.util,json,sys,time
from pathlib import Path
from types import SimpleNamespace
import pytest

ROOT=Path(__file__).resolve().parents[1]
CANDIDATE=ROOT/'candidate'
sys.path.insert(0,str(CANDIDATE))
import collectors
from publisher import Bridge
spec=importlib.util.spec_from_file_location('review_network_coral',str(ROOT/'reference'/'network_coral.py'))
transport=importlib.util.module_from_spec(spec);spec.loader.exec_module(transport)
NODE='dddddddd-dddd-4ddd-8ddd-dddddddddddd'
KEY=b'fixture-only-signed-status-key-0123456789'

@pytest.mark.parametrize('valid_signature',[True,False])
def test_registry_real_hmac_status_and_typed_mqtt_pipeline(valid_signature):
    attempts=[]
    raw=json.dumps({'ok':True,'uptime_s':12.5,'models':{}}).encode()
    class Response:
        status=200
        def read1(self,limit):return raw
        def isclosed(self):return True
        def getheader(self,name):
            text='\n'.join(('argos-coral-v1-resp',attempts[-1][3]['X-Argos-Nonce'],'200',hashlib.sha256(raw).hexdigest())).encode()
            return hmac.new(KEY,text,hashlib.sha256).hexdigest() if valid_signature else 'invalid-signature'
        def close(self):pass
    class Connection:
        def __init__(self,host,port,timeout):
            assert host=='127.0.0.2' and port==8770 and timeout==3.0
            self.sock=SimpleNamespace(settimeout=lambda remaining:None)
        def connect(self):pass
        def request(self,method,path,body,headers):attempts.append((method,path,body,headers))
        def getresponse(self):return Response()
        def close(self):pass
    factory=lambda url,key,timeout:transport.CoralClient(url,key,timeout=timeout,connection_factory=Connection)
    stamp=time.time()
    current={'schema':1,'machines':{NODE:{'id':NODE,'state':'available','last_verified':stamp,'roles':['coral'],
        'apis':{'coral':{'url':'http://127.0.0.2:8770','state':'available','last_verified':stamp}}}}}
    registry=SimpleNamespace(read_registry=lambda:copy.deepcopy(current),fresh=lambda entry:entry.get('state')=='available' and 0<=time.time()-entry.get('last_verified',0)<=900)
    result=collectors.collect_coral(NODE,dependencies=lambda:(registry,factory,KEY))
    assert len(attempts)==1
    method,path,body,headers=attempts[0]
    assert (method,path,body)==('GET','/v1/status',b'')
    signed='\n'.join(('argos-coral-v1',method,path,headers['X-Argos-Ts'],headers['X-Argos-Nonce'],hashlib.sha256(body).hexdigest())).encode()
    assert hmac.compare_digest(headers['X-Argos-Mac'],hmac.new(KEY,signed,hashlib.sha256).hexdigest())
    node={'id':NODE,'name':'Synthetic Coral','kind':'coral_accel'}
    messages=[];bridge=Bridge([node],lambda *args:messages.append(args),clock=lambda:100.)
    epoch=bridge.connect();assert bridge.update(node,result,epoch,100.)
    state=json.loads(messages[-2][1])
    if valid_signature:
        assert state['connected'] is True and state['service_ready'] is True and state['uptime_seconds']==12.5
        assert state['status_source']=='coral_accelerator_api' and state['inference_verified'] is False
        assert messages[-1][1]=='ONLINE'
    else:
        assert state['connected'] is False and state['service_ready'] is None and state['uptime_seconds'] is None
        assert messages[-1][1]=='OFFLINE'


def test_mqtt_old_epoch_and_expired_observation_cannot_revalidate_source():
    node={'id':NODE,'name':'Synthetic Coral','kind':'coral_accel'}
    messages=[];clock=[100.]
    bridge=Bridge([node],lambda *args:messages.append(args),clock=lambda:clock[0])
    epoch=bridge.connect();current={'connected':True,'service_ready':True,'role':'accelerator','uptime_seconds':2}
    bridge.disconnect();bridge.connect();before=len(messages)
    assert bridge.update(node,current,epoch,100.) is False
    assert len(messages)==before
    clock[0]=161.
    assert bridge.update(node,current,bridge.snapshot(),100.) is False
    assert messages[-1][1]=='OFFLINE'
    for payload in bridge.configs[NODE].values():
        assert payload['expire_after']==90 and payload['availability_mode']=='all'
