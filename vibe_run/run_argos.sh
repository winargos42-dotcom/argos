#!/usr/bin/env bash
# Reproducible sandbox launcher for ARGOS Universal OS (original repo code).
# Starts: test LLM adapter (11434) -> MCP API (8000) -> ARGOS API gateway (8080).
# No secrets are required; external backends are disabled via empty env vars.
set -euo pipefail

REPO_DIR="${REPO_DIR:-/workspace/github__winargos42-dotcom__argos}"
RUN_DIR="${RUN_DIR:-/workspace/argos-runtime}"
VENV="${VENV:-$RUN_DIR/venv}"
LOG_DIR="$RUN_DIR/logs"
mkdir -p "$LOG_DIR"

if [ ! -x "$VENV/bin/python" ]; then
  python3.12 -m venv "$VENV"
  "$VENV/bin/pip" install -q fastapi 'uvicorn[standard]' httpx requests python-dotenv
fi

PY="$VENV/bin/python"
cd "$REPO_DIR"

# --- 1. Local LLM: real Qwen2.5-0.5B-Instruct Q4 via llama.cpp (loopback) --
# Falls back to the deterministic test adapter if no model is downloaded.
MODEL="$(ls "$RUN_DIR"/models/models--Qwen--Qwen2.5-0.5B-Instruct-GGUF/snapshots/*/qwen2.5-0.5b-instruct-q4_k_m.gguf 2>/dev/null | head -1 || true)"
if [ -n "$MODEL" ]; then
  ARGOS_MODEL_PATH="$MODEL" ARGOS_LLM_THREADS=4 nohup "$PY" vibe_run/local_llm_server.py \
    > "$LOG_DIR/local_llm.log" 2>&1 &
  echo $! > "$LOG_DIR/local_llm.pid"
else
  nohup "$PY" vibe_run/test_llm_adapter.py \
    > "$LOG_DIR/test_adapter.log" 2>&1 &
  echo $! > "$LOG_DIR/test_adapter.pid"
fi

# --- 2. MCP API (src/mcp_api_standalone.py, original code) -----------------
# Empty env vars override the hardcoded Cloudflare peers so the node stays local.
env -u ARGOS_MODEL_ROUTER \
  ARGOS_PC_URL="" ARGOS_BRAIN_URL="" ARGOS_LAPTOP_URL="" \
  ARGOS_MCP_URL="" OLLAMA_URL="http://127.0.0.1:11434" \
  HF_TOKEN="" ANTHROPIC_API_KEY="" OPENAI_API_KEY="" GEMINI_API_KEY="" \
  ARGOS_LOG_DIR="$LOG_DIR" \
  nohup "$PY" -m uvicorn src.mcp_api_standalone:app --host 127.0.0.1 --port 8000 \
  > "$LOG_DIR/mcp_api.log" 2>&1 &
echo $! > "$LOG_DIR/mcp_api.pid"

# --- 3. ARGOS API gateway (main.py, original code) --------------------------
ARGOS_NODE_ID="argos-vibe-sandbox" \
  ARGOS_MCP_URL="http://127.0.0.1:8000" \
  ARGOS_PC_URL="" ARGOS_BRAIN_API_URL="" \
  ARGOS_LOG_DIR="$LOG_DIR" \
  nohup "$PY" -m uvicorn main:app --host 127.0.0.1 --port 8080 \
  > "$LOG_DIR/gateway.log" 2>&1 &
echo $! > "$LOG_DIR/gateway.pid"

sleep 4
echo "--- health checks ---"
curl -s http://127.0.0.1:11434/health; echo
curl -s http://127.0.0.1:8000/health; echo
curl -s http://127.0.0.1:8080/health; echo
echo "--- PIDs ---"
for f in "$LOG_DIR"/*.pid; do echo "$f: $(cat "$f")"; done
