# MUKHTAR-Bench: verified schema 2 run, 2026-09-27

Nine 20-second trials from clean code revision
`62ce2a97eb44c3a06cdd4172591eb2e724684bbc`, Python 3.11.16,
NumPy 2.4.6, MuJoCo 3.14.0, seed 42. The manifest records the exact code,
serialized scenario model and raw event artifact hashes. No neural checkpoint
is used by these analytic Stage1 controllers.

| Scenario | Controller | Distance m | Fell | Peak drop mm | Tilt max deg | Episode starts |
|---|---|---:|---|---:|---:|---:|
| Flat | BASE | 1.260 | no | 0.0 | 2.7 | 0 |
| Flat | R1b | 1.260 | no | 0.0 | 2.7 | 0 |
| Flat | R3v2 | 1.260 | no | 0.0 | 2.7 | 0 |
| Flat | R4 | 0.887 | no | 0.0 | 2.7 | 108 |
| Footcatch 12 mm | BASE | 0.486 | no | 0.0 | 5.5 | 0 |
| Footcatch 12 mm | R1b | 1.238 | no | 0.9 | 5.0 | 9 |
| Gap 20 mm | BASE | 0.939 | yes | 156.0 | 180.0 | 0 |
| Gap 20 mm | R3v2 | 0.987 | no | 24.6 | 21.5 | 76 |
| Gap 20 mm | R1b+R3v2 | 1.190 | no | 29.2 | 27.2 | 69 |

`false_events` is labelled only for the flat no-reflex oracle. Obstacle/gap
results use null, because activation alone does not establish false positives.
Episode starts count reason transitions by leg/reflex, not physical contacts,
not active ticks, and not R3's separate `n_searches` domain count.

Validation: 52 tests passed (38 existing reflex tests plus 14 new export/metric
checks); all 19 manifest artifact hashes and raw event counts verified.
All nine result objects matched an earlier full run exactly. The original
failing checks covered incorrect tilt, loss of transient height dips,
mislabelled false events, repeated hold ticks and mixed-checkout provenance.
An independent read-only review found no remaining blockers.

Reproduce from the source checkout using the installation instructions in the
lab README, then run:

```bash
python fly_bridge/bench_jsonl.py --out /tmp/mukhtar-schema2-reproduction
```

These are simulation measurements for the listed scenes. They do not establish
general navigation ability or results for B04–B10, CPG knockouts, vision or ARC.
Historical HF schema 1 results remain separate. There is no video or complete
body trajectory in this artifact set; JSONL is raw reflex-event telemetry.
