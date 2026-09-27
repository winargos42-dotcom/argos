"""Publish current diagnostics, refusing results from previous connections."""
import json
import math
import threading
import time

from entities import discovery, normalize_state

BRIDGE_TOPIC = 'argos/nodes/bridge/availability'
MAX_AGE = 60.0


class Bridge:
    def __init__(self, nodes, publish, clock=time.monotonic):
        self.nodes = {node['id']: dict(node) for node in nodes}
        if len(self.nodes) != len(nodes):
            raise ValueError('duplicate node')
        self.configs = {key: discovery(node) for key, node in self.nodes.items()}
        self.publish, self.clock = publish, clock
        self.lock = threading.RLock()
        self.online, self.epoch = False, 0

    def connect(self):
        with self.lock:
            self.epoch += 1
            self.online = True
            for key in self.nodes:
                self.publish(f'argos/nodes/{key}/availability', 'OFFLINE')
            for configs in self.configs.values():
                for topic, config in configs.items():
                    self.publish(topic, json.dumps(config, ensure_ascii=False, allow_nan=False))
            self.publish(BRIDGE_TOPIC, 'ONLINE')
            return self.epoch

    def disconnect(self):
        with self.lock:
            self.epoch += 1
            self.online = False

    def snapshot(self):
        with self.lock:
            return self.epoch if self.online else None

    def update(self, node, observation, epoch, observed_at):
        with self.lock:
            if not self.online or epoch != self.epoch or self.nodes.get(node.get('id')) != node:
                return False
            topic = f"argos/nodes/{node['id']}"
            age = self.clock() - observed_at
            if not math.isfinite(age) or not 0 <= age <= MAX_AGE:
                self.publish(topic + '/availability', 'OFFLINE')
                return False
            state = normalize_state(observation)
            self.publish(topic + '/state', json.dumps(state, ensure_ascii=False, allow_nan=False))
            self.publish(topic + '/availability', 'ONLINE' if state['connected'] is True else 'OFFLINE')
            return True

    def shutdown(self):
        with self.lock:
            if self.online:
                for key in self.nodes:
                    self.publish(f'argos/nodes/{key}/availability', 'OFFLINE')
                self.publish(BRIDGE_TOPIC, 'OFFLINE')
            self.disconnect()
