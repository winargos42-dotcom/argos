#!/bin/bash
# ARGOS Autopilot — Full Ecosystem Startup
set -e
cd /home/ava/Projects/argoss
source .venv/bin/activate 2>/dev/null || true
mkdir -p logs

# Environment
export ARGOS_BRAIN_URL="http://127.0.0.1:5001"
export ARGOS_NODE_NAME="argos-laptop"
export ARGOS_NODE_ROLE="compute"
export ARGOS_NODE_CAPABILITIES="p2p,mcp,compute,ai"
export ARGOS_NODE_ADDRESS="192.168.1.53:8000"
export TELEGRAM_BOT_TOKEN="8651650695:AAFKp_UyRq0cRorzV-Boouwwkf7kHB3xYw8"
export ADMIN_IDS="6923777384"

echo "🧠 Starting ARGOS Autopilot..."

# 0. .env validation
echo "  Validating .env..."
python3 scripts/env_validator.py; rc=$?
if [ $rc -eq 2 ]; then
    echo "❌ Критические ошибки в .env! Запуск отменён."
    exit 1
fi

# 0.5 Kill stale processes on known ports
echo "  Cleaning stale processes..."
for port in 5001 8000 1883; do
    fuser -k ${port}/tcp 2>/dev/null || true
done
# Kill stale telegram bot processes (409 conflict prevention)
for pid in $(pgrep -f "run_telegram_bot" 2>/dev/null); do
    # Skip if it's the current process
    if [ "$pid" != "$$" ]; then
        echo "    Killing stale telegram bot PID $pid"
        kill $pid 2>/dev/null || true
    fi
done
sleep 1

# 1. MQTT broker (should be systemd, but verify)
if ! pgrep -x mosquitto > /dev/null; then
    echo "  Starting mosquitto..."
    sudo systemctl start mosquitto
fi

# 1. SSH Tunnel to PC Ollama (port 11434 → localhost:11435)
if ! pgrep -f "ollama_tunnel" > /dev/null; then
    echo "  Starting SSH tunnel to PC Ollama..."
    nohup /home/ava/Projects/argoss/scripts/ollama_tunnel.sh > logs/ollama_tunnel.log 2>&1 &
    sleep 2
    # Verify tunnel
    if curl -s --max-time 5 http://127.0.0.1:11435/ > /dev/null 2>&1; then
        echo "  ✅ PC Ollama tunnel OK (9 models)"
    else
        echo "  ⚠️  PC Ollama tunnel not responding"
    fi
else
    echo "  Ollama tunnel already running"
fi

# 2. Brain API (port 5001)
if ! pgrep -f "argos_brain_api" > /dev/null; then
    echo "  Starting brain_api on :5001..."
    nohup .venv/bin/python argos_brain_api.py > logs/brain_api.log 2>&1 &
    sleep 3
fi

# 3. MCP API (port 8000)
if ! pgrep -f "mcp_api_standalone" > /dev/null; then
    echo "  Starting MCP API on :8000..."
    nohup .venv/bin/uvicorn src.mcp_api_standalone:app --host 0.0.0.0 --port 8000 > logs/mcp_api.log 2>&1 &
    sleep 3
fi

# 4. Agent Bus (MQTT router)
if ! pgrep -f "agent_bus.py" > /dev/null; then
    echo "  Starting agent_bus..."
    nohup .venv/bin/python3 scripts/agent_bus.py > logs/agent_bus.log 2>&1 &
fi

# 5. Autonomous Brain (decision loop)
if ! pgrep -f "autonomous_brain.py" > /dev/null; then
    echo "  Starting autonomous_brain..."
    nohup .venv/bin/python3 scripts/autonomous_brain.py > logs/autonomous_brain.log 2>&1 &
fi

# 6. Agent Bridge MCP
if ! pgrep -f "agent_bridge_mcp" > /dev/null; then
    echo "  Starting agent_bridge_mcp..."
    nohup .venv/bin/python3 scripts/agent_bridge_mcp.py > logs/agent_bridge.log 2>&1 &
fi

# 7. P2P Agent
if ! pgrep -f "p2p_agent" > /dev/null; then
    echo "  Starting p2p_agent..."
    nohup .venv/bin/python archive/root_py/p2p_agent.py > logs/p2p_agent.log 2>&1 &
fi

# 8. Telegram Bot
if ! pgrep -f "run_telegram_bot" > /dev/null; then
    echo "  Starting telegram_bot..."
    nohup .venv/bin/python scripts/run_telegram_bot.py >> logs/telegram_bot.log 2>&1 &
fi

# 9. HA Metrics Pusher
if ! pgrep -f "ha_metrics_pusher" > /dev/null; then
    echo "  Starting ha_metrics_pusher..."
    nohup .venv/bin/python3 scripts/ha_metrics_pusher.py > logs/ha_metrics.log 2>&1 &
fi

# 10. ESP Display Manager
if ! pgrep -f "esp_display_manager" > /dev/null; then
    echo "  Starting esp_display_manager..."
    nohup .venv/bin/python3 scripts/esp_display_manager.py >> logs/esp_display.log 2>&1 &
fi

# 11. Ollama (local — verify running)
if pgrep -f "ollama serve" > /dev/null; then
    echo "  Ollama already running"
else
    echo "  Starting Ollama..."
    nohup ollama serve > logs/ollama.log 2>&1 &
    sleep 5
fi

# 12. .env validator (post-start check)
echo "  Post-start .env check..."
python3 scripts/env_validator.py > /dev/null 2>&1 || true

# 10. Register PC node in Brain
echo "  Registering PC node in P2P..."
curl -s -X POST http://localhost:5001/brain/register \
    -H "Content-Type: application/json" \
    -d '{"node_id":"argos-pc","address":"192.168.1.66:5010","role":"server","capabilities":["gpu","compute","brain","ollama","redis"]}' > /dev/null 2>&1 || true

sleep 2
echo ""
echo "✅ ARGOS Autopilot started. Services:"
echo "  🧠 Brain API:    http://localhost:5001"
echo "  🔧 MCP API:      http://localhost:8000"
echo "  📊 HA Metrics:   Pushing to :8123"
echo "  📡 MQTT Broker:  localhost:1883"
echo "  🖥️  PC Ollama:   http://localhost:11435 (via SSH tunnel)"
echo "  🤖 Telegram Bot: @Argosssbot"
echo ""
echo "  P2P Nodes:"
curl -s http://localhost:5001/brain/nodes 2>/dev/null | python3 -c "
import sys,json
try:
    d=json.load(sys.stdin)
    for n in d.get('nodes',[]):
        print(f'    {n.get(\"node_id\",\"?\")} @ {n.get(\"address\",\"?\")} caps={n.get(\"capabilities\",[])}')
except: print('    (no nodes)')
" 2>/dev/null || echo "    (brain not responding)"

echo ""
echo "  Running processes:"
pgrep -fa "argos_brain_api|mcp_api|agent_bus|autonomous_brain|agent_bridge|p2p_agent|telegram_bot|mosquitto" | while read line; do echo "    $line"; done
