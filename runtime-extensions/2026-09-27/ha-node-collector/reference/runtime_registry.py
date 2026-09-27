from __future__ import annotations

import json
import ipaddress
import os
from pathlib import Path
import tempfile
import time


def registry_path():
    state = Path(os.getenv('ARGOS_STATE_ROOT', str(Path(__file__).resolve().parents[2] / 'state')))
    return Path(os.getenv('ARGOS_DISCOVERY_REGISTRY', str(state / 'discovery/registry.json')))


def read_registry(path=None):
    try:
        with Path(path or registry_path()).open('rb') as stream:
            raw = stream.read(1024 * 1024 + 1)
        value = json.loads(raw) if len(raw) <= 1024 * 1024 else None
        if not isinstance(value, dict) or value.get('schema') != 1 or not isinstance(value.get('machines'), dict):
            return {}
        return value
    except (OSError, ValueError, TypeError):
        return {}


def write_registry(value, path=None):
    path = Path(path or registry_path())
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    raw = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()
    if len(raw) > 1024 * 1024:
        raise ValueError('Registry exceeds its size budget')
    fd, temporary = tempfile.mkstemp(prefix='.registry-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def fresh(entry, now=None):
    now = time.time() if now is None else now
    try:
        age = now - float(entry.get('last_verified', 0))
        return entry.get('state') == 'available' and 0 <= age <= 900
    except (TypeError, ValueError):
        return False


def resolve_path(name, override=None, machine_id=None):
    if override:
        try:
            path = Path(override).expanduser().resolve(strict=True)
            if path.is_dir():
                return str(path)
        except OSError:
            pass
    value = read_registry()
    machine = value.get('machines', {}).get(machine_id or value.get('local_id'), {})
    entry = machine.get('projects', {}).get(name, {})
    if not fresh(entry):
        return None
    path = entry.get('path')
    if not isinstance(path, str):
        return None
    if machine_id and machine_id != value.get('local_id'):
        return path
    try:
        return str(Path(path).resolve(strict=True)) if Path(path).is_dir() else None
    except OSError:
        return None


def resolve_api(name, override=None, machine_id=None):
    value = read_registry()
    machines = value.get('machines', {})
    ordered = [machine_id] if machine_id else [value.get('local_id'), *machines]
    candidates = []
    for identity in dict.fromkeys(ordered):
        entry = machines.get(identity, {}).get('apis', {}).get(name, {})
        if fresh(entry) and isinstance(entry.get('url'), str):
            candidates.append(entry['url'])
    if override and override.rstrip('/') in candidates:
        return override.rstrip('/')
    return candidates[0] if candidates else None


def api_url(name, override=None, legacy_default=''):
    found = resolve_api(name, override)
    if found:
        return found
    if registry_path().exists():
        return ''
    return (override or legacy_default).rstrip('/')


def resolve_machine(role_or_id):
    value = read_registry()
    for identity, machine in value.get('machines', {}).items():
        if identity == role_or_id or role_or_id in machine.get('roles', []):
            return machine if fresh(machine) else None
    return None


def remote_api_url(role, name, legacy_default=''):
    machine = resolve_machine(role)
    if machine:
        return resolve_api(name, machine_id=machine['id']) or ''
    return '' if registry_path().exists() else legacy_default.rstrip('/')


def machine_host(role_or_id):
    machine = resolve_machine(role_or_id)
    if machine:
        return machine.get('ssh_host') or next(iter(machine.get('addresses', [])), None)
    return None


def ssh_command(role_or_id):
    """Resolve host from the verified map, credentials from the existing private inventory."""
    machine = resolve_machine(role_or_id)
    if machine is None or not machine.get('ssh_host'):
        raise ValueError('Known machine unavailable or stale')
    host = str(ipaddress.ip_address(machine['ssh_host']))
    path = os.getenv('ARGOS_TERMINAL_INVENTORY', '/etc/argos/terminal-nodes.json')
    nodes = json.loads(Path(path).read_text())['nodes']
    entry = nodes[machine['id']]
    if entry.get('transport') != 'ssh':
        raise ValueError('Known SSH transport unavailable')
    return ['ssh', '-F', '/dev/null', '-T', '-i', entry['key'], '-p', str(entry['port']),
            '-o', 'BatchMode=yes', '-o', 'IdentitiesOnly=yes', '-o', 'ConnectTimeout=5',
            '-o', 'StrictHostKeyChecking=yes', '-o', 'UserKnownHostsFile=' + entry['known_hosts'],
            '-o', 'HostKeyAlias=' + entry['host'], '-o', 'ForwardAgent=no',
            '-o', 'ClearAllForwardings=yes', '-o', 'PermitLocalCommand=no', '--', entry['user'] + '@' + host]


def memory_context(query='', snapshot=None):
    value = read_registry() if snapshot is None else snapshot
    if not value:
        return ''
    lines = ['CURRENT VERIFIED SYSTEM MAP — проверяй state и last_verified; исторические ссылки не являются текущими.']
    for identity, machine in list(value.get('machines', {}).items())[:8]:
        state = machine.get('state', 'unavailable')
        if state == 'available' and not fresh(machine):
            state = 'stale'
        lines.append(f"Machine {identity}: {machine.get('hostname', '')}; state={state}; last_verified={machine.get('last_verified', 0)}; "
                     f"addresses={','.join(machine.get('addresses', []))}")
        for category, field in (('projects', 'path'), ('apis', 'url')):
            for name, entry in list(machine.get(category, {}).items())[:24]:
                state = entry.get('state', 'unavailable')
                if state == 'available' and not fresh(entry):
                    state = 'stale'
                lines.append(f"{category}.{name}: {entry.get(field, '')}; state={state}; "
                             f"last_verified={entry.get('last_verified', 0)}")
        for repository in machine.get('repositories', [])[:16]:
            state = repository.get('state', 'unavailable')
            if state == 'available' and not fresh(repository):
                state = 'stale'
            lines.append(f"repo {repository.get('path')}: state={state}; last_verified={repository.get('last_verified', 0)}; "
                         f"{repository.get('remote_url', '')}; "
                         f"branch={repository.get('branch', '')}; head={repository.get('head', '')}; "
                         f"dirty={repository.get('dirty')}; ahead={repository.get('ahead')}; behind={repository.get('behind')}")
        for entry in machine.get('retired', [])[:8]:
            lines.append(f"STALE {entry.get('name')}: {entry.get('path', entry.get('url', ''))}; do not use")
    return '\n'.join(lines)[:10000]


def publish_memory(snapshot):
    path = os.getenv('ARGOS_MEMPALACE_FACTS_PATH', '').strip()
    if not path:
        return {'state': 'unavailable', 'reason': 'facts_path_not_configured'}
    from src.memory_index import replace_source_fact
    ident = replace_source_fact(path, memory_context(snapshot=snapshot), source='runtime_discovery',
                                source_file=str(registry_path()), wing='technical', room='current_system',
                                protected_paths=[os.getenv('ARGOS_MEMPALACE_SQLITE_PATH', ''),
                                                 os.getenv('ARGOS_MEMPALACE_INDEX_PATH', '')])
    return {'state': 'available', 'fact_id': ident}
