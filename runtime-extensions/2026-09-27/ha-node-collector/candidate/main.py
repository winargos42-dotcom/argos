#!/usr/bin/env python3
"""Home Assistant diagnostics for the two verified physical ARGOS nodes."""
import argparse
import json
import os
from pathlib import Path
import signal
import socket
import stat
import threading
import time

from collectors import collect_coral, collect_runtime
from publisher import BRIDGE_TOPIC, Bridge

NODES = [
    {'id': '6e5e1e1f-1c33-4173-8158-2ae39d0875cb', 'name': 'ARGOS X230', 'kind': 'runtime'},
    {'id': '3e124287-3312-4249-bd66-868d0f9fe08c', 'name': 'ARGOS Coral accelerator API', 'kind': 'coral_accel'},
]
PASSWORD_FILE = Path('/etc/argos/mqtt-nodes.pass')
STATE_FILE = Path('/var/lib/argos-ha-nodes/status.json')


def secret(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as source:
        info = os.fstat(source.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid() or info.st_mode & 0o077:
            raise ValueError('invalid credential file')
        value = source.read(1025).strip()
    if not 32 <= len(value) <= 1024 or any(c in value for c in (b'\n', b'\r', b'\x00')):
        raise ValueError('invalid credential')
    return value.decode('ascii')


def observe(node):
    if node == NODES[0]:
        return {**collect_runtime('http://127.0.0.1:8080/health'), 'node_id': node['id']}
    if node == NODES[1]:
        return collect_coral(node['id'])
    raise ValueError('unknown node')


def save_state(observations):
    # Unit StateDirectory owns this directory. No credentials/raw envelopes.
    temporary = STATE_FILE.with_suffix('.tmp')
    with temporary.open('w') as target:
        json.dump({'updated_at': time.time(), 'observations': observations}, target, allow_nan=False)
        target.flush()
        os.fsync(target.fileno())
    temporary.replace(STATE_FILE)


def finish(client, bridge):
    try:
        bridge.shutdown()
    except Exception:
        pass
    delivered = False
    try:
        pending = client.publish(BRIDGE_TOPIC, 'OFFLINE', qos=1, retain=True)
        pending.wait_for_publish(timeout=3)
        delivered = pending.is_published()
    except Exception:
        pass
    if delivered:
        client.disconnect()
    else:
        # Without final OFFLINE delivery, preserve the broker's last will.
        sock = client.socket()
        if sock is not None:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
    client.loop_stop()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--observe', action='store_true', help='Read-only current probes; no MQTT publication')
    args = parser.parse_args()
    if args.observe:
        print(json.dumps({node['id']: observe(node) for node in NODES}, ensure_ascii=False, allow_nan=False))
        return
    import paho.mqtt.client as mqtt
    os.umask(0o077)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id='argos-ha-node-diagnostics',
                         clean_session=True, protocol=mqtt.MQTTv311)
    client.username_pw_set('argos-nodes', secret(PASSWORD_FILE))
    client.will_set(BRIDGE_TOPIC, 'OFFLINE', qos=1, retain=True)
    client.max_queued_messages_set(32)
    client.max_inflight_messages_set(8)
    client.reconnect_delay_set(1, 15)
    stop, refresh = threading.Event(), threading.Event()

    def publish(topic, payload):
        # Paho does not queue QoS0 for replay after a reconnect.
        info = client.publish(topic, payload, qos=0, retain=True)
        if info.rc != mqtt.MQTT_ERR_SUCCESS:
            raise ConnectionError('MQTT publication unavailable')

    bridge = Bridge(NODES, publish)

    def on_connect(_client, _userdata, _flags, reason, _properties):
        if stop.is_set():
            return
        if reason.is_failure:
            bridge.disconnect()
            return
        try:
            bridge.connect()
            client.subscribe('homeassistant/status', qos=0)
            refresh.set()
        except Exception:
            bridge.disconnect()
            stop.set()  # systemd restarts after a failed publication.
            refresh.set()

    def on_disconnect(_client, _userdata, _flags, _reason, _properties):
        bridge.disconnect()

    def on_message(_client, _userdata, message):
        if not stop.is_set() and message.topic == 'homeassistant/status' and message.payload == b'online':
            try:
                bridge.connect()  # invalidate in-flight observations after HA restart
                refresh.set()
            except Exception:
                bridge.disconnect()
                stop.set()
                refresh.set()

    client.on_connect, client.on_disconnect, client.on_message = on_connect, on_disconnect, on_message
    for signum in (signal.SIGTERM, signal.SIGINT):
        signal.signal(signum, lambda *_: (stop.set(), refresh.set()))
    client.connect_async('127.0.0.1', 1883, keepalive=20)
    client.loop_start()
    try:
        while not stop.is_set():
            epoch = bridge.snapshot()
            if epoch is not None:
                observations = {}
                for node in NODES:
                    if stop.is_set():
                        break
                    started = time.monotonic()
                    result = observe(node)
                    if bridge.update(node, result, epoch, started):
                        observations[node['id']] = result
                save_state(observations)
            refresh.wait(20)
            refresh.clear()
    finally:
        stop.set()
        finish(client, bridge)


if __name__ == '__main__':
    main()
