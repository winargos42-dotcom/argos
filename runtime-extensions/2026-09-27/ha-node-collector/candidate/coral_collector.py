"""Signed Coral status bound to a fresh verified registry identity.

Only network_coral.CoralClient.status() is used; no P2P, inference or commands.
Direct trusted module loading avoids src.__init__ and unrelated core startup.
"""
import math
import os
from pathlib import Path
import stat
import types

BUDGET=3.0
CONFIG_KEYS=('ARGOS_CORAL_SECRET_FILE','ARGOS_STATE_ROOT','ARGOS_DISCOVERY_REGISTRY')


def read_key(path):
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,'rb') as stream:
        info=os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid!=os.geteuid() or info.st_mode & 0o077 or info.st_size>4096:
            raise ValueError('invalid credential file')
        key=stream.read(4097).strip()
    if not 32<=len(key)<=4096 or key.lower() in (b'argos_default_secret',b'change_me',b'changeme'):
        raise ValueError('invalid credential')
    return key


def _trusted_module(path,name):
    info=path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_uid!=0 or info.st_mode & 0o022:
        raise ValueError('untrusted runtime module')
    module=types.ModuleType(name)
    module.__file__=str(path)
    exec(compile(path.read_bytes(),str(path),'exec'),module.__dict__)
    return module


def load_dependencies(runtime_root=None):
    from dotenv import dotenv_values
    root=Path(runtime_root or os.getenv('ARGOS_NODE_RUNTIME_ROOT') or Path(__file__).resolve().parents[2]).resolve()
    config_path=root/'argos.env'
    info=config_path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_uid!=0 or info.st_mode & 0o022:
        raise ValueError('untrusted configuration file')
    values=dotenv_values(config_path,interpolate=False)
    settings={key:os.environ.get(key,values.get(key)) for key in CONFIG_KEYS}
    registry=_trusted_module(root/'app'/'src'/'runtime_registry.py','_ha_verified_registry')
    transport=_trusted_module(root/'app'/'src'/'network_coral.py','_ha_signed_coral_transport')
    registry_path=settings.get('ARGOS_DISCOVERY_REGISTRY') or str(Path(settings.get('ARGOS_STATE_ROOT') or root/'state')/'discovery'/'registry.json')
    view=types.SimpleNamespace(read_registry=lambda:registry.read_registry(registry_path),fresh=registry.fresh)
    return view,transport.CoralClient,read_key(settings.get('ARGOS_CORAL_SECRET_FILE') or '')


def _failed(code):
    return {'connected':False,'service_ready':False,'role':'accelerator','error':code,
            'status_source':'coral_accelerator_api','readiness_scope':'signed_status','inference_verified':False}


def _endpoint(registry,identity):
    snapshot=registry.read_registry()
    if not isinstance(snapshot,dict) or snapshot.get('schema')!=1:
        return None,'not_configured'
    machines=snapshot.get('machines',{})
    machine=machines.get(identity) if isinstance(machines,dict) else None
    if not isinstance(machine,dict) or machine.get('id')!=identity or 'coral' not in machine.get('roles',[]):
        return None,'not_configured'
    if not registry.fresh(machine): return None,'stale'
    apis=machine.get('apis',{})
    api=apis.get('coral') if isinstance(apis,dict) else None
    if not isinstance(api,dict) or not isinstance(api.get('url'),str): return None,'not_configured'
    if not registry.fresh(api): return None,'stale'
    return api['url'],None


def collect_coral(expected_node_id,*,dependencies=None):
    try:
        registry,client_factory,key=(dependencies or load_dependencies)()
        endpoint,error=_endpoint(registry,expected_node_id)
        if error: return _failed(error)
        client=client_factory(endpoint,key,timeout=BUDGET)
    except Exception:
        return _failed('not_configured')
    try:
        status=client.status()
    except TimeoutError:
        return _failed('timeout')
    except Exception:
        # Current client merges HTTP/auth/transport errors; never guess causes.
        return _failed('service_unavailable')
    if (not isinstance(status,dict) or status.get('ok') is not True
            or type(status.get('uptime_s')) not in (int,float)
            or not math.isfinite(status['uptime_s']) or not 0<=status['uptime_s']<=3155760000
            or not isinstance(status.get('models'),dict)):
        return _failed('invalid_response')
    try:
        current,error=_endpoint(registry,expected_node_id)
        if error or current!=endpoint: return _failed(error or 'stale')
    except Exception:
        return _failed('stale')
    return {'connected':True,'service_ready':True,'role':'accelerator','node_id':expected_node_id,
            'uptime_seconds':status['uptime_s'],'authenticated':True,
            'status_source':'coral_accelerator_api','readiness_scope':'signed_status','inference_verified':False}
