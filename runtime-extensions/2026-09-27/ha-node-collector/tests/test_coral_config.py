import os,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'candidate'))

def test_scoped_config_avoids_core_initialization_and_environment_mutation(tmp_path,monkeypatch):
 import coral_collector as adapter
 src=tmp_path/'app'/'src';src.mkdir(parents=True)
 (src/'__init__.py').write_text('raise AssertionError("core must not initialize")')
 (src/'runtime_registry.py').write_text('def read_registry(path=None): return {"path":str(path)}\ndef fresh(entry): return True\n')
 (src/'network_coral.py').write_text('class CoralClient: pass\n')
 key=tmp_path/'key';key.write_bytes(b'k'*48);key.chmod(0o600)
 (tmp_path/'argos.env').write_text(f'ARGOS_CORAL_SECRET_FILE={key}\nARGOS_STATE_ROOT={tmp_path}/state\nUNRELATED_PRIVATE_SETTING=keep-private\n')
 before=dict(os.environ)
 registry,client,secret=adapter.load_dependencies(tmp_path)
 assert registry.read_registry()['path']==str(tmp_path/'state'/'discovery'/'registry.json')
 assert client.__name__=='CoralClient' and secret==b'k'*48
 assert dict(os.environ)==before

def test_fifo_key_rejected_without_blocking(tmp_path):
 import coral_collector as adapter
 path=tmp_path/'fifo';os.mkfifo(path,0o600)
 with pytest.raises(ValueError): adapter.read_key(path)

def test_public_or_symlink_key_rejected(tmp_path):
 import coral_collector as adapter
 key=tmp_path/'key';key.write_bytes(b'k'*48);key.chmod(0o644)
 with pytest.raises(ValueError): adapter.read_key(key)
 key.chmod(0o600);link=tmp_path/'link';link.symlink_to(key)
 with pytest.raises(OSError): adapter.read_key(link)
