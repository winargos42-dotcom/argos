# ARGOS-VIBE Stage 11: automatic return notices

Verified with an unprivileged X230 receiver and X230 sender emulator
on 2026-11-14. NOT YET tested from the Mistral Vibe sandbox.

## Transport
1. X230 creates a safe analyze-only task in the GitHub inbox.
2. Vibe x230_link.py validates payload SHA256 and persists inbound task ID.
3. Vibe uploads the result of ONLY a verified inbox task to x0.at.
4. Vibe sends URL + SHA256 + correlation ID (not the body) to ntfy public topic.
5. X230 polls the ntfy topic every 60s, verifies that task exists in its own
   GitHub inbox, restricts URL to HTTPS x0.at, checks SHA256 and result schema,
   and saves the result into an isolated SQLite DB marked UNTRUSTED.

Vibe keeps outbox.jsonl and notice_receipts.jsonl. Failed ntfy publications
are retried through retry_unnotified() every scheduled daemon poll.

## Security and limitations
- Public ntfy and x0.at: NEVER publish credentials, proprietary source,
  private user records, system commands or unrestricted ARGOS data.
- Topic is public: SHA256 checks integrity, not origin authenticity.
- X230 does NOT execute downloaded code or feed it into ARGOS actions.
- ntfy message retention is finite (normally 12h); long outages can lose
  notifications despite successful ntfy publication.
- Original Vibe sandbox must load code before actual Vibe -> X230 confirmation.
- Sandbox VM lifetime/free limits remain controlled by Mistral.

## Vibe activation
Fetch branch vibe/argos-vibe-stage1-11-review-20261114.
Copy only vibe_run/x230_link.py, vibe_run/daemon.py and
vibe_run/return_channel.json to existing Vibe checkout.
Preserve SQLite and x230_link_state.json. Safely replace the one active daemon
without restarting the LLM, MCP or gateway.
Verify new result_notice_sent event, notice_receipts.jsonl,
and the result actually arriving in the X230 receiver.
