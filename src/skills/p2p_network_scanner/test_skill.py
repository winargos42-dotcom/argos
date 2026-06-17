"""Юнит-тесты для навыка p2p_network_scanner."""

import json
import os
import sys
import tempfile
import unittest
from collections import deque

# Ensure argoss source is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.event_bus import Events, get_bus
from src.skills.p2p_network_scanner.skill import (
    DEFAULT_NODES,
    P2PNetworkSkill,
    NodeState,
    _parse_nodes_env,
    _validate_node,
)

# Module-level constants were moved to class attributes.
HISTORY_FILE = P2PNetworkSkill.HISTORY_FILE


class TestNodeValidation(unittest.TestCase):
    def test_tuple_ok(self):
        self.assertEqual(_validate_node(("192.168.1.1", 5001)), ("192.168.1.1", 5001))

    def test_list_ok(self):
        self.assertEqual(_validate_node(["host", 80]), ("host", 80))

    def test_dict_ok(self):
        self.assertEqual(_validate_node({"host": "h", "port": 8080}), ("h", 8080))

    def test_empty_host(self):
        with self.assertRaises(ValueError):
            _validate_node({"host": "", "port": 80})

    def test_port_out_of_range(self):
        with self.assertRaises(ValueError):
            _validate_node(("h", 70000))

    def test_invalid_port_type(self):
        with self.assertRaises(ValueError):
            _validate_node(("h", "abc"))


class TestEnvParsing(unittest.TestCase):
    def test_csv(self):
        self.assertEqual(_parse_nodes_env("a:1,b:2"), [("a", 1), ("b", 2)])

    def test_json_pairs(self):
        self.assertEqual(_parse_nodes_env('[["a", 1], ["b", 2]]'), [("a", 1), ("b", 2)])

    def test_json_objects(self):
        self.assertEqual(
            _parse_nodes_env('[{"host": "a", "port": 1}, {"host": "b", "port": 2}]'),
            [("a", 1), ("b", 2)],
        )


class TestNodeState(unittest.TestCase):
    def test_update_and_history(self):
        s = NodeState("h", 80)
        self.assertFalse(s.update({"online": False, "status": None, "code": None, "error": "x"}))
        self.assertFalse(s.update({"online": False, "status": None, "code": None, "error": "x"}))
        self.assertTrue(s.update({"online": True, "status": "OK", "code": 200, "error": None}))
        self.assertEqual(len(s.history), 3)


class TestP2PNetworkSkill(unittest.TestCase):
    def setUp(self):
        self.bus = get_bus()
        self.captured = []
        self._handler = self._capture
        self.bus.subscribe(Events.P2P_NODE_JOINED, self._handler)
        self.bus.subscribe(Events.P2P_NODE_LEFT, self._handler)

        # Do not touch the real history file; just point skill to temp path.
        self.history_fd, self.history_path = tempfile.mkstemp(suffix=".json")
        os.close(self.history_fd)

    def tearDown(self):
        self.bus.unsubscribe(Events.P2P_NODE_JOINED, self._handler)
        self.bus.unsubscribe(Events.P2P_NODE_LEFT, self._handler)
        if os.path.exists(self.history_path):
            os.remove(self.history_path)

    def _capture(self, event):
        self.captured.append((event.type, event.payload.get("host"), event.payload.get("port")))

    def _make_skill(self, nodes, results):
        skill = P2PNetworkSkill(nodes=nodes)
        skill.HISTORY_FILE = self.history_path
        skill.check_fn = lambda host, port, timeout: results.get((host, port), {"online": False, "error": "unknown"})
        return skill

    def test_scan_emits_joined(self):
        skill = self._make_skill([("a", 1)], {("a", 1): {"online": True, "status": "OK", "code": 200, "error": None}})
        skill.execute("")
        self.assertIn(("p2p.node_joined", "a", 1), self.captured)

    def test_scan_emits_left(self):
        skill = self._make_skill(
            [("a", 1)],
            {
                ("a", 1): {"online": True, "status": "OK", "code": 200, "error": None},
            },
        )
        skill.execute("")
        self.captured.clear()
        skill.check_fn = lambda host, port, timeout: {"online": False, "status": None, "code": None, "error": "down"}
        skill.execute("")
        self.assertIn(("p2p.node_left", "a", 1), self.captured)

    def test_summary_counts(self):
        skill = self._make_skill(
            [("a", 1), ("b", 2)],
            {
                ("a", 1): {"online": True, "status": "OK", "code": 200, "error": None},
                ("b", 2): {"online": False, "status": None, "code": None, "error": "x"},
            },
        )
        skill.execute("")
        summary = skill.summary()
        self.assertEqual(summary["total_nodes"], 2)
        self.assertEqual(summary["online"], 1)
        self.assertEqual(summary["offline"], 1)

    def test_history_saved(self):
        skill = self._make_skill([("a", 1)], {("a", 1): {"online": True, "status": "OK", "code": 200, "error": None}})
        skill.execute("")
        self.assertTrue(os.path.exists(self.history_path))
        with open(self.history_path, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["host"], "a")


if __name__ == "__main__":
    unittest.main()
