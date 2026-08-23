#!/usr/bin/env bash
# ARGOS RECOVERY — восстановление и запуск ядра после пожара 03.08.2026.
#
# Поднимает три сервиса на чистой машине:
#   Brain API   :5001  — argos_brain_api.py + argos_ai_brain.py (агенты, /think, /coordinate)
#   MCP API     :8000  — src/mcp_api_standalone.py
#   Edge API    :8080  — main.py (тот же сервис, что крутится на Railway)
#
# Использование:
#   bash scripts/argos_recovery.sh            # установить зависимости и запустить
#   bash scripts/argos_recovery.sh --check    # только проверить, что всё живо
#   bash scripts/argos_recovery.sh --stop     # остановить сервисы
#
# Почему тут отдельный ARGOS_MODEL_ROUTER: значения по умолчанию в
# argos_brain_api.py указывают на llama-server по адресу 192.168.1.72 — это
# сгоревший ПК. Без переопределения каждый /think ждёт 45 с × 3 сервера.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VENV="${ARGOS_VENV:-$ROOT/.venv-argos}"
PY="$VENV/bin/python"
PIP="$VENV/bin/pip"
LOGS="$ROOT/logs"

BRAIN_PORT="${ARGOS_BRAIN_API_PORT:-5001}"
MCP_PORT="${ARGOS_MCP_PORT:-8000}"
EDGE_PORT="${ARGOS_EDGE_PORT:-8080}"

# Локальные обращения не должны уходить в HTTP-прокси.
export NO_PROXY="${NO_PROXY:-*}" no_proxy="${no_proxy:-*}"
# Роутер моделей: по умолчанию локальный llama-server; сгоревшие 192.168.1.x убраны.
export ARGOS_MODEL_ROUTER="${ARGOS_MODEL_ROUTER:-http://127.0.0.1:8082|local|10}"

log() { printf '  %s\n' "$*"; }

wait_health() {  # wait_health <url> <секунд>
    local url="$1" limit="${2:-30}" i
    for ((i = 1; i <= limit; i++)); do
        if curl -sS --noproxy '*' -m 2 "$url" >/dev/null 2>&1; then
            printf '%s' "$i"
            return 0
        fi
        sleep 1
    done
    return 1
}

check_services() {
    local ok=0 total=3
    echo "Проверка сервисов:"
    for entry in "Brain API:http://127.0.0.1:$BRAIN_PORT/health" \
                 "MCP API:http://127.0.0.1:$MCP_PORT/health" \
                 "Edge API:http://127.0.0.1:$EDGE_PORT/health"; do
        name="${entry%%:*}"; url="${entry#*:}"
        if curl -sS --noproxy '*' -m 5 "$url" >/dev/null 2>&1; then
            log "OK    $name  $url"
            ok=$((ok + 1))
        else
            log "МЁРТВ $name  $url"
        fi
    done
    echo "Итого: $ok/$total"
    [ "$ok" = "$total" ]
}

stop_services() {
    echo "Останавливаю сервисы..."
    for pattern in "argos_brain_api.py" "mcp_api_standalone" "main:app"; do
        for pid in $(pgrep -f "$pattern" 2>/dev/null || true); do
            case "$(cat "/proc/$pid/comm" 2>/dev/null)" in
                python | python3 | uvicorn)
                    log "kill $pid ($pattern)"
                    kill "$pid" 2>/dev/null || true
                    ;;
            esac
        done
    done
    sleep 2
    echo "Готово."
}

case "${1:-}" in
    --check) check_services; exit $? ;;
    --stop)  stop_services;  exit 0 ;;
esac

echo "============================================================"
echo "  ARGOS RECOVERY — восстановление ядра"
echo "  Корень: $ROOT"
echo "============================================================"

echo
echo "[1/5] Виртуальное окружение"
if [ ! -x "$PY" ]; then
    log "создаю $VENV"
    python3 -m venv "$VENV"
else
    log "уже есть: $VENV"
fi

echo
echo "[2/5] Зависимости"
"$PIP" install --quiet --disable-pip-version-check --upgrade pip >/dev/null 2>&1 || true
"$PIP" install --quiet --disable-pip-version-check -r requirements.txt
"$PIP" install --quiet --disable-pip-version-check -r requirements-brain.txt
# Нужны восстановленным модулям ядра: web_scrapper, quantum, event_bus, context_manager.
"$PIP" install --quiet --disable-pip-version-check beautifulsoup4 psutil redis packaging python-dotenv
log "установлены"

echo
echo "[3/5] Проверка целостности ядра"
if "$PY" -c "import sys; sys.path.insert(0,'.'); import src.core" >/dev/null 2>&1; then
    log "OK    src.core импортируется (ArgosCore доступен)"
else
    log "ВНИМАНИЕ: src.core не импортируется — часть модулей всё ещё утрачена."
    log "          Список: см. POST_FIRE_RECOVERY.md, раздел «Что ещё не восстановлено»."
fi
if "$PY" -c "import argos_ai_brain" >/dev/null 2>&1; then
    log "OK    argos_ai_brain импортируется"
else
    log "ОШИБКА: argos_ai_brain недоступен — Brain API не поднимется."
    exit 1
fi

echo
echo "[4/5] Запуск сервисов"
mkdir -p "$LOGS"

if ! curl -sS --noproxy '*' -m 2 "http://127.0.0.1:$BRAIN_PORT/health" >/dev/null 2>&1; then
    ARGOS_BRAIN_API_PORT="$BRAIN_PORT" setsid nohup "$PY" argos_brain_api.py \
        > "$LOGS/brain_api.log" 2>&1 < /dev/null &
    log "Brain API запускается на :$BRAIN_PORT"
else
    log "Brain API уже слушает :$BRAIN_PORT"
fi

if ! curl -sS --noproxy '*' -m 2 "http://127.0.0.1:$MCP_PORT/health" >/dev/null 2>&1; then
    setsid nohup "$VENV/bin/uvicorn" src.mcp_api_standalone:app --host 0.0.0.0 --port "$MCP_PORT" \
        > "$LOGS/mcp_api.log" 2>&1 < /dev/null &
    log "MCP API запускается на :$MCP_PORT"
else
    log "MCP API уже слушает :$MCP_PORT"
fi

if ! curl -sS --noproxy '*' -m 2 "http://127.0.0.1:$EDGE_PORT/health" >/dev/null 2>&1; then
    setsid nohup "$VENV/bin/uvicorn" main:app --host 0.0.0.0 --port "$EDGE_PORT" \
        > "$LOGS/edge_api.log" 2>&1 < /dev/null &
    log "Edge API запускается на :$EDGE_PORT"
else
    log "Edge API уже слушает :$EDGE_PORT"
fi

for entry in "Brain:$BRAIN_PORT" "MCP:$MCP_PORT" "Edge:$EDGE_PORT"; do
    name="${entry%%:*}"; port="${entry#*:}"
    if t=$(wait_health "http://127.0.0.1:$port/health" 40); then
        log "$name поднялся за ${t} с"
    else
        log "$name НЕ поднялся — смотри $LOGS/"
    fi
done

echo
echo "[5/5] Итог"
check_services || true

cat <<EOF

Дальше:
  Проверка мышления:
    curl -X POST http://127.0.0.1:$BRAIN_PORT/think \\
      -H 'Content-Type: application/json' \\
      -d '{"query":"Статус системы","role":"monitor"}'

  Реальные ответы LLM вместо rule-based: заполнить AZURE_OPENAI_ENDPOINT и
  AZURE_OPENAI_KEY в .env либо поднять локальный llama-server/Ollama и указать
  ARGOS_MODEL_ROUTER="http://<host>:<port>|<модель>|<приоритет>".

  Остановить: bash scripts/argos_recovery.sh --stop
EOF
