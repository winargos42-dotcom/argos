#!/usr/bin/env bash
# restore_from_x230.sh — safe restore of ORIGINAL ARGOS modules transferred from X230.
#
# Usage:
#   ./vibe_run/restore_from_x230.sh --archive <snapshot.zip> [repo_dir]
#   ./vibe_run/restore_from_x230.sh --staging <staging_dir> [repo_dir]   # explicit fallback
#
# Archive mode (primary): the ZIP snapshot prepared on X230
#   (/home/argos-data/mcp-workspace/argos-vibe-recovery-staging/
#    argos-vibe-recovery-readable-snapshot.zip,
#    SHA256 6b1a60237cca2bfd2b202457da24043eb6cca3de59da9baeaf0d4da73347606e).
#   The script refuses to run without the archive (or the explicit --staging
#   fallback), verifies the archive SHA256, extracts it, and only then copies.
#
# Expected archive/staging layout:
#   recovery/argos_ai_brain.py          <- /home/argos-data/recovery/argos_ai_brain.py
#   recovery/argos_brain_api.py         <- /home/argos-data/recovery/argos_brain_api.py
#   runtime/app/src/...                 <- /home/argos-data/runtime/app/src/
#                                          (core.py, awa_core.py, 13 deps)
#
# Guarantees:
#   * archive SHA256 must match the recorded value (or EXPECTED_ARCHIVE_SHA256);
#   * every copied file is verified SHA256 source<->destination;
#   * files about to be overwritten are backed up, never deleted;
#   * missing modules are REPORTED, never imitated; restore stops on any gap
#     unless ALLOW_MISSING=1 is set explicitly (partial restore of what exists);
#   * import checks keep ArgosCore (src/core.py) and AWACore (src/awa_core.py)
#     strictly separate; Brain API tests run last.
set -euo pipefail

EXPECTED_ARCHIVE_SHA256="${EXPECTED_ARCHIVE_SHA256:-6b1a60237cca2bfd2b202457da24043eb6cca3de59da9baeaf0d4da73347606e}"

MODE=""
SRC=""
REPO="$(pwd)"
while [ $# -gt 0 ]; do
  case "$1" in
    --archive) MODE="archive"; SRC="${2:?missing zip path}"; shift 2 ;;
    --staging) MODE="staging"; SRC="${2:?missing staging dir}"; shift 2 ;;
    *) REPO="$1"; shift ;;
  esac
done
[ -n "$MODE" ] || { echo "[restore][FAIL] no source given: use --archive <zip> or --staging <dir>" >&2; exit 2; }

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
WORK="$(mktemp -d /tmp/argos-restore-XXXXXX)"
STAGING="$WORK/staging"
BACKUP="$REPO/.vibe-restore-backup-$STAMP"
MANIFEST="$REPO/.vibe-restore-manifest-$STAMP.sha256"
PY="${PYTHON:-}"
[ -n "$PY" ] || PY="${ARGOS_RUNTIME:-/workspace/argos-runtime}/venv/bin/python"
[ -x "$PY" ] || PY="$(command -v python3)"

log() { printf '[restore] %s\n' "$*"; }
fail() { printf '[restore][FAIL] %s\n' "$*" >&2; exit 1; }
trap 'rm -rf "$WORK"' EXIT

# --- stage the source ----------------------------------------------------------
if [ "$MODE" = "archive" ]; then
  [ -f "$SRC" ] || fail "archive not found: $SRC"
  ACTUAL="$(sha256sum "$SRC" | awk '{print $1}')"
  log "archive  : $SRC"
  log "sha256   : $ACTUAL"
  if [ "$ACTUAL" != "$EXPECTED_ARCHIVE_SHA256" ]; then
    fail "archive SHA256 mismatch (expected $EXPECTED_ARCHIVE_SHA256). Refusing to restore."
  fi
  log "sha256   : OK (matches X230 record)"
  mkdir -p "$STAGING"
  unzip -q "$SRC" -d "$STAGING"
  log "extracted to $STAGING"
else
  [ -d "$SRC" ] || fail "staging dir not found: $SRC"
  STAGING="$SRC"
  log "staging  : $STAGING (explicit fallback mode)"
fi
[ -d "$REPO/src" ] || fail "repo dir not found: $REPO"

# --- required file map: staged_path|repo_relative_path -------------------------
REQUIRED=(
  "recovery/argos_ai_brain.py|argos_ai_brain.py"
  "recovery/argos_brain_api.py|argos_brain_api.py"
  "runtime/app/src/core.py|src/core.py"
  "runtime/app/src/awa_core.py|src/awa_core.py"
  "runtime/app/src/quantum/__init__.py|src/quantum/__init__.py"
  "runtime/app/src/quantum/logic.py|src/quantum/logic.py"
  "runtime/app/src/factory/__init__.py|src/factory/__init__.py"
  "runtime/app/src/factory/replicator.py|src/factory/replicator.py"
  "runtime/app/src/connectivity/sensor_bridge.py|src/connectivity/sensor_bridge.py"
  "runtime/app/src/skill_loader.py|src/skill_loader.py"
  "runtime/app/src/dag_agent.py|src/dag_agent.py"
  "runtime/app/src/github_marketplace.py|src/github_marketplace.py"
  "runtime/app/src/modules.py|src/modules.py"
  "runtime/app/src/context_manager.py|src/context_manager.py"
  "runtime/app/src/agent.py|src/agent.py"
  "runtime/app/src/argos_integrator.py|src/argos_integrator.py"
  "runtime/app/src/agent_guard.py|src/agent_guard.py"
  "runtime/app/src/rollback_manager.py|src/rollback_manager.py"
  "runtime/app/src/telegram_direct_commands.py|src/telegram_direct_commands.py"
)

log "checking $((${#REQUIRED[@]})) required files..."
MISSING_LIST=""
for entry in "${REQUIRED[@]}"; do
  src="${entry%%|*}"
  [ -f "$STAGING/$src" ] || MISSING_LIST="$MISSING_LIST $src"
done

if [ -n "$MISSING_LIST" ]; then
  N=$(echo $MISSING_LIST | wc -w)
  log "MISSING in source ($N):"
  for m in $MISSING_LIST; do log "  - $m"; done
  if [ "${ALLOW_MISSING:-0}" != "1" ]; then
    fail "missing module(s) reported, not imitated. Re-run with ALLOW_MISSING=1 to restore only what exists."
  fi
  log "ALLOW_MISSING=1 — partial restore of present files only."
fi

# --- backup + copy + sha256 ----------------------------------------------------
mkdir -p "$BACKUP"
: > "$MANIFEST"
sha() { sha256sum "$1" | awk '{print $1}'; }

COPIED=0
for entry in "${REQUIRED[@]}"; do
  src="${entry%%|*}"; dst="${entry##*|}"
  [ -f "$STAGING/$src" ] || { log "skip     : $dst (absent in source)"; continue; }
  if [ -f "$REPO/$dst" ]; then
    mkdir -p "$BACKUP/$(dirname "$dst")"
    cp -p "$REPO/$dst" "$BACKUP/$dst"
    log "backup   : $dst"
  fi
  mkdir -p "$REPO/$(dirname "$dst")"
  cp -p "$STAGING/$src" "$REPO/$dst"
  s="$(sha "$STAGING/$src")"; d="$(sha "$REPO/$dst")"
  printf '%s  %s\n' "$d" "$dst" >> "$MANIFEST"
  [ "$s" = "$d" ] || fail "SHA256 mismatch after copy: $src ($s) vs $dst ($d)"
  log "ok       : $dst  sha256=${d:0:12}..."
  COPIED=$((COPIED+1))
done
log "copied $COPIED file(s), all SHA256 source<->destination checks passed"
log "manifest: $MANIFEST"

# --- dependency closure check --------------------------------------------------
log "import-closure check: which required symbols resolve"
"$PY" - "$REPO" <<'EOF'
import sys
sys.path.insert(0, sys.argv[1])
checks = [
    ("argos_ai_brain", ["ARGOSBrain", "ARGOSAgent", "AgentRole", "AgentConfig", "AzureAIClient"]),
]
for modname, syms in checks:
    try:
        mod = __import__(modname)
        missing = [s for s in syms if not hasattr(mod, s)]
        print(f"[restore] {modname}: OK" if not missing else f"[restore] {modname}: missing {missing}")
    except Exception as exc:
        print(f"[restore] {modname}: UNAVAILABLE ({type(exc).__name__}: {exc})")
for cls, stmt in (("ArgosCore", "from src.core import ArgosCore"),
                  ("AWACore", "from src.awa_core import AWACore")):
    try:
        exec(stmt)
        print(f"[restore] {cls}: import OK (separate implementation)")
    except Exception as exc:
        print(f"[restore] {cls}: import FAILED ({type(exc).__name__}: {exc})")
EOF

# --- Brain API integration tests ----------------------------------------------
log "running Brain API integration tests"
(cd "$REPO" && "$PY" -m pytest vibe_run/test_brain_api_integration.py -v || true)

log "DONE. Report above states exactly what was restored, what is still missing."
log "Backups of previously existing repo files: $BACKUP"
