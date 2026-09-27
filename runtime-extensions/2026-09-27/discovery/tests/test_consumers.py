import json
from pathlib import Path
import time
from src.runtime_registry import write_registry

def snapshot(tmp_path, monkeypatch):
    path = tmp_path / 'registry.json'
    monkeypatch.setenv('ARGOS_DISCOVERY_REGISTRY', str(path))
    data = {'schema': 1, 'local_id': 'local', 'updated_at': time.time(), 'machines': {'local': {'hostname': 'testnode', 'addresses': ['127.0.0.1'], 'state': 'available', 'projects': {'argos': {'path': str(tmp_path), 'state': 'available', 'last_verified': time.time()}}, 'apis': {'home_assistant': {'url': 'http://127.0.0.1:18123', 'state': 'available', 'last_verified': time.time()}}, 'repositories': []}}}
    write_registry(data, path)
    return (path, data)

def test_ha_consumer_uses_current_endpoint_and_refuses_unavailable_map(tmp_path, monkeypatch):
    from src.runtime_registry import api_url
    path, data = snapshot(tmp_path, monkeypatch)
    assert api_url('home_assistant', 'http://192.0.2.99:8123', 'http://127.0.0.1:8123') == 'http://127.0.0.1:18123'
    data['machines']['local']['apis']['home_assistant']['state'] = 'unavailable'
    write_registry(data, path)
    assert api_url('home_assistant', 'http://192.0.2.99:8123', 'http://127.0.0.1:8123') == ''

def test_discovery_api_resolves_only_fresh_registry_entries(tmp_path, monkeypatch):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from src.discovery_api import create_discovery_router
    from src.cloud_auth import CloudBearerAuthMiddleware
    path, data = snapshot(tmp_path, monkeypatch)
    monkeypatch.setenv('ARGOS_MCP_API_KEY', 'test-only-key')
    app = FastAPI()
    app.add_middleware(CloudBearerAuthMiddleware)
    app.include_router(create_discovery_router())
    with TestClient(app) as client:
        assert client.get('/api/discovery').status_code == 401
        headers = {'Authorization': 'Bearer test-only-key'}
        response = client.get('/api/discovery/resolve/path/argos', headers=headers)
        assert response.status_code == 200 and response.json()['value'] == str(tmp_path)
        data['machines']['local']['projects']['argos']['last_verified'] = 1
        write_registry(data, path)
        assert client.get('/api/discovery/resolve/path/argos', headers=headers).status_code == 409

def test_cached_coral_client_follows_verified_new_ip(tmp_path, monkeypatch):
    import pytest
    from src.network_coral import CoralClient, CoralError
    path, data = snapshot(tmp_path, monkeypatch)
    entry = {'url': 'http://192.0.2.1:8770', 'state': 'available', 'last_verified': time.time()}
    data['machines']['local']['apis']['coral'] = entry
    write_registry(data, path)
    key = tmp_path / 'key'
    key.write_bytes(b'x' * 32)
    key.chmod(384)
    monkeypatch.setenv('ARGOS_CORAL_SECRET_FILE', str(key))
    monkeypatch.setenv('ARGOS_CORAL_URL', entry['url'])
    client = CoralClient.from_env()
    entry['url'] = 'http://192.0.2.2:8771'
    write_registry(data, path)
    attempts = []

    def connection(host, port, **kwargs):
        attempts.append((host, port))
        raise CoralError('test transport unavailable')
    client.connection_factory = connection
    with pytest.raises(CoralError):
        client.status()
    assert attempts == [('192.0.2.2', 8771)]
    attempts.clear()
    entry['state'] = 'unavailable'
    write_registry(data, path)
    with pytest.raises(CoralError):
        client.status()
    assert attempts == []

def test_configured_coral_client_created_while_offline_recovers_after_refresh(tmp_path, monkeypatch):
    import pytest
    from src.network_coral import CoralClient, CoralError
    path, data = snapshot(tmp_path, monkeypatch)
    entry = {'url': 'http://192.0.2.1:8770', 'state': 'unavailable', 'last_verified': 0}
    data['machines']['local']['apis']['coral'] = entry
    write_registry(data, path)
    key = tmp_path / 'key'
    key.write_bytes(b'x' * 32)
    key.chmod(384)
    monkeypatch.setenv('ARGOS_CORAL_SECRET_FILE', str(key))
    monkeypatch.setenv('ARGOS_CORAL_URL', entry['url'])
    client = CoralClient.from_env()
    assert client is not None
    with pytest.raises(CoralError):
        client.status()
    entry.update(url='http://192.0.2.3:8770', state='available', last_verified=time.time())
    write_registry(data, path)
    attempted = []

    def connection(host, port, **kwargs):
        attempted.append(host)
        raise CoralError('test transport')
    client.connection_factory = connection
    with pytest.raises(CoralError):
        client.status()
    assert attempted == ['192.0.2.3'] and client.host == '192.0.2.3'

def test_known_ssh_command_follows_verified_machine_and_refuses_stale(tmp_path, monkeypatch):
    import pytest
    from src.runtime_registry import ssh_command, remote_api_url
    path, data = snapshot(tmp_path, monkeypatch)
    machine = {'id': 'remote', 'hostname': 'argos-coral', 'state': 'available', 'last_verified': time.time(), 'ssh_host': '192.168.1.99', 'roles': ['coral'], 'apis': {'ollama': {'state': 'unavailable'}}}
    data['machines']['remote'] = machine
    write_registry(data, path)
    config = tmp_path / 'terminal.json'
    config.write_text(json.dumps({'nodes': {'remote': {'transport': 'ssh', 'host': '192.168.1.94', 'user': 'root', 'port': 22, 'key': '/test/key', 'known_hosts': '/test/hosts'}}}))
    monkeypatch.setenv('ARGOS_TERMINAL_INVENTORY', str(config))
    argv = ssh_command('coral')
    assert 'HostKeyAlias=192.168.1.94' in argv and argv[-1] == 'root@192.168.1.99'
    assert remote_api_url('coral', 'ollama', 'http://192.168.1.94:11434') == ''
    machine['last_verified'] = 1
    write_registry(data, path)
    with pytest.raises(ValueError, match='unavailable'):
        ssh_command('coral')

def test_current_memory_marks_expired_machine_and_repository_stale(tmp_path, monkeypatch):
    from src.runtime_registry import memory_context
    path, data = snapshot(tmp_path, monkeypatch)
    machine = data['machines']['local']
    machine['last_verified'] = 1
    machine['repositories'] = [{'path': '/test/project', 'state': 'available', 'last_verified': 1, 'head': 'old', 'branch': 'main', 'dirty': False}]
    context = memory_context(snapshot=data)
    assert 'Machine local: testnode; state=stale; last_verified=1' in context
    assert 'repo /test/project: state=stale; last_verified=1' in context
