#!/usr/bin/env python3
"""Integration test для recovered модулей ARGOS"""
import sys, os
PROJECT_ROOT = os.path.expanduser("~/Projects/argoss")
sys.path.insert(0, PROJECT_ROOT)

from src.principles.topology_id import RelationalIdentity
from src.principles.audit_procedure import ProceduralAudit
from src.principles.open_loop_ctl import OpenLoopPredictor
from src.principles.convergent_fsm import ConvergentFSM
from src.mcp.cache_layer import MCPCache
from src.integrations.conflict_aggregator import ConflictAggregator, ConflictReport
from src.integrations.circuit_breaker import CircuitBreaker, CircuitBreakerOpen, cb_providers
from src.integrations.anomaly_detector import AnomalyDetector
from src.integrations.esports_tracker import EsportsTracker
from src.memory.obsidian_indexer import ObsidianIndexer
import numpy as np

errors = []
success = []

# 1. topology_id
a = RelationalIdentity.compute_fingerprint([("n1", 0.5), ("n2", 0.3)])
b = RelationalIdentity.compute_fingerprint([("n2", 0.3), ("n1", 0.5)])
assert a == b, "fingerprint order invariant failed"
success.append("topology_id.compute_fingerprint")

# 2. audit
audit = ProceduralAudit()
ts = audit.log_context("test_001", {"truth": 1.0}, {"risk": "low"}, "test")
assert ts > 0
success.append("audit_procedure.log_context")

# 3. open_loop
predictor = OpenLoopPredictor([1.0, 2.0], np.array([[0.1]]))
seq = predictor.compute_sequence(np.zeros(1), 5)
assert len(seq) == 5
success.append("open_loop_ctl.compute_sequence")

# 4. convergent_fsm
def transition(x):
    return x * 0.5
fsm = ConvergentFSM(1.0, transition, tol=1e-4)
result = fsm.run()
assert abs(result) < 0.01
success.append("convergent_fsm.run")

# 5. cache
cache = MCPCache()
cache.set("q1", "fp1", {"text": "hello"}, "known", level=1)
assert cache.get("q1", "fp1") is not None
success.append("mcp_cache.set_get")

# 6. conflict aggregator
agg = ConflictAggregator()
res = agg.analyze({"p1": {"epistemic": "known"}, "p2": {"epistemic": "known_gap"}})
assert len(res) == 1 and res[0].severity == "high"
success.append("conflict_aggregator.analyze")

# 7. circuit breaker
cb = CircuitBreaker("test", failure_threshold=2)
try:
    cb.call(lambda: (_ for _ in ()).throw(Exception("fail")))
except Exception:
    pass
try:
    cb.call(lambda: (_ for _ in ()).throw(Exception("fail")))
except Exception:
    pass
try:
    cb.call(lambda: "OK")
    assert False, "should be open"
except CircuitBreakerOpen:
    success.append("circuit_breaker.open_state")

# 8. anomaly detector (partial, mock)
ad = AnomalyDetector("", "", "test")
status = ad.run_detection_cycle()
assert status.get("status") == "clean"
success.append("anomaly_detector.clean_cycle")

# 9. obsidian indexer
idx = ObsidianIndexer("/tmp/test_vault")
links = idx.link_note("/tmp/test_vault/note1.md", "#tag1 content here")
success.append("obsidian_indexer.link_note")

# Report
print(f"=== RECOVERED MODULES TEST ===")
print(f"Success: {len(success)}/{len(success)+len(errors)}")
for s in success:
    print(f"  ✅ {s}")
for e in errors:
    print(f"  ❌ {e}")
print(f"================================")
