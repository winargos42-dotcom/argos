# SNN worker v2 — directed recurrence repair, 2026-09-27

This is an isolated repair of the real MaleCNS ARC bridge. It is **not a trained
ARC agent**, and no ARC performance improvement is claimed. The live old worker,
training processes, runtime defaults, Git and Hugging Face were not modified.

## What was proved and repaired

The frozen live source is `snn_rank_worker.py`, SHA256
`0fee7c638a513eb5bfc7d48760c2bf86502cb0a1e4d5d2d43ed488d0cf64ace3`.
Canonical evidence is copied under `canonical/`: `model.py` computes
`recurrent = sparse.mm(CSR, spikes.T).T`; `sparse_mm.py` has the same forward
operator and its gradient explicitly identifies row as receiving neuron and
column as transmitting neuron. `sparse_mm_fast.py` calls transpose CSR columns
postsynaptic IDs grouped by presynaptic cell.

Three functional tests fail against the actual old Torch worker:

1. An edge 0 → 1 cannot activate the uninjected neuron 1 because the old
   `scatter_add_(col, weights * spikes[col])` accumulates back at the sender.
2. `layer_from([0])` returns the incoming neuron 2 in the fixture 2 → 0 → 1,
   rather than downstream neuron 1.
3. A two-neuron cycle becomes three local entries due to concatenation without
   uniqueness; lookup and searchsorted then disagree about duplicated indices.

`snn_rank_worker_v2.py` fixes these with actual CSR matrix multiplication,
downstream row selection by absolute incoming weight from selected presynaptic
cells, and a unique induced graph with a single global-to-local map. Inhibitory
weights retain their sign in dynamics. Sparse tensor invariants are checked at
construction. Local node identities and readout body IDs are reported.

`red-old-evidence.json` preserves the three expected failures. The last execution
is recorded in `remote-checks.json`; `checkpoint-smoke.json` contains full raw
inputs, outputs, timings, source hashes and checkpoint provenance.

## Real checkpoint and scope

Checkpoint: `/root/output/male_cns_spikewhale.pt` on Coral, 315,527,837 bytes,
SHA256 `b381422e88d41ad3525f63284815784b3bbadfe32b59d8166986f92d7083f6fb`.
It contains 167,565 neurons and 25,623,478 edges, anatomical weights, identity and
configuration. No trained ARC adapter or action head is in this artifact.

The production interpreter was found in the existing ARC launcher:
`/root/flyenv/bin/python` (Python 3.11, Torch 2.14.0+cpu). A bounded process scan
found no running `snn_rank_worker` at inspection time; it did not stop anything.

The v2 checkpoint loader verifies SHA256 before safe `weights_only=True`
deserialization and rechecks it afterwards. It refuses a changed checkpoint.
It keeps the old bridge input selection/order, injection `tanh(features / 64)`,
40 ticks, final 15-tick rate window, beta 0.9, threshold 1, and **explicit bridge
synapse scale 0.05**. The checkpoint configuration says 0.01. The canonical full
ConnectomeSNN also uses a different same-step threshold/reset convention. This
patch intentionally does **not** calibrate these differences; the v2 provenance
labels its scope as the legacy bridge timing and scale. It is an anatomical
subgraph computation, not a faithful simulation of the entire canonical model.

## Measurements

The canonical checkpoint matvec and an independent NumPy row-sum oracle matched
exactly across all 167,565 outputs (max absolute error 0), with 22,776 receiving
cells affected by three selected input cells.

The old graph had 30,160 entries but only 22,002 unique global neurons, i.e. 8,158
duplicates. V2 has 20,817 unique neurons and 3,839,161 edges; old native graph has
5,315,308 edges, including the effects of duplicated rows.

Four fixed synthetic feature vectors were run from zero state. The isolated
ablation runs the **old recurrence on the identical v2 graph and readout**, so
these deltas compare matching neuron coordinates:

| Input | Max absolute readout change, old operator → CSR |
|---|---:|
| All zero | 0 |
| All 64 | 0.761594 |
| First input 64, others zero | 0 |
| Linear ramp −64 to 128 | 0.695026 |

The complete native old graph was also run with the same vectors, but it has
different readout neurons. Do **not** compare its output components as if they
were aligned with v2. Raw outputs remain in the report for inspection.

Final measured v2 latency was 0.67–0.72 seconds/vector, old native 3.67–3.81
seconds/vector, one Torch CPU thread. The complete comparison and protocol
probe took 47.28 seconds, process peak RSS 889 MiB; this peak includes allocations
for both graphs/checkpoint comparisons. The later standalone deployment probe
peaked at 725.6 MiB. The old/native speed comparison includes a different graph
size. On the identical v2 graph, the old operator took 2.67–2.78 seconds/vector.
These are four local smoke timings, not a performance benchmark distribution.

## Protocol and limits

- `ping` → `{"pong":1}` (legacy compatibility).
- `{"vecs":[[160 finite numbers]],"diag":true}` → `readout`, optional `diag`.
- `{"op":"info"}` → checkpoint/graph/source provenance and request limits.
- At most 16 vectors/request, exactly 160 numeric features/vector, `|x| <= 1e6`.
- 262,144 characters/line; oversized lines are drained, then the next request is
  accepted. Malformed JSON, null, wrong dimensions, strings/bools and non-finite
  values return JSON errors. The whole request is validated before inference.
- Exact-key LRU cache, 128 entries; no six-decimal rounding alias.
- Production main uses one Torch CPU thread, 40 ticks/vector, no network access.

Actual subprocess verification sends four invalid requests, then ping, a valid
160-feature batch and info. It exits successfully with seven responses; subsequent
valid inference remains available. No server is started automatically.

## Reproduce

Mathematical/protocol tests (NumPy required; Torch parity is explicitly skipped
if Torch is absent):

```bash
python -m unittest test_snn_v2 -v
```

The frozen old worker's three functional regressions intentionally fail:

```bash
python reproduce_old_regressions.py
```

With the known checkpoint and canonical sources available on Coral, the full
bounded CPU verification is executable from this package directory:

```bash
/root/flyenv/bin/python checkpoint_smoke.py
```

It verifies old-source/checkpoint hashes, uses one Torch thread, runs four
synthetic vectors and probes a real persistent subprocess with a 60-second
timeout. The frozen-old test return code 1 is expected; v2 tests and checkpoint
smoke must have return code 0. Local verification: 15 passed, 1 explicit Torch
skip; Coral verification: all 16 passed. `remote-checks.json` preserves both.
Private transport, deployment and inventory helpers are deliberately absent
from this public package.

## Installed side-by-side version and explicit invocation

After independent review, the standalone v2 file was installed as
`/opt/argos-roach/fly_bridge/snn_rank_worker_v2.py`, with SHA256
`e366fb50ab4825abea09df6217e2f2fe81ff49209e275ff0bd920f05060e9253`.
Installation verified the checkpoint and old worker hashes, refused replacement
of a different existing v2, and checked all hashes again after the probe. The old
worker and default launcher remain unchanged. Start v2 explicitly on the node:

```bash
/root/flyenv/bin/python /opt/argos-roach/fly_bridge/snn_rank_worker_v2.py
```

An executable request stream on the node is:

```bash
python3 -c 'import json; print("ping"); print(json.dumps({"op":"info"})); print(json.dumps({"vecs":[[64.]*160],"diag":True}))' \
  | /root/flyenv/bin/python /opt/argos-roach/fly_bridge/snn_rank_worker_v2.py
```

From a normally configured ARGOS runtime process, use its current registry
instead of a hard-coded address or key. This explicitly chooses the v2 backend
for this invocation only; existing consumers remain on their current default:

```python
import json
import subprocess
from src.runtime_registry import ssh_command

command = ssh_command("coral") + [
    "/root/flyenv/bin/python /opt/argos-roach/fly_bridge/snn_rank_worker_v2.py"
]
requests = "ping\n" + json.dumps({"op": "info"}) + "\n" + json.dumps({
    "vecs": [[64.0] * 160], "diag": True
}) + "\n"
result = subprocess.run(command, input=requests, text=True,
                        capture_output=True, timeout=60, check=True)
responses = [json.loads(line) for line in result.stdout.splitlines()]
assert responses[0] == {"pong": 1}
assert responses[1]["provenance"]["worker_version"] == 2
assert len(responses[2]["readout"][0]) == 64
```

The actual installed worker probe returned seven responses: ping/info,
zero+constant64 inference, two invalid requests, valid zero inference and ping.
Its constant64 output matched the raw smoke result; it exited after EOF in 7.65
seconds including checkpoint loading. No daemon was left running.
`deployment-verification.json` contains the responses and verified hashes.

Consumer/default switching remains a separate task-level evaluation decision.
There is no automatic process restart or trained-weight change in this package.
