import time
from types import SimpleNamespace as NS
import pytest
from src.network_runtime import NetworkRuntime,NetworkConflict,CORAL_ID,encode_request
from src.runtime_registry import write_registry


@pytest.fixture
def runtime(tmp_path,monkeypatch):
    path=tmp_path/'registry.json';monkeypatch.setenv('ARGOS_DISCOVERY_REGISTRY',str(path))
    machine={'id':CORAL_ID,'state':'available','last_verified':time.time(),'ssh_host':'192.0.2.2'}
    registry={'schema':1,'local_id':'local','machines':{CORAL_ID:machine}}
    write_registry(registry,path)
    row={'node_id':CORAL_ID,'addr':'192.0.2.1','port':55771,'last_seen':time.time()}
    calls=[]
    def request(address,data,port=None):
        calls.append(address);return {'node_id':CORAL_ID}
    def accept(profile,address):row.update(addr=address,last_seen=time.time())
    bridge=NS(profile=NS(node_id='11111111-1111-4111-8111-111111111111',role='gateway'),
              bind_host='127.0.0.1',registry=NS(all=lambda:[row]),_running=True,
              _request_peer=request,_accept_profile=accept)
    client=NS(host='192.0.2.2',status=lambda:{'ok':True,'uptime_s':1,'models':{}})
    rt=NetworkRuntime(NS(p2p=bridge),lambda _:'',ready=lambda:True,
        guard=NS(evaluate=lambda *a,**kw:NS(allowed=True)),coral=client)
    return rt,path,registry,machine,row,calls


def test_nodes_uses_verified_address_over_old_p2p_row(runtime):
    rt,path,registry,machine,row,calls=runtime
    coral=next(n for n in rt.nodes()['items'] if n['id']==CORAL_ID)
    assert coral['ip']=='192.0.2.2'


def test_p2p_connect_uses_verified_address_and_unavailable_has_no_fallback(runtime):
    rt,path,registry,machine,row,calls=runtime
    result=rt._function({'node':CORAL_ID,'action':'p2p.connect','text':''})
    assert calls==['192.0.2.2']
    machine['state']='unavailable';write_registry(registry,path)
    calls.clear()
    with pytest.raises(NetworkConflict,match='адрес'):
        rt._function({'node':CORAL_ID,'action':'p2p.connect','text':''})
    assert calls==[]
    coral=next(n for n in rt.nodes()['items'] if n['id']==CORAL_ID)
    assert coral['ip']=='' and not coral['ready']


def test_generic_two_argument_handler_receives_owned_core_exactly_once(runtime):
    rt,*_=runtime
    calls=[]
    def handler(text,core):
        calls.append((text,core is rt.core))
        return {'answer':'verified result','execution_status':'succeeded'}
    rt.core.skill_loader=NS(_skills={'example':NS(runtime=NS(handle=handler),
        manifest=NS(name='fixture',version='1',permissions=set()))},_failed={})
    local=rt._local()['id'];catalog=rt.actions(local,'skills')
    request={'request_id':'b'*32,'node':local,'action':catalog['items'][0]['id'],
             'revision':catalog['revision'],'text':'status'}
    result=rt.dispatch(encode_request(request))
    assert calls==[('status',True)]
    assert result=={'answer':'verified result','execution_status':'succeeded'}


def test_two_argument_handler_error_is_called_once_without_chat_fallback(runtime):
    rt,*_=runtime
    calls=[];fallback=[]
    def handler(text,core):
        calls.append((text,core is rt.core))
        raise TypeError('fixture internal error must not leak')
    rt.fallback=lambda text:fallback.append(text)
    rt.core.skill_loader=NS(_skills={'example':NS(runtime=NS(handle=handler),
        manifest=NS(name='fixture',version='1',permissions=set()))},_failed={})
    local=rt._local()['id'];catalog=rt.actions(local,'skills')
    request={'request_id':'c'*32,'node':local,'action':catalog['items'][0]['id'],
             'revision':catalog['revision'],'text':'status'}
    result=rt.dispatch(encode_request(request))
    assert calls==[('status',True)] and fallback==[]
    assert result['execution_status']=='failed'
    assert 'fixture internal error' not in result['answer']
