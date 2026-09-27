import importlib.util,json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('lan_discovery',ROOT/'candidate/lan_discovery.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

@pytest.fixture
def policy(tmp_path):
 path=tmp_path/'policy.json';path.write_text(json.dumps({'interface':'fixture0','trusted_subnet':'192.168.7.0/24','lan_port':8081}))
 return path

def interfaces(address='192.168.7.8'):
 return [{'ifname':'fixture0','addr_info':[{'family':'inet','scope':'global','local':address}]}]

def test_missing_policy_does_not_invent_endpoint(tmp_path):
 assert m.probe_lan(tmp_path/'missing') is None

def test_only_protocol_ready_response_marks_lan_available(policy):
 calls=[]
 def health(host,port,interface):calls.append((host,port,interface));return {'ok':True,'ready':True}
 result=m.probe_lan(policy,addresses=interfaces(),health=health)
 assert result['state']=='available' and result['url']=='http://192.168.7.8:8081'
 assert result['last_verified']>0 and calls==[('192.168.7.8',8081,'fixture0')]

def test_changed_ip_is_used_without_previous_fallback(policy):
 calls=[]
 def health(host,*args):calls.append(host);return {'ok':True,'ready':True}
 assert m.probe_lan(policy,addresses=interfaces('192.168.7.9'),health=health)['url']=='http://192.168.7.9:8081'
 assert calls==['192.168.7.9']

@pytest.mark.parametrize('reply',[None,{}, {'ok':True,'ready':False},{'ok':False,'ready':True},{'ok':True,'ready':'true'}])
def test_unverified_health_never_means_available(policy,reply):
 result=m.probe_lan(policy,addresses=interfaces(),health=lambda *a:reply)
 assert result['state']=='unavailable' and result['last_verified']==0

def test_wrong_interface_or_network_is_never_contacted(policy):
 def bad(*a):raise AssertionError('must not contact outside trusted interface/subnet')
 assert m.probe_lan(policy,addresses=interfaces('192.168.8.8'),health=bad)['state']=='unavailable'
 rows=interfaces();rows[0]['ifname']='other0'
 assert m.probe_lan(policy,addresses=rows,health=bad)['state']=='unavailable'

def test_transport_failure_is_sanitized_unavailable(policy):
 def fail(*a):raise OSError('private address details')
 result=m.probe_lan(policy,addresses=interfaces(),health=fail)
 assert result['state']=='unavailable' and 'private' not in json.dumps(result)
