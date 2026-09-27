"""Read-only node collectors. No core imports, inference, discovery or commands."""
import http.client
import importlib.util
import json
import math
import os
from pathlib import Path
import socket
import stat
import threading
import time
import uuid
from urllib.parse import urlsplit

AUTH_MODULE = Path('/home/argos-data/runtime/app/src/connectivity/p2p_auth.py')
BUDGET = 3.0

# New signed accelerator source; the legacy P2P helper is not used by main.
from coral_collector import collect_coral


def failed(role, code):
    code = {'invalid_target': 'not_configured', 'invalid_identity': 'not_configured',
            'auth_configuration': 'not_configured', 'http_status': 'invalid_response',
            'response_too_large': 'invalid_response', 'identity_mismatch': 'unauthenticated',
            'invalid_authenticated_response': 'unauthenticated', 'unavailable': 'unreachable'}.get(code, code)
    return {'connected': False, 'service_ready': False, 'role': role, 'error': code}


def collect_runtime(url):
    connection = timer = None
    try:
        parsed = urlsplit(url)
        if (parsed.scheme != 'http' or parsed.hostname != '127.0.0.1'
                or parsed.username is not None or parsed.password is not None
                or parsed.path != '/health' or parsed.query or parsed.fragment
                or parsed.port != 8080):
            return failed('gateway', 'invalid_target')
        until = time.monotonic() + BUDGET
        connection = http.client.HTTPConnection('127.0.0.1', parsed.port or 80, timeout=BUDGET)
        connection.connect()
        remaining = until - time.monotonic()
        if remaining <= 0:
            raise TimeoutError()
        sock = connection.sock
        sock.settimeout(remaining)

        def abort():
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

        timer = threading.Timer(remaining, abort)
        timer.daemon = True
        timer.start()
        connection.request('GET', '/health', headers={'Connection': 'close'})
        response = connection.getresponse()
        if response.status != 200:
            return failed('gateway', 'http_status')
        data = response.read(16385)
        if len(data) > 16384:
            return failed('gateway', 'response_too_large')
        if time.monotonic() >= until:
            raise TimeoutError()
        value = json.loads(data)
        if not isinstance(value, dict):
            return failed('gateway', 'invalid_response')
        uptime = value.get('uptime_seconds')
        if (value.get('ok') is not True or type(value.get('ready')) is not bool
                or type(uptime) not in (int, float) or not math.isfinite(uptime) or uptime < 0):
            return failed('gateway', 'invalid_response')
        return {'connected': True, 'service_ready': value['ready'] and value.get('error') is None,
                'role': 'gateway', 'uptime_seconds': uptime}
    except (TimeoutError, socket.timeout):
        return failed('gateway', 'timeout')
    except Exception:
        return failed('gateway', 'unavailable')
    finally:
        if timer:
            timer.cancel()
            timer.join(timeout=.2)
        if connection:
            connection.close()


def _auth(path, key_file):
    path = Path(path)
    if path != AUTH_MODULE or path.resolve() != path:
        raise ValueError('module')
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
        raise ValueError('module')
    key_path = Path(key_file)
    if not key_path.is_absolute() or key_path.resolve() != key_path:
        raise ValueError('key')
    spec = importlib.util.spec_from_file_location('_ha_nodes_p2p_auth', path)
    module = importlib.util.module_from_spec(spec)
    # Load this one trusted source without creating a __pycache__ in the live app.
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)

    fd = os.open(key_path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid()
                or info.st_mode & 0o077 or info.st_size > 4096):
            raise ValueError('key')
        key = stream.read(4097).strip()
    if not 32 <= len(key) <= 4096 or key.lower() in (b'argos_default_secret', b'change_me', b'changeme'):
        raise ValueError('key')
    return module, module.Auth(key)


def collect_p2p(host, port, key_file, auth_module, expected_node_id):
    try:
        if host != '192.168.1.94' or type(port) is not int or port != 55771:
            return failed('worker', 'invalid_target')
        if str(uuid.UUID(expected_node_id)) != expected_node_id:
            return failed('worker', 'invalid_identity')
    except (ValueError, TypeError, AttributeError):
        return failed('worker', 'invalid_identity')
    try:
        module, auth = _auth(auth_module, key_file)
    except Exception:
        return failed('worker', 'auth_configuration')
    try:
        until = time.monotonic() + BUDGET
        packet = auth.pack('request', {'action': 'status'})
        with socket.create_connection((host, port), timeout=BUDGET) as sock:
            remaining = until - time.monotonic()
            if remaining <= 0:
                raise TimeoutError()
            sock.settimeout(remaining)
            module.send_frame(sock, packet)
            remaining = until - time.monotonic()
            if remaining <= 0:
                raise TimeoutError()
            response = module.recv_frame(sock, seconds=remaining)
            profile = auth.verify(response, 'response', reply_to=packet['nonce'])
            if time.monotonic() >= until:
                raise TimeoutError()
        if profile.get('node_id') != expected_node_id or profile.get('role') != 'worker':
            return failed('worker', 'identity_mismatch')
        return {'connected': True, 'service_ready': True, 'role': 'worker',
                'node_id': expected_node_id, 'authenticated': True,
                'capability': 'authenticated_status', 'inference_configured': False}
    except (TimeoutError, socket.timeout):
        return failed('worker', 'timeout')
    except (ValueError, TypeError, KeyError, RecursionError):
        return failed('worker', 'invalid_authenticated_response')
    except Exception:
        return failed('worker', 'unavailable')
