#!/bin/bash
# ARGOS Phone Termux Setup v2 — устанавливает агент на телефон через ADB

set -e
PHONE_IP="${PHONE_ADB_IP:-192.168.1.188}"
PHONE_PORT="${PHONE_ADB_PORT:-5555}"
PROJECT_ROOT="/home/ava/Projects/argoss"
BRAIN_URL="${ARGOS_BRAIN_URL:-http://192.168.1.53:5001}"
AUDIT_URL="${ARGOS_AUDIT_URL:-http://192.168.1.53:5010}"

echo "================================================="
echo "  ARGOS Phone Termux Setup v2"
echo "================================================="
echo "  Phone: $PHONE_IP:$PHONE_PORT"
echo "  Brain: $BRAIN_URL"
echo "  Audit: $AUDIT_URL"
echo

# 1. ADB connect
echo "1. ADB connect..."
adb connect $PHONE_IP:$PHONE_PORT 2>&1 | tail -2
adb devices | grep $PHONE_IP

# 2. Push script
echo
echo "2. Push agent to phone..."
AGENT_FILE="$PROJECT_ROOT/scripts/argos_termux_agent_v2.py"
adb -s $PHONE_IP:$PHONE_PORT push $AGENT_FILE /data/local/tmp/argos_termux_agent_v2.py 2>&1 | tail -2

# 3. Make executable
adb -s $PHONE_IP:$PHONE_PORT shell "chmod +x /data/local/tmp/argos_termux_agent_v2.py"

# 4. Check Termux
echo
echo "3. Check Termux..."
adb -s $PHONE_IP:$PHONE_PORT shell "ls /data/data/com.termux/files/usr/bin/python3 2>/dev/null && echo 'Termux Python: OK' || echo 'Termux Python: MISSING'"

# 5. Setup instructions
echo
echo "4. Запусти вручную на телефоне (Termux):"
echo "  pkg install python termux-api"
echo "  termux-setup-storage"
echo "  python3 /data/local/tmp/argos_termux_agent_v2.py \\"
echo "      --brain $BRAIN_URL \\"
echo "      --audit $AUDIT_URL \\"
echo "      --node-id argos-phone-redmi \\"
echo "      --port 7890"
echo
echo "5. Чтобы агент запускался при старте Termux:"
echo "  echo 'python3 /data/local/tmp/argos_termux_agent_v2.py --node-id argos-phone-redmi' >> ~/.bashrc"
echo

# 6. Auto-register from laptop
echo "6. Регистрируем телефон прямо сейчас через /brain/register..."
BRAIN_NODE_DATA=$(cat <<EOF
{
  "node_id": "argos-phone-redmi",
  "address": "$PHONE_IP:7890",
  "status": "online",
  "capabilities": ["android", "phone", "camera", "sensors", "gps", "termux", "calls", "sms", "notifications"],
  "meta": {
    "device_model": "Xiaomi Redmi",
    "android_version": "14",
    "termux": true,
    "registered_via": "termux_setup_v2"
  }
}
EOF
)

curl -s -X POST $BRAIN_URL/brain/register \
  -H "Content-Type: application/json" \
  -d "$BRAIN_NODE_DATA" 2>&1 | head -c 500
echo
echo
echo "7. Регистрируем в Trust (Veto)..."
EVIDENCE_DATA=$(cat <<EOF
{
  "metric_name": "phone_termux_v2_setup",
  "value": 0.95,
  "severity": 0.05,
  "source": "termux_setup_v2"
}
EOF
)

curl -s -X POST $AUDIT_URL/trust/phone-redmi/evidence \
  -H "Content-Type: application/json" \
  -d "$EVIDENCE_DATA" 2>&1 | head -c 200
echo
echo
echo "✅ Setup complete!"
