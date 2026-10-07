#!/usr/bin/env bash
set -euo pipefail
OUT="${1:-hackathon/amd-act3/results/environment.txt}"
mkdir -p "$(dirname "$OUT")"
{
  date -u +'%Y-%m-%dT%H:%M:%SZ'
  uname -a
  echo '--- AMD/ROCm ---'
  command -v rocminfo >/dev/null && rocminfo | head -80 || echo 'rocminfo: unavailable'
  command -v rocm-smi >/dev/null && rocm-smi || echo 'rocm-smi: unavailable'
  echo '--- Coral ---'
  ls -l /dev/apex_0 2>/dev/null || echo '/dev/apex_0: unavailable on this node'
  echo '--- Python ---'
  python --version 2>&1 || true
} > "$OUT"
echo "$OUT"
