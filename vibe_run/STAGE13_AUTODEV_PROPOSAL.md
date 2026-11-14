# ARGOS-VIBE Stage 13 — bounded autonomous code proposals

Status: **implemented and locally tested on X230, NOT installed or verified in Mistral Vibe sandbox**.

## Goal
Separate automatic transport from actual work product. The existing Stage 12 daemon routes every incoming task through `analyze:` and the Qwen 0.5B `think` path, so receiving a text answer must not be reported as code development.

## Design
- `vibe_run/autodev.py`: one local proposal task at most every 24 hours, drawn from a three-item safe ARGOS network/task-health backlog.
- A new `develop:` worker route invokes local Ollama `/api/generate`, requires a short JSON `{ "code": "..." }` output, checks Python AST and static restrictions, and saves the candidate in `$ARGOS_RUNTIME/autodev/proposals/<uuid>/candidate.py` with a separate `report.json`.
- The generated code is **never imported, executed, deployed, or committed automatically**. The report explicitly sets `NEEDS_REVIEW`, `code_executed=false`, `tests_executed=false`, `behavior_verified=false`.
- For externally requested development, `x230_link.py` accepts `mode=develop` **only when the task passes HMAC verification**. Unsigned tasks still go through the existing `analyze:` path or are rejected if they try to invoke `develop`.
- The original `analyze` worker path, 2-worker limit, GitHub polling, state preservation, Qwen/MCP/gateway, and return transport remain intact. The daily proposal queue is local; it does not send code to public servers without a specifically signed inbox request.
- `ARGOS_AUTODEV_ENABLED=0` disables daily proposals; default is 1 after installation. `ARGOS_AUTODEV_MODEL` changes the local model (default qwen2.5:0.5b). At most one new proposal is queued per day.
- Bad JSON, unsupported code or model failure creates an explicit error; **no success is fabricated**.

## Tested on X230
- `python -m unittest -v test_autodev.py` — **6 tests PASS**: safe storage, permissions, import/block checks, daily throttle, worker routing without direct ARGOS execution, and explicit evidence that syntax correctness is not semantic correctness.
- AST parses across Stage 13 Python files.
- Actual local Qwen2.5:0.5B produced malformed JSON on a realistic task (38.26 seconds), then syntactically valid but semantically incorrect code on a shorter prompt. This is a **real blocker to unsupervised integration**, not a passing test.
- This stage creates bounded code proposals, **not autonomous software deployment**. It requires a stronger/reliable model plus separate sandboxed semantic tests and owner-reviewed promotion before any generated patch can be integrated.

## Rollout
1. Manually/on an authorized Vibe remote execution channel install the files from this review branch, retaining the current running daemon and memory DB backups.
2. Run `python vibe_run/test_autodev.py` and inspect the 6 test results.
3. Restart only the confirmed single Vibe daemon (not the ARGOS X230 receiver, Qwen or gateway).
4. Confirm Stage 13 heartbeat and local proposal status by reading Vibe's actual runtime. Do not assert activation based only on a GitHub commit or Qwen answer.
5. To request one external development proposal, submit a `mode=develop` **HMAC-signed** inbox task. Its returned candidate should be static-reviewed on X230 before any execution.

**Not yet solved:** direct access to install code inside Mistral Vibe, reliable coding quality of 0.5B model, semantic tests, automated review/merge, private P2P. HMAC is still in audit mode.
