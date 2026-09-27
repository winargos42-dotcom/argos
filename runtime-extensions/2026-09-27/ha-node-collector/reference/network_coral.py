"""Bounded, signed Coral LAN transport. No proxy, redirects, retries or LLM fallback."""
from __future__ import annotations

import hashlib
import hmac
import http.client
import ipaddress
import json
import math
import os
import socket
import stat
import threading
import time
import uuid
from urllib.parse import urlsplit

MAX_RESPONSE = 1024 * 1024
MAX_IMAGE = 4 * 1024 * 1024
MODELS = frozenset(('objects', 'faces', 'classify'))


class CoralError(RuntimeError):
    pass


def strict_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate field')
        result[key] = value
    return result


def finite(value, low=0, high=1e12):
    return type(value) in (int, float) and math.isfinite(value) and low <= value <= high


def dimensions(value):
    return isinstance(value, list) and len(value) == 2 and all(type(v) is int and 1 <= v <= 20000 for v in value)


def validate_status(data):
    if not isinstance(data, dict) or data.get('ok') is not True or not finite(data.get('uptime_s')):
        raise CoralError('Coral status invalid')
    models = data.get('models')
    if not isinstance(models, dict) or len(models) > 16:
        raise CoralError('Coral models invalid')
    clean = {}
    for name, model in models.items():
        if name not in MODELS:
            continue
        if (not isinstance(model, dict) or type(model.get('tpu')) is not bool
                or type(model.get('calls')) is not int or model['calls'] < 0
                or not dimensions(model.get('input'))
                or 'avg_ms' not in model or (model['avg_ms'] is not None and not finite(model['avg_ms']))
                or (name == 'classify' and model.get('kind') != 'classify')):
            raise CoralError('Coral model metadata invalid')
        clean[name] = {k: model[k] for k in ('tpu', 'calls', 'input', 'avg_ms')}
        if name == 'classify':
            clean[name]['kind'] = 'classify'
    return {'ok': True, 'uptime_s': data['uptime_s'], 'models': clean}


def validate_inference(data, model):
    if (model not in MODELS or not isinstance(data, dict) or data.get('model') != model
            or data.get('tpu') is not True or not finite(data.get('inference_ms'), high=120000)):
        raise CoralError('Coral inference invalid')
    key = 'labels' if model == 'classify' else 'objects'
    rows = data.get(key)
    if not isinstance(rows, list) or len(rows) > (5 if model == 'classify' else 20):
        raise CoralError('Coral result count invalid')
    if key == 'objects' and not dimensions(data.get('image')):
        raise CoralError('Coral image dimensions invalid')
    clean = []
    for row in rows:
        if (not isinstance(row, dict) or not isinstance(row.get('label'), str)
                or not 1 <= len(row['label']) <= 256 or not finite(row.get('score'), high=1)):
            raise CoralError('Coral result invalid')
        item = {'label': ''.join(c for c in row['label'] if c.isprintable())[:96], 'score': row['score']}
        if key == 'objects':
            box = row.get('box')
            width, height = data['image']
            if (type(row.get('class_id')) is not int or not 0 <= row['class_id'] <= 100000
                    or not isinstance(box, list) or len(box) != 4
                    or not all(finite(v, high=20000) for v in box)
                    or not 0 <= box[0] <= box[2] <= width or not 0 <= box[1] <= box[3] <= height):
                raise CoralError('Coral box invalid')
            item.update(class_id=row['class_id'], box=box)
        clean.append(item)
    result = {'model': model, 'tpu': True, 'inference_ms': data['inference_ms'], key: clean}
    if key == 'objects':
        result['image'] = data['image']
    return result


class CoralClient:
    def __init__(self, url, key, *, timeout=3.0, connection_factory=http.client.HTTPConnection, clock=time.monotonic):
        parsed = urlsplit(url)
        address = ipaddress.ip_address(parsed.hostname)
        port = 80 if parsed.port is None else parsed.port
        if (parsed.scheme != 'http' or not (address.is_private and not address.is_unspecified and not address.is_multicast)
                or parsed.username is not None or parsed.password is not None or parsed.path not in ('', '/')
                or parsed.query or parsed.fragment or not 1 <= port <= 65535
                or not isinstance(key, bytes) or not 32 <= len(key) <= 4096
                or not finite(timeout, low=0.1, high=10)):
            raise ValueError('Invalid Coral configuration')
        self.host, self.port, self.key = str(address), port, key
        self.timeout, self.connection_factory, self.clock = timeout, connection_factory, clock

    @classmethod
    def from_env(cls):
        from src.runtime_registry import api_url
        configured = os.environ.get('ARGOS_CORAL_URL', '').strip()
        # Keep a configured client alive across offline -> available refreshes.
        # _call always resolves again and never sends to an unverified old URL.
        url = api_url('coral', configured) or configured
        path = os.environ.get('ARGOS_CORAL_SECRET_FILE', '').strip()
        if not url or not path:
            return None
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
        with os.fdopen(fd, 'rb') as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid() or info.st_mode & 0o077:
                raise ValueError('Invalid Coral credential permissions')
            key = stream.read(4097).strip()
        instance = cls(url, key)
        instance._follow_registry = True
        return instance

    def _call(self, method, target, body=b''):
        if getattr(self, '_follow_registry', False):
            from src.runtime_registry import api_url
            url = api_url('coral', os.environ.get('ARGOS_CORAL_URL', '').strip())
            if not url:
                raise CoralError('Coral endpoint unavailable in current registry')
            try:
                current = type(self)(url, self.key, timeout=self.timeout)
            except (TypeError, ValueError):
                raise CoralError('Coral endpoint invalid in current registry') from None
            host, port = current.host, current.port
            self.host, self.port = host, port
        else:
            host, port = self.host, self.port
        if len(body) > MAX_IMAGE:
            raise CoralError('Coral image too large')
        timestamp, nonce = f'{time.time():.3f}', uuid.uuid4().hex
        digest = hashlib.sha256(body).hexdigest()
        message = '\n'.join(('argos-coral-v1', method, target, timestamp, nonce, digest)).encode()
        headers = {'X-Argos-Ts': timestamp, 'X-Argos-Nonce': nonce,
                   'X-Argos-Mac': hmac.new(self.key, message, hashlib.sha256).hexdigest(),
                   'Content-Type': 'application/octet-stream'}
        connection = self.connection_factory(host, port, timeout=self.timeout)
        response = None
        deadline = self.clock() + self.timeout
        owned_sockets = []
        def abort():
            # A per-read timeout alone does not bound slow trickling HTTP headers.
            # This watchdog touches only this request's connection/socket.
            for transport in owned_sockets:
                try:
                    transport.shutdown(socket.SHUT_RDWR)
                except (OSError, AttributeError):
                    pass
                try:
                    transport.close()
                except (OSError, AttributeError):
                    pass
            connection.close()
        watchdog = threading.Timer(self.timeout, abort)
        watchdog.daemon = True
        def remaining():
            value = deadline - self.clock()
            if value <= 0:
                raise CoralError('Coral deadline exceeded')
            return value
        try:
            watchdog.start()
            connection.connect()
            transport = connection.sock
            owned_sockets.append(transport)
            transport.settimeout(remaining())
            connection.request(method, target, body, headers)
            transport.settimeout(remaining())
            response = connection.getresponse()
            if response.status != 200:
                raise CoralError('Coral HTTP status rejected')
            raw = bytearray()
            while True:
                transport.settimeout(remaining())
                chunk = response.read1(min(65536, MAX_RESPONSE + 1 - len(raw)))
                if not chunk:
                    break
                raw.extend(chunk)
                if len(raw) > MAX_RESPONSE:
                    raise CoralError('Coral response too large')
                # HTTP/1.0 + Content-Length can close the final response file
                # reference as soon as read1 consumes the last bytes. Do not
                # touch that now-closed socket merely to discover EOF again.
                if response.isclosed():
                    break
            remaining()
            expected = hmac.new(self.key, '\n'.join(('argos-coral-v1-resp', nonce, str(response.status),
                                hashlib.sha256(raw).hexdigest())).encode(), hashlib.sha256).hexdigest()
            mac = response.getheader('X-Argos-Mac')
            if not isinstance(mac, str) or not hmac.compare_digest(expected, mac):
                raise CoralError('Coral response signature rejected')
            data = json.loads(raw.decode('utf-8'), object_pairs_hook=strict_pairs,
                              parse_constant=lambda _: (_ for _ in ()).throw(ValueError('Invalid constant')))
            remaining()
            return data
        except Exception:
            raise CoralError('Coral response unavailable or invalid') from None
        finally:
            watchdog.cancel()
            if watchdog.ident is not None:
                watchdog.join(timeout=1)
            if response is not None:
                # HTTP/1.0 may detach this response from HTTPConnection. Close
                # its file reference explicitly even for partial/error bodies.
                try:
                    response.close()
                except OSError:
                    pass
            connection.close()

    def status(self):
        return validate_status(self._call('GET', '/v1/status'))

    def infer(self, image, model):
        if model not in MODELS or not isinstance(image, bytes) or not image or len(image) > MAX_IMAGE:
            raise CoralError('Invalid Coral inference request')
        target = ('/v1/classify?model=classify&threshold=0.10&top_k=5' if model == 'classify'
                  else f'/v1/detect?model={model}&threshold=0.40&top_k=20')
        return validate_inference(self._call('POST', target, image), model)
