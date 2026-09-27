import asyncio,ctypes,importlib.util,types,os
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]/'candidate'
def runtime_source(name):
 root=os.getenv('ARGOS_RUNTIME_SOURCE')
 if not root:pytest.skip('Set ARGOS_RUNTIME_SOURCE to test existing registry/auth integration')
 return Path(root)/'src'/name
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def test_ancestor_only_bpf_does_not_prove_socket_acl(monkeypatch):
 m=load('bpf_review',ROOT/'lan_bpf_check.py')
 monkeypatch.setattr(m.subprocess,'run',lambda *a,**k:types.SimpleNamespace(stdout='/system.slice/argos-lan.socket\n'))
 monkeypatch.setattr(m.os,'open',lambda *a,**k:123)
 monkeypatch.setattr(m.os,'close',lambda *a:None)
 monkeypatch.setattr(m.platform,'machine',lambda:'x86_64')
 def syscall(number,command,ptr,size):
  query=ctypes.cast(ptr,ctypes.POINTER(m.Query)).contents
  # A filter exists only on an ancestor cgroup; no program is attached to the socket unit.
  query.prog_cnt=1 if query.query_flags==1 else 0
  return 0
 monkeypatch.setattr(m.ctypes,'CDLL',lambda *a,**k:types.SimpleNamespace(syscall=syscall))
 with pytest.raises(ValueError):m.check('argos-lan.socket')

def test_lan_registry_entry_expires_after_900_seconds(monkeypatch):
 m=load('registry_review',runtime_source('runtime_registry.py'))
 monkeypatch.setattr(m.time,'time',lambda:1000)
 entry={'url':'http://192.168.7.8:8081','state':'available','last_verified':101}
 monkeypatch.setattr(m,'read_registry',lambda:{'local_id':'local','machines':{'local':{'apis':{'argos_lan':entry}}}})
 assert m.resolve_api('argos_lan')==entry['url']
 entry['last_verified']=99
 assert m.resolve_api('argos_lan') is None

@pytest.mark.parametrize('headers', [[],[(b'authorization',b'Bearer invalid')],[(b'authorization',b'Bearer fixture-only'),(b'authorization',b'Bearer fixture-only')]])
def test_relay_localhost_origin_never_bypasses_api_auth(monkeypatch,headers):
 m=load('auth_review',runtime_source('cloud_auth.py'))
 monkeypatch.setenv('ARGOS_MCP_API_KEY','fixture-only')
 async def target(*a):pytest.fail('Unauthorized API request reached handler')
 sent=[]
 async def send(message):sent.append(message)
 async def receive():return {'type':'http.request','body':b''}
 scope={'type':'http','method':'GET','path':'/api/ha','headers':headers+[(b'x-forwarded-for',b'127.0.0.1')],'client':('127.0.0.1',123),'http_version':'1.1'}
 asyncio.run(m.CloudBearerAuthMiddleware(target)(scope,receive,send))
 assert sent[0]['status']==401
