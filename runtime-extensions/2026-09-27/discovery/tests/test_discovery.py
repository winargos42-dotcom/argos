import json
import os
from pathlib import Path
import subprocess
import time

import pytest


def git(path, *args):
    result = subprocess.run(['git', '-C', str(path), *args], check=True,
                            capture_output=True, text=True)
    return result.stdout.strip()


def test_registry_does_not_resolve_missing_or_expired_paths(tmp_path, monkeypatch):
    from src.runtime_registry import write_registry, resolve_path
    path = tmp_path / 'registry.json'
    monkeypatch.setenv('ARGOS_DISCOVERY_REGISTRY', str(path))
    project = tmp_path / 'project'
    project.mkdir()
    snapshot = {'schema': 1, 'local_id': 'local', 'updated_at': time.time(), 'machines': {
        'local': {'projects': {'argos': {'path': str(project), 'state': 'available',
                    'last_verified': time.time(), 'provenance': 'test'}}, 'apis': {}, 'repositories': []}}}
    write_registry(snapshot, path)
    assert resolve_path('argos') == str(project)
    assert resolve_path('argos', override=str(tmp_path / 'missing')) == str(project)
    project.rmdir()
    assert resolve_path('argos') is None
    project.mkdir()
    snapshot['machines']['local']['projects']['argos']['last_verified'] = 1
    write_registry(snapshot, path)
    assert resolve_path('argos') is None
    assert path.stat().st_mode & 0o777 == 0o600


def test_memory_map_replaces_one_fact_and_keeps_other_facts(tmp_path):
    from src.memory_index import save_fact, replace_source_fact, search_index
    db = tmp_path / 'facts.sqlite3'
    save_fact(db, 'unrelated owner fact')
    replace_source_fact(db, 'old project /missing', source='runtime_discovery', source_file='registry')
    replace_source_fact(db, 'current project /real', source='runtime_discovery', source_file='registry')
    import sqlite3
    with sqlite3.connect(db) as conn:
        assert conn.execute('SELECT COUNT(*) FROM documents').fetchone()[0] == 2
    assert not search_index(db, 'missing')
    assert search_index(db, 'real')[0]['text'] == 'current project /real'
    assert search_index(db, 'unrelated')


def test_api_resolution_requires_fresh_verified_protocol(tmp_path, monkeypatch):
    from src.runtime_registry import write_registry, resolve_api
    path = tmp_path / 'registry.json'
    monkeypatch.setenv('ARGOS_DISCOVERY_REGISTRY', str(path))
    snapshot = {'schema': 1, 'local_id': 'local', 'updated_at': time.time(), 'machines': {
        'local': {'projects': {}, 'apis': {'argos': {'url': 'http://127.0.0.1:8080',
               'state': 'unavailable', 'last_verified': 0, 'provenance': 'test'}}, 'repositories': []}}}
    write_registry(snapshot, path)
    assert resolve_api('argos') is None
    snapshot['machines']['local']['apis']['argos'].update(state='available', last_verified=time.time())
    write_registry(snapshot, path)
    assert resolve_api('argos') == 'http://127.0.0.1:8080'


def test_repo_sync_only_fast_forwards_clean_matching_branch(tmp_path):
    from src.runtime_discovery import sync_repository
    origin = tmp_path / 'origin.git'
    work = tmp_path / 'work'
    peer = tmp_path / 'peer'
    subprocess.run(['git', 'init', '--bare', str(origin)], check=True, capture_output=True)
    subprocess.run(['git', 'clone', str(origin), str(work)], check=True, capture_output=True)
    for path in (work,):
        git(path, 'config', 'user.email', 'test@localhost')
        git(path, 'config', 'user.name', 'test')
    git(work, 'checkout', '-b', 'main')
    (work / 'data').write_text('one')
    git(work, 'add', 'data'); git(work, 'commit', '-m', 'one')
    git(work, 'push', '-u', 'origin', 'main')
    subprocess.run(['git', 'clone', '-b', 'main', str(origin), str(peer)], check=True, capture_output=True)
    git(peer, 'config', 'user.email', 'test@localhost'); git(peer, 'config', 'user.name', 'test')
    (peer / 'data').write_text('two')
    git(peer, 'commit', '-am', 'two'); git(peer, 'push')
    before = git(work, 'rev-parse', 'HEAD')
    assert sync_repository(work, apply=False)['state'] == 'dry_run'
    assert git(work, 'rev-parse', 'HEAD') == before
    result = sync_repository(work, apply=True)
    assert result['state'] == 'updated'
    assert (work / 'data').read_text() == 'two'
    (work / 'data').write_text('local work')
    assert sync_repository(work, apply=True)['reason'] == 'dirty'
    assert (work / 'data').read_text() == 'local work'


def test_probe_rejects_unrelated_json_and_credentials():
    from src.runtime_discovery import valid_health, safe_url
    assert valid_health('argos', {'ok': True, 'ready': True})
    assert not valid_health('argos', {'status': 'ok'})
    assert valid_health('ollama', {'models': []})
    assert not valid_health('ollama', {'ok': True})
    assert safe_url('https://user:secret@example.org/path') is None
    assert safe_url('http://127.0.0.1:8080?token=secret') is None


def test_repository_metadata_never_contains_remote_credentials(tmp_path):
    from src.runtime_discovery import repository_status
    subprocess.run(['git', 'init', str(tmp_path / 'repo')], check=True, capture_output=True)
    repo = tmp_path / 'repo'
    git(repo, 'remote', 'add', 'origin', 'https://user:secret@example.org/project.git?token=hidden')
    metadata = repository_status(repo)
    rendered = json.dumps(metadata)
    assert 'secret' not in rendered and 'hidden' not in rendered
    assert metadata['remote_url'] == 'https://example.org/project.git'


def test_sync_fetches_only_explicit_matching_branch_when_tracking_ref_missing(tmp_path):
    from src.runtime_discovery import sync_repository
    origin, work = tmp_path / 'origin.git', tmp_path / 'work'
    subprocess.run(['git', 'init', '--bare', str(origin)], check=True, capture_output=True)
    subprocess.run(['git', 'clone', str(origin), str(work)], check=True, capture_output=True)
    git(work, 'config', 'user.email', 'test@localhost'); git(work, 'config', 'user.name', 'test')
    git(work, 'checkout', '-b', 'main')
    (work / 'data').write_text('one'); git(work, 'add', '.'); git(work, 'commit', '-m', 'one')
    git(work, 'push', '-u', 'origin', 'main')
    git(work, 'update-ref', '-d', 'refs/remotes/origin/main')
    git(work, 'config', 'remote.origin.fetch', '+refs/heads/other:refs/remotes/origin/other')
    before = git(work, 'rev-parse', 'HEAD')
    assert sync_repository(work)['state'] == 'dry_run'
    result = sync_repository(work, apply=True)
    assert result['state'] == 'up_to_date'
    assert git(work, 'rev-parse', 'refs/remotes/origin/main') == before
    assert git(work, 'rev-parse', '--abbrev-ref', '@{upstream}') == 'origin/main'
    git(work, 'config', 'branch.main.merge', 'refs/heads/other')
    assert sync_repository(work, apply=True)['reason'] == 'upstream_mismatch'


def test_refresh_writes_serializable_candidate_observations(tmp_path, monkeypatch):
    from src import runtime_discovery as discovery
    monkeypatch.setenv('ARGOS_DISCOVERY_REGISTRY', str(tmp_path / 'registry.json'))
    monkeypatch.setenv('ARGOS_MEMPALACE_FACTS_PATH', str(tmp_path / 'facts.sqlite3'))
    monkeypatch.setattr(discovery, 'candidate_config', lambda: {})
    monkeypatch.setattr(discovery, 'inspect_machine', lambda _: {
        'id': 'local', 'projects': {}, 'apis': {}, 'repositories': []})
    monkeypatch.setattr(discovery, 'probe_api', lambda kind, url: {
        'url': url, 'state': 'available', 'last_verified': time.time()})
    result = discovery.refresh(include_remote=False)
    assert json.loads((tmp_path / 'registry.json').read_text())['schema'] == 1
    assert result['memory_publication']['state'] == 'available'


def test_sync_refuses_divergence_and_preserves_local_commit(tmp_path):
    from src.runtime_discovery import sync_repository
    origin, work, peer = tmp_path / 'origin.git', tmp_path / 'work', tmp_path / 'peer'
    subprocess.run(['git', 'init', '--bare', str(origin)], check=True, capture_output=True)
    subprocess.run(['git', 'clone', str(origin), str(work)], check=True, capture_output=True)
    git(work, 'config', 'user.email', 'test@localhost'); git(work, 'config', 'user.name', 'test')
    git(work, 'checkout', '-b', 'main'); (work / 'data').write_text('one')
    git(work, 'add', '.'); git(work, 'commit', '-m', 'one'); git(work, 'push', '-u', 'origin', 'main')
    subprocess.run(['git', 'clone', '-b', 'main', str(origin), str(peer)], check=True, capture_output=True)
    git(peer, 'config', 'user.email', 'test@localhost'); git(peer, 'config', 'user.name', 'test')
    (peer / 'data').write_text('remote'); git(peer, 'commit', '-am', 'remote'); git(peer, 'push')
    (work / 'local').write_text('local'); git(work, 'add', '.'); git(work, 'commit', '-m', 'local')
    before = git(work, 'rev-parse', 'HEAD')
    assert sync_repository(work, apply=True)['reason'] == 'diverged'
    assert git(work, 'rev-parse', 'HEAD') == before and not git(work, 'status', '--porcelain')


def test_remote_ip_candidates_only_follow_known_host_identity(monkeypatch):
    from src import runtime_discovery as discovery
    calls = []
    def lookup(command, **kwargs):
        calls.append(command)
        return '192.168.1.99 STREAM known-host'
    monkeypatch.setattr(discovery, 'run', lookup)
    assert discovery.remote_candidates({'host': '192.168.1.94'}, {'hostname': 'known-host'}) == [
        '192.168.1.94', '192.168.1.99']
    assert calls == [['getent', 'ahostsv4', 'known-host']]
    monkeypatch.setattr(discovery, 'run', lambda *args, **kwargs: json.dumps({'id': 'wrong-node'}))
    with pytest.raises(ValueError, match='remote_identity_mismatch'):
        discovery.remote_machine('expected-node', {'host':'192.168.1.94', 'user':'root', 'port':22,
            'key':'/test/key', 'known_hosts':'/test/hosts', 'node_id_file':'/test/id'})


def test_known_hostname_new_ip_precedes_old_secondary_interfaces(monkeypatch):
    from src import runtime_discovery as discovery
    monkeypatch.setattr(discovery, 'run', lambda *args, **kwargs: '192.168.1.99 STREAM known-host')
    values = discovery.remote_candidates({'host':'192.168.1.94'}, {'hostname':'known-host',
        'addresses':['192.168.1.94','172.17.0.1','172.18.0.1','172.19.0.1']})
    assert '192.168.1.99' in values and len(values) <= 4


def test_sync_refuses_changed_repository_identity_before_any_fetch(tmp_path, monkeypatch):
    from src import runtime_discovery as discovery
    current = {'state':'available', 'id':'new', 'path':str(tmp_path), 'remote_url':'https://example.test/new.git',
               'branch':'main', 'remote':'origin', 'merge_ref':'refs/heads/main', 'upstream':'origin/main', 'dirty':False}
    expected = {**current, 'id':'old', 'remote_url':'https://example.test/old.git'}
    monkeypatch.setattr(discovery, 'repository_status', lambda _: current)
    def forbidden(*args, **kwargs):
        raise AssertionError('Identity mismatch must be rejected before Git mutation')
    monkeypatch.setattr(discovery, 'git', forbidden)
    assert discovery.sync_repository(tmp_path, apply=True, expected=expected)['reason'] == 'repository_identity_changed'


def test_local_project_candidates_follow_configured_user_home(tmp_path, monkeypatch):
    import pwd
    from types import SimpleNamespace
    from src.runtime_discovery import candidate_config
    inventory = tmp_path/'nodes.json'
    inventory.write_text(json.dumps({'nodes':{'local':{'transport':'local','user':'fixture'}}}))
    monkeypatch.setenv('ARGOS_TERMINAL_INVENTORY', str(inventory))
    monkeypatch.setenv('ARGOS_DISCOVERY_CONFIG', str(tmp_path/'missing-config'))
    monkeypatch.setattr(pwd, 'getpwnam', lambda _: SimpleNamespace(pw_dir=str(tmp_path/'user-home')))
    config = candidate_config()
    assert str(tmp_path/'user-home/Documents') in config['projects']['documents']
    assert str(tmp_path/'user-home/Projects/argos-panel7') in config['projects']['panel']
