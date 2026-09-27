from __future__ import annotations

import argparse
import fcntl
import hashlib
import http.client
import inspect
import ipaddress
import itertools
import json
import os
import pwd
from pathlib import Path
import re
import shlex
import socket
import subprocess
import threading
import time
from urllib.parse import urlsplit, urlunsplit
import uuid

from src.runtime_registry import memory_context, publish_memory, read_registry, registry_path, write_registry


def run(command, *, timeout=5, input_text=None):
    result = subprocess.run(command, input=input_text, capture_output=True, text=True,
                            timeout=timeout, env={**os.environ, 'GIT_TERMINAL_PROMPT': '0', 'LC_ALL': 'C'})
    if result.returncode:
        raise RuntimeError('command_failed')
    if len(result.stdout) > 1024 * 1024:
        raise RuntimeError('output_too_large')
    return result.stdout.strip()


def git(path, *args, timeout=5):
    return run(['git', '-C', str(path), *args], timeout=timeout)


def sanitized_remote(value):
    if '://' in value:
        parsed = urlsplit(value)
        host = parsed.hostname or ''
        if parsed.port:
            host += ':' + str(parsed.port)
        return urlunsplit((parsed.scheme, host, parsed.path, '', ''))
    if re.fullmatch(r'[A-Za-z0-9._-]+@[A-Za-z0-9.-]+:[A-Za-z0-9_./-]+', value):
        return value.split('@', 1)[1]
    return value if value.startswith('/') and '\n' not in value else ''


def repository_status(path):
    path = Path(path).resolve()
    result = {'path': str(path), 'state': 'unavailable', 'provenance': 'git', 'last_verified': 0,
              'branch': '', 'head': '', 'dirty': None, 'upstream': '', 'remote': '', 'remote_url': '',
              'merge_ref': '', 'ahead': None, 'behind': None}
    try:
        if Path(git(path, 'rev-parse', '--show-toplevel')).resolve() != path:
            return result
        try:
            result['remote_url'] = sanitized_remote(git(path, 'remote', 'get-url', 'origin'))
        except RuntimeError:
            pass
        result['dirty'] = bool(git(path, 'status', '--porcelain', '--untracked-files=normal'))
        result['branch'] = git(path, 'branch', '--show-current')
        result['head'] = git(path, 'rev-parse', '--verify', 'HEAD')
        try:
            result['remote'] = git(path, 'config', '--get', 'branch.' + result['branch'] + '.remote')
            result['merge_ref'] = git(path, 'config', '--get', 'branch.' + result['branch'] + '.merge')
            result['remote_url'] = sanitized_remote(git(path, 'remote', 'get-url', result['remote']))
            if result['merge_ref'] == 'refs/heads/' + result['branch']:
                result['upstream'] = result['remote'] + '/' + result['branch']
            else:
                result['upstream'] = git(path, 'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{upstream}')
            counts = git(path, 'rev-list', '--left-right', '--count', 'HEAD...refs/remotes/' + result['upstream']).split()
            result['ahead'], result['behind'] = map(int, counts)
        except (RuntimeError, ValueError):
            pass
        result.update(state='available', last_verified=time.time())
    except (OSError, RuntimeError, subprocess.TimeoutExpired):
        pass
    result['id'] = hashlib.sha256((str(path) + '\n' + result['remote_url']).encode()).hexdigest()[:24]
    return result


def sync_repository(path, *, apply=False, expected=None):
    before = repository_status(path)
    def conflict(reason):
        return {'state': 'conflict', 'reason': reason, 'repository': before}
    if expected is not None and any(before.get(k) != expected.get(k) for k in
                                    ('id', 'path', 'remote_url', 'branch', 'remote', 'merge_ref')):
        return conflict('repository_identity_changed')
    if before['state'] != 'available':
        return conflict('unavailable')
    if before['dirty']:
        return conflict('dirty')
    if not before['branch']:
        return conflict('detached')
    remote, branch = before['remote'], before['branch']
    if not remote or before['merge_ref'] != 'refs/heads/' + branch or before['upstream'] != remote + '/' + branch:
        return conflict('upstream_mismatch')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', remote):
        return conflict('remote_invalid')
    if not apply:
        return {'state': 'dry_run', 'repository': before, 'remote_ref_verified': False}
    try:
        tracking_ref = 'refs/remotes/' + remote + '/' + branch
        git(path, 'check-ref-format', tracking_ref)
        git(path, 'fetch', '--no-tags', remote, before['merge_ref'] + ':' + tracking_ref, timeout=25)
        current = repository_status(path)
        if current['dirty'] or any(current[k] != before[k] for k in ('head', 'branch', 'upstream', 'remote_url')):
            return conflict('changed_during_fetch')
        if current['ahead']:
            return conflict('diverged' if current['behind'] else 'ahead')
        target = git(path, 'rev-parse', '--verify', tracking_ref + '^{commit}')
        git(path, 'merge-base', '--is-ancestor', 'HEAD', target)
        current = repository_status(path)
        if current['dirty'] or any(current[k] != before[k] for k in ('head', 'branch', 'upstream', 'remote_url', 'merge_ref')):
            return conflict('changed_before_merge')
        if target != before['head']:
            git(path, '-c', 'core.hooksPath=/dev/null', 'merge', '--ff-only', '--no-edit', target, timeout=15)
        after = repository_status(path)
        if after['head'] != target or after['dirty']:
            return conflict('postcondition_failed')
        try:
            configured_upstream = git(path, 'rev-parse', '--abbrev-ref', '@{upstream}')
        except RuntimeError:
            configured_upstream = ''
        if not configured_upstream:
            # A narrow/single-branch clone may lack a fetch mapping for this
            # explicitly configured tracking branch. Preserve all existing specs.
            check = repository_status(path)
            if check['dirty'] or any(check[k] != after[k] for k in ('head', 'id', 'branch', 'remote', 'merge_ref')):
                return conflict('changed_before_tracking_configuration')
            git(path, 'config', '--add', 'remote.' + remote + '.fetch', before['merge_ref'] + ':' + tracking_ref)
            configured_upstream = git(path, 'rev-parse', '--abbrev-ref', '@{upstream}')
        if configured_upstream != remote + '/' + branch:
            return conflict('tracking_configuration_mismatch')
        return {'state': 'updated' if target != before['head'] else 'up_to_date', 'repository': after,
                'before_head': before['head'], 'remote_ref_verified': True}
    except (OSError, RuntimeError, subprocess.TimeoutExpired):
        return conflict('fetch_or_ff_failed')


def safe_url(value):
    try:
        parsed = urlsplit(value)
        if (parsed.scheme not in {'http', 'https'} or not parsed.hostname or parsed.username is not None
                or parsed.password is not None or parsed.query or parsed.fragment
                or parsed.path not in {'', '/'} or not 1 <= (parsed.port or 80) <= 65535):
            return None
        return value.rstrip('/')
    except (TypeError, ValueError):
        return None


def valid_health(kind, body):
    if not isinstance(body, dict):
        return False
    if kind == 'argos':
        return body.get('ok') is True and body.get('ready') is True
    if kind == 'ollama':
        return isinstance(body.get('models'), list)
    if kind == 'home_assistant':
        return body.get('message') == 'API running.'
    return False


def probe_api(kind, url):
    result = {'url': safe_url(url) or '', 'state': 'unavailable', 'last_verified': 0,
              'observed_at': time.time(), 'provenance': 'protocol_health:' + kind}
    if not result['url']:
        result['reason'] = 'invalid_url'
        return result
    try:
        if kind == 'coral':
            from src.network_coral import CoralClient, validate_status
            key_path = os.getenv('ARGOS_CORAL_SECRET_FILE', '')
            if not key_path:
                result['reason'] = 'credential_not_configured'
                return result
            with open(key_path, 'rb') as stream:
                key = stream.read(4097).strip()
            validate_status(CoralClient(url, key, timeout=2).status())
        else:
            paths = {'argos': '/health', 'ollama': '/api/tags', 'home_assistant': '/api/'}
            parsed = urlsplit(url)
            connection_class = http.client.HTTPSConnection if parsed.scheme == 'https' else http.client.HTTPConnection
            connection = connection_class(parsed.hostname, parsed.port, timeout=2)
            transports = []
            def abort():
                for transport in transports:
                    try:
                        transport.shutdown(socket.SHUT_RDWR)
                        transport.close()
                    except OSError:
                        pass
                connection.close()
            watchdog = threading.Timer(2, abort)
            watchdog.daemon = True
            started = time.monotonic()
            headers = {'Accept': 'application/json', 'Connection': 'close'}
            if kind == 'home_assistant':
                with open(os.getenv('ARGOS_HA_TOKEN_FILE', '/etc/argos/ha-token'), encoding='utf-8') as stream:
                    headers['Authorization'] = 'Bearer ' + stream.read(4096).strip()
            try:
                watchdog.start()
                connection.connect()
                transports.append(connection.sock)
                connection.request('GET', paths[kind], headers=headers)
                response = connection.getresponse()
                raw = response.read(65537)
                if time.monotonic() - started >= 2 or response.status != 200 or len(raw) > 65536 or not valid_health(kind, json.loads(raw)):
                    raise ValueError('unexpected_protocol_response')
            finally:
                watchdog.cancel()
                if watchdog.ident is not None:
                    watchdog.join(timeout=0.1)
                connection.close()
        result.update(state='available', last_verified=time.time())
    except (OSError, ValueError, KeyError, RuntimeError, http.client.HTTPException):
        result['reason'] = 'health_check_failed'
    return result


def identity(node_file):
    try:
        value = Path(node_file).read_text().strip()
        return str(uuid.UUID(value))
    except (OSError, ValueError):
        value = Path('/etc/machine-id').read_text().strip()
        return 'machine-' + hashlib.sha256(value.encode()).hexdigest()[:24]


def interfaces():
    try:
        rows = json.loads(run(['ip', '-j', 'address', 'show'], timeout=2))
        return [{'name': row['ifname'], 'addresses': [a['local'] for a in row.get('addr_info', [])
                 if a.get('scope') == 'global' and not ipaddress.ip_address(a['local']).is_loopback]}
                for row in rows[:32]]
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.TimeoutExpired):
        return []


def service_directories():
    result = []
    for scope, unit in (('--user', 'argos-local.service'), ('--user', 'hermes-gateway.service')):
        try:
            value = run(['systemctl', scope, 'show', unit, '--property=WorkingDirectory', '--value'], timeout=2)
            if value.startswith('/') and Path(value).is_dir():
                result.append(value)
        except (OSError, RuntimeError, subprocess.TimeoutExpired):
            pass
    return result


def listening_ports():
    try:
        rows = run(['ss', '-H', '-lnt'], timeout=2).splitlines()[:256]
        return sorted({int(row.split()[3].rsplit(':', 1)[1]) for row in rows})
    except (OSError, RuntimeError, ValueError, IndexError, subprocess.TimeoutExpired):
        return []


def candidate_config():
    runtime = Path(os.getenv('ARGOS_RUNTIME_ROOT', str(Path(__file__).resolve().parents[2])))
    data = runtime.parent
    inventory = os.getenv('ARGOS_TERMINAL_INVENTORY', '/etc/argos/terminal-nodes.json')
    homes = [Path.home()]
    try:
        for entry in list(json.loads(Path(inventory).read_text()).get('nodes', {}).values())[:8]:
            if entry.get('transport') == 'local':
                homes.append(Path(pwd.getpwnam(entry['user']).pw_dir))
    except (OSError, ValueError, KeyError, TypeError):
        pass
    homes = list(dict.fromkeys(homes))
    value = {'runtime_root': str(runtime), 'node_id_file': str(runtime / 'app/config/node_id'),
             'projects': {'runtime': [str(runtime / 'app')], 'argos': [str(data / 'improve'), str(data / 'recovery')],
                          'backups': [str(runtime / 'backups')], 'documents': [str(home/'Documents') for home in homes],
                          'mukhtar': [str(home/'mukhtar-development') for home in homes],
                          'panel': [str(home/'Projects/argos-panel7') for home in homes]},
             'repository_roots': [str(data), str(data / 'improve/git'), *map(str, homes), *[str(home/'Projects') for home in homes]],
             'terminal_inventory': inventory}
    file = os.getenv('ARGOS_DISCOVERY_CONFIG', '/etc/argos/discovery.json')
    try:
        configured = json.loads(Path(file).read_text())
        for key in ('runtime_root', 'node_id_file', 'projects', 'repository_roots', 'terminal_inventory'):
            if key in configured:
                value[key] = configured[key]
    except FileNotFoundError:
        pass
    return value


def inspect_machine(config):
    now = time.time()
    machine = {'id': identity(config['node_id_file']), 'hostname': socket.gethostname(), 'state': 'available',
               'last_verified': now, 'observed_at': now, 'provenance': 'local_os',
               'interfaces': interfaces(), 'projects': {}, 'apis': {}, 'repositories': []}
    machine['addresses'] = list(dict.fromkeys(a for row in machine['interfaces'] for a in row['addresses']))
    service_dirs = service_directories()
    for name, candidates in list(config['projects'].items())[:24]:
        override = os.getenv('ARGOS_PROJECT_' + name.upper(), '').strip()
        candidates = ([override] if override else []) + list(candidates)
        if name == 'runtime':
            candidates.extend(service_dirs)
        seen = []
        for candidate in candidates[:12]:
            path = Path(candidate).expanduser()
            valid = path.is_dir()
            seen.append({'path': str(path), 'state': 'available' if valid else 'unavailable'})
            if valid:
                machine['projects'][name] = {'path': str(path.resolve()), 'state': 'available', 'last_verified': now,
                    'observed_at': now, 'provenance': 'explicit_override' if candidate == override else 'known_candidate',
                    'candidates': seen}
                break
        else:
            machine['projects'][name] = {'path': '', 'state': 'unavailable', 'last_verified': 0,
                                        'observed_at': now, 'provenance': 'known_candidates', 'candidates': seen}
    repo_paths = {Path(entry['path']) for entry in machine['projects'].values() if entry['state'] == 'available'}
    for root in config['repository_roots'][:8]:
        root = Path(root).expanduser()
        if not root.is_dir():
            continue
        repo_paths.add(root)
        try:
            repo_paths.update(p for p in itertools.islice(root.iterdir(), 64) if p.is_dir() and (p / '.git').exists())
        except OSError:
            continue
    repo_paths = {path.resolve() for path in repo_paths}
    for path in sorted(repo_paths, key=str)[:32]:
        if (path / '.git').exists():
            machine['repositories'].append(repository_status(path))
    machine['service_directories'] = service_dirs
    machine['listening_tcp_ports'] = listening_ports()
    return machine


def known_remote_entries(config):
    try:
        data = json.loads(Path(config['terminal_inventory']).read_text())
        return {key: entry for key, entry in data.get('nodes', {}).items()
                if entry.get('transport') == 'ssh'}
    except (OSError, ValueError, TypeError):
        return {}


def remote_machine(expected_id, entry, host=None):
    host = str(ipaddress.ip_address(host or entry['host']))
    if not re.fullmatch('[A-Za-z_][A-Za-z0-9_-]*', entry['user']):
        raise ValueError('invalid_remote_user')
    node_path = entry['node_id_file']
    dependencies = '\n'.join(inspect.getsource(f) for f in (run, git, sanitized_remote, repository_status, listening_ports))
    payload = '''import json, pathlib, socket, subprocess, uuid, os, re, time, hashlib
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
''' + dependencies + '''
p=pathlib.Path(NODE_FILE)
identity=str(uuid.UUID(p.read_text().strip()))
roots=['/opt/argos-worker','/opt/argos-runtime','/opt/argos','/root/argos','/root/malecns','/opt/argos-data','/root/mukhtar','/opt/argos-roach','/root/output','/root/flyenv']
projects={}
for root in roots:
 d=pathlib.Path(root)
 if d.is_dir(): projects[d.name]=str(d.resolve())
try: addresses=json.loads(subprocess.run(['ip','-j','address','show'],capture_output=True,text=True,timeout=2,check=True).stdout)
except Exception: addresses=[]
repos=[]
for root in projects.values():
 if (pathlib.Path(root)/'.git').exists(): repos.append(repository_status(root))
print(json.dumps({'id':identity,'hostname':socket.gethostname(),'projects':projects,'interfaces':addresses,'repositories':repos,'listening_tcp_ports':listening_ports()}))
'''.replace('NODE_FILE', repr(node_path))
    command = ['ssh', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes', '-o', 'ConnectTimeout=3',
               '-o', 'HostKeyAlias=' + str(entry['host']),
               '-o', 'UserKnownHostsFile=' + entry['known_hosts'], '-i', entry['key'], '-p', str(entry['port']),
               entry['user'] + '@' + host, 'python3', '-']
    raw = json.loads(run(command, timeout=10, input_text=payload))
    if raw.get('id') != expected_id:
        raise ValueError('remote_identity_mismatch')
    now = time.time()
    addresses = [a['local'] for row in raw['interfaces'] for a in row.get('addr_info', []) if a.get('scope') == 'global']
    return {'id': expected_id, 'hostname': raw['hostname'], 'state': 'available', 'last_verified': now,
            'observed_at': now, 'provenance': 'known_ssh:verified_node_id', 'addresses': addresses,
            'interfaces': raw['interfaces'], 'listening_tcp_ports': raw['listening_tcp_ports'],
            'ssh_host': host, 'projects': {name: {'path': path, 'state': 'available', 'last_verified': now,
            'observed_at': now, 'provenance': 'known_ssh:stat'} for name, path in raw['projects'].items()},
            'apis': {}, 'repositories': raw['repositories']}


def remote_candidates(entry, previous):
    """Only configured/successfully verified addresses and DNS of this known host."""
    candidates = [entry.get('host'), previous.get('ssh_host')]
    for name in (entry.get('hostname', ''), previous.get('hostname', '')):
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9.-]{0,252}', name):
            continue
        try:
            candidates.extend(line.split()[0] for line in run(['getent', 'ahostsv4', name], timeout=2).splitlines()[:8])
        except (OSError, RuntimeError, subprocess.TimeoutExpired):
            pass
    candidates.extend(previous.get('addresses', [])[:8])
    result = []
    for value in candidates:
        try:
            address = ipaddress.ip_address(value)
            if not (address.is_unspecified or address.is_loopback or address.is_multicast):
                result.append(str(address))
        except ValueError:
            pass
    return list(dict.fromkeys(result))[:4]


def refresh(*, include_remote=True):
    config = candidate_config()
    path = registry_path()
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock_fd = os.open(path.with_suffix('.lock'), os.O_RDWR | os.O_CREAT, 0o600)
    with os.fdopen(lock_fd, 'w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        previous = read_registry(path)
        local = inspect_machine(config)
        snapshot = {'schema': 1, 'updated_at': time.time(), 'local_id': local['id'], 'machines': {local['id']: local}}
        for kind, key, default in [('argos', 'ARGOS_API_URL', 'http://127.0.0.1:8080'),
                                   ('ollama', 'OLLAMA_HOST', 'http://127.0.0.1:11434'),
                                   ('home_assistant', 'ARGOS_HA_URL', 'http://127.0.0.1:8123'),
                                   ('coral', 'ARGOS_CORAL_URL', '')]:
            candidates = list(dict.fromkeys([u for u in (os.getenv(key, '').strip(), default) if u]))
            observed = []
            for candidate in candidates:
                observation = probe_api(kind, candidate)
                observed.append(observation)
                if observation['state'] == 'available':
                    local['apis'][kind] = dict(observation)
                    break
            if kind not in local['apis']:
                local['apis'][kind] = dict(observed[-1]) if observed else {'url': '', 'state': 'unavailable',
                    'last_verified': 0, 'observed_at': time.time(), 'provenance': 'no_configured_candidate'}
            local['apis'][kind]['candidates'] = observed
        if include_remote:
            for node_id, entry in list(known_remote_entries(config).items())[:4]:
                try:
                    machine = None
                    for host in remote_candidates(entry, previous.get('machines', {}).get(node_id, {})):
                        try:
                            machine = remote_machine(node_id, entry, host)
                            break
                        except (OSError, ValueError, KeyError, RuntimeError, subprocess.TimeoutExpired):
                            continue
                    if machine is None:
                        raise RuntimeError('known_node_unavailable')
                    snapshot['machines'][node_id] = machine
                    machine['roles'] = ['coral'] if (machine['hostname'] == 'argos-coral' or 8770 in machine['listening_tcp_ports']) else []
                    for kind, port in (('coral', 8770), ('ollama', 11434)):
                        if port not in machine['listening_tcp_ports']:
                            machine['apis'][kind] = {'url': 'http://' + machine['ssh_host'] + ':' + str(port), 'state': 'unavailable', 'last_verified': 0,
                                'observed_at': time.time(), 'provenance': 'known_ssh:listening_ports', 'reason': 'not_listening'}
                            continue
                        url = 'http://' + machine['ssh_host'] + ':' + str(port)
                        observation = probe_api(kind, url)
                        observation['provenance'] = 'known_ssh:listen+protocol_health:' + kind
                        machine['apis'][kind] = observation
                    coral = local['apis'].get('coral', {})
                    if urlsplit(coral.get('url', '')).hostname in machine['addresses']:
                        if coral.get('state') == 'available':
                            machine['apis']['coral'] = coral
                        del local['apis']['coral']
                except (OSError, ValueError, KeyError, RuntimeError, subprocess.TimeoutExpired):
                    stale = dict(previous.get('machines', {}).get(node_id, {}))
                    stale.update(id=node_id, state='unavailable', observed_at=time.time(), provenance='known_ssh',
                                 reason='connection_or_identity_failed')
                    for category in ('projects', 'apis'):
                        for value in stale.get(category, {}).values():
                            value['state'] = 'stale'
                    snapshot['machines'][node_id] = stale
        for node_id, machine in snapshot['machines'].items():
            old = previous.get('machines', {}).get(node_id, {})
            machine['retired'] = old.get('retired', [])[-48:]
            for category, field in (('projects', 'path'), ('apis', 'url')):
                for name, entry in old.get(category, {}).items():
                    current = machine.get(category, {}).get(name, {})
                    if entry.get(field) and entry.get(field) != current.get(field):
                        machine['retired'].append({**entry, 'name': name, 'kind': category, 'state': 'stale'})
            unique = {(entry.get('kind'), entry.get('name'), entry.get('path', entry.get('url'))): entry
                      for entry in machine['retired']}
            machine['retired'] = list(unique.values())[-48:]
        write_registry(snapshot, path)
        snapshot['memory_publication'] = publish_memory(snapshot)
        write_registry(snapshot, path)
        return snapshot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['status', 'refresh', 'resolve', 'sync'])
    parser.add_argument('name', nargs='?')
    parser.add_argument('--kind', choices=['path', 'api'], default='path')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--local-only', action='store_true')
    parser.add_argument('--machine', help='Known stable machine id for resolution')
    parser.add_argument('--summary', action='store_true', help='Print counts, not the private map')
    args = parser.parse_args()
    if args.action == 'refresh':
        result = refresh(include_remote=not args.local_only)
    elif args.action == 'status':
        result = read_registry()
    elif args.action == 'resolve':
        from src.runtime_registry import resolve_api, resolve_path
        result = (resolve_api if args.kind == 'api' else resolve_path)(args.name, machine_id=args.machine)
    else:
        snapshot = read_registry()
        local = snapshot.get('machines', {}).get(snapshot.get('local_id'), {})
        repository = next((row for row in local.get('repositories', []) if row.get('id') == args.name), None)
        if repository is None:
            raise ValueError('Unknown local repository id')
        result = sync_repository(repository['path'], apply=args.apply, expected=repository)
    if args.summary and isinstance(result, dict) and 'machines' in result:
        result = {'schema': result['schema'], 'updated_at': result['updated_at'],
                  'machines': len(result['machines']), 'memory_publication': result.get('memory_publication', {})}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
