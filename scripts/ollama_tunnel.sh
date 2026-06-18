#!/bin/bash
# ollama_tunnel.sh — Persistent SSH tunnel to PC Ollama (192.168.1.66:11434 → localhost:11435)
# Restarts automatically on failure. Used by ARGOS to reach PC Ollama models.

REMOTE_HOST="192.168.1.66"
REMOTE_PORT="11434"
LOCAL_PORT="11435"
SSH_KEY="/home/ava/.ssh/id_ed25519"
SSH_USER="ava"
MAX_RETRIES=0
RETRY_DELAY=5

while true; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting SSH tunnel: localhost:${LOCAL_PORT} → ${REMOTE_HOST}:${REMOTE_PORT}"
    ssh -o ConnectTimeout=5 -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -o ExitOnForwardFailure=yes -o StrictHostKeyChecking=no -i "${SSH_KEY}" -NL ${LOCAL_PORT}:127.0.0.1:${REMOTE_PORT} ${SSH_USER}@${REMOTE_HOST}
    EXIT_CODE=$?
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SSH tunnel exited with code ${EXIT_CODE}"
    if [ ${MAX_RETRIES} -gt 0 ]; then
        MAX_RETRIES=$((MAX_RETRIES - 1))
        sleep ${RETRY_DELAY}
    else
        sleep ${RETRY_DELAY}
    fi
done
