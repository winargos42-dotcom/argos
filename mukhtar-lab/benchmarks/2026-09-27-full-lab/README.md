# Full live-lab regression — 2026-09-27

The complete raw archive, original manifest and exact runner/verifier are in
[MUKHTAR-Bench](https://huggingface.co/datasets/AvaSiG/MUKHTAR-Bench/tree/2caf07882ae7a8f8752b3ddbd4c2ed0fe7d0b6c8/runs/2026-09-27-full-lab).
This Git directory keeps the summary and verification report.

Actual local calculations: 20 locomotion trials (4 scenarios × 5 controllers,
20 seconds each), 12 PRC experiments (4 drives × E1/I1/I2), and offline ARC
search on 5 games (400-action maximum). One deterministic run per configuration;
this is not a statistical performance claim. Controllers are analytic; PRC is
the isolated five-cell BASE T1-L circuit. ARC uses search without a neural head.

`raw-runs.tar.gz` contains every model XML, trajectory, reflex event log,
summary and SHA256 manifest, PRC control/perturbation rasters, and native ARC
frames/actions/scorecards. `raw-manifest.json` describes paths inside its
`raw-runs/` directory. `verification.json` records independent kinematic replay
and event-count checks of all 20 trajectories. Failed behavior is retained.

The exact executed runner/verifier are included for provenance. Their SPACE
and ROOT constants identify this execution environment; change those locations
to replay in another checkout. Install `mukhtar-lab/space/requirements.txt`
under Python 3.12 before running. Each trial records the executing source hashes.

Git revisions: 91146d65ffdc36b76bc818c7511055c1e2543e5b

| Scenario | Controller | Distance m | Fell | Reflex starts |
|---|---|---:|---|---:|
| B01-flat | BASE | 1.260 | False | 0 |
| B01-flat | R1b | 1.260 | False | 0 |
| B01-flat | R3v2 | 1.260 | False | 0 |
| B01-flat | R1b+R3v2 | 1.260 | False | 0 |
| B01-flat | R4 | 0.887 | False | 108 |
| B02-footcatch12 | BASE | 0.486 | False | 0 |
| B02-footcatch12 | R1b | 1.238 | False | 9 |
| B02-footcatch12 | R3v2 | 0.486 | False | 0 |
| B02-footcatch12 | R1b+R3v2 | 1.257 | False | 11 |
| B02-footcatch12 | R4 | 0.981 | False | 112 |
| B03-gap20 | BASE | 0.939 | True | 0 |
| B03-gap20 | R1b | 1.249 | False | 10 |
| B03-gap20 | R3v2 | 0.987 | False | 76 |
| B03-gap20 | R1b+R3v2 | 1.190 | False | 69 |
| B03-gap20 | R4 | 0.907 | True | 78 |
| B04-rough4_10 | BASE | 1.286 | False | 0 |
| B04-rough4_10 | R1b | 1.335 | False | 2 |
| B04-rough4_10 | R3v2 | 1.286 | False | 1 |
| B04-rough4_10 | R1b+R3v2 | 1.335 | False | 2 |
| B04-rough4_10 | R4 | 0.989 | False | 120 |
