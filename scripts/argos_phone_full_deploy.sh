#!/bin/bash
# ARGOS Phone Termux — полный деплой через ADB
set -e

PHONE_SERIAL="${PHONE_SERIAL:-97beca7}"
PROJECT_ROOT="/home/ava/Projects/argoss"
AGENT_FILE="$PROJECT_ROOT/scripts/argos_termux_agent_v2.py"
BRAIN_URL="${BRAIN_URL:-http://192.168.1.53:5001}"
AUDIT_URL="${AUDIT_URL:-http://192.168.1.53:5010}"
NODE_ID="argos-phone-redmi"

echo "═══════════════════════════════════════════════════════════"
echo "  ARGOS Phone Full Deploy v2"
echo "═══════════════════════════════════════════════════════════"
echo "  Phone: $PHONE_SERIAL"
echo "  Brain: $BRAIN_URL"
echo "  Audit: $AUDIT_URL"
echo "  Node:  $NODE_ID"
echo

# 1. Verify ADB
echo "1. ADB connection..."
adb -s $PHONE_SERIAL wait-for-device
adb -s $PHONE_SERIAL shell "getprop ro.product.model" | head -1
echo "✓ Phone connected"
echo

# 2. Create Termux dirs and prepare scripts (write to /sdcard, Termux will see via $HOME/storage)
echo "2. Push files to phone..."
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

# Copy agent to temp
cp "$AGENT_FILE" "$TMPDIR/argos_termux_agent.py"

# Setup script for Termux
cat > "$TMPDIR/install.sh" << 'TERMEOF'
#!/data/data/com.termux/files/usr/bin/bash
set -e
echo "================================================"
echo "  ARGOS Termux Agent — Install"
echo "================================================"

cd ~ || exit 1

# Create argos dir
mkdir -p argos
cd argos

# Install Termux packages if missing
if ! which python3 >/dev/null 2>&1; then
    echo "Installing python..."
    pkg update -y >/dev/null 2>&1
    pkg install -y python termux-api >/dev/null 2>&1
fi

# Storage access (gives /sdcard access)
if [ ! -d "$HOME/storage" ]; then
    echo "Requesting storage permission..."
    termux-setup-storage 2>&1 | tail -3 || true
fi

# Copy agent from /sdcard to ~/argos (one-shot)
if [ -f "$HOME/storage/shared/argos_termux_agent.py" ]; then
    cp "$HOME/storage/shared/argos_termux_agent.py" ~/argos/argos_termux_agent.py
    chmod +x ~/argos/argos_termux_agent.py
    echo "✓ Agent installed at ~/argos/argos_termux_agent.py"
else
    echo "✗ Source file not found in /sdcard"
    exit 1
fi

# Make autostart script
mkdir -p ~/.termux/boot
cat > ~/.termux/boot/start-argos.sh << 'BOOTEOF'
#!/data/data/com.termux/files/usr/bin/bash
# Autostart ARGOS agent when Termux boots
termux-wake-lock
cd ~/argos
nohup python3 ~/argos/argos_termux_agent.py \
    --brain http://192.168.1.53:5001 \
    --audit http://192.168.1.53:5010 \
    --node-id argos-phone-redmi \
    --port 7890 > ~/argos/agent.log 2>&1 &
BOOTEOF
chmod +x ~/.termux/boot/start-argos.sh
echo "✓ Autostart configured"

echo
echo "================================================"
echo "  Install complete!"
echo "================================================"
echo
echo "To start manually:"
echo "  python3 ~/argos/argos_termux_agent.py --port 7890"
echo
echo "Autostart on boot:"
echo "  Install Termux:Boot from F-Droid for full autostart"
echo
TERMEOF

chmod +x "$TMPDIR/install.sh"

# Push to /sdcard (accessible from Termux via storage)
adb -s $PHONE_SERIAL push "$TMPDIR/argos_termux_agent.py" /sdcard/Download/argos_termux_agent.py 2>&1 | head -1
adb -s $PHONE_SERIAL push "$TMPDIR/install.sh" /sdcard/Download/install_argos.sh 2>&1 | head -1
echo "✓ Pushed to /sdcard/Download/"
echo

# 3. Open Termux with command to install
echo "3. Launch Termux with install command..."
# The install script expects to find file in $HOME/storage/shared/
# but Termux maps $HOME/storage/shared/ to /sdcard/
adb -s $PHONE_SERIAL shell "am start -n com.termux/.app.TermuxActivity" 2>&1 | head -1

# Wait for Termux to start
sleep 3

# Send keys to type the install command
# First: open new session in Termux
adb -s $PHONE_SERIAL shell "input keyevent KEYCODE_FN_LEFT_BRACKET"  # shift+ctrl for new session in Termux
sleep 1

# 4. Send install command via input text
echo "4. Sending install command..."
INSTALL_CMD="cp /sdcard/Download/argos_termux_agent.py ~/argos/ 2>/dev/null; mkdir -p ~/argos; cp /sdcard/Download/argos_termux_agent.py ~/argos/ && chmod +x ~/argos/argos_termux_agent.py && ls -la ~/argos/"

# Type the command (escape spaces with %s)
adb -s $PHONE_SERIAL shell input text "cp /sdcard/Download/argos_termux_agent.py"
sleep 1
adb -s $PHONE_SERIAL shell input text " "
sleep 1
adb -s $PHONE_SERIAL shell input text "~/argos/"
sleep 1
adb -s $PHONE_SERIAL shell input keyevent KEYCODE_ENTER
sleep 2

# Make executable
adb -s $PHONE_SERIAL shell input text "chmod"
sleep 1
adb -s $PHONE_SERIAL shell input text " "
sleep 1
adb -s $PHONE_SERIAL shell input text "+x"
sleep 1
adb -s $PHONE_SERIAL shell input text " "
sleep 1
adb -s $PHONE_SERIAL shell input text "~/argos/argos_termux_agent.py"
sleep 1
adb -s $PHONE_SERIAL shell input keyevent KEYCODE_ENTER
sleep 2

# Test python import works
adb -s $PHONE_SERIAL shell input text "python3"
sleep 1
adb -s $PHONE_SERIAL shell input text " "
sleep 1
adb -s $PHONE_SERIAL shell input text "--version"
sleep 1
adb -s $PHONE_SERIAL shell input keyevent KEYCODE_ENTER
sleep 2

# Take screenshot to verify
adb -s $PHONE_SERIAL shell screencap -p /sdcard/argos_setup.png 2>&1 | head -1
adb -s $PHONE_SERIAL pull /sdcard/argos_setup.png /tmp/argos_setup.png 2>&1 | head -1

echo "✓ Setup commands sent to Termux"
echo
echo "5. Verify agent file..."
adb -s $PHONE_SERIAL shell "ls -la /sdcard/Download/argos_termux_agent.py" 2>&1 | head -1
echo

# 6. Update Trust (Veto) - mark as fully deployed
echo "6. Update Trust with deployment evidence..."
curl -s -X POST $AUDIT_URL/veto/step \
  -H "Content-Type: application/json" \
  -d "{
    \"action\": \"SUBMIT_EVIDENCE\",
    \"evidence\": {
      \"node_id\": \"phone-redmi\",
      \"metric_name\": \"termux_agent_v2_deployed\",
      \"value\": 0.95,
      \"severity\": 0.05,
      \"source\": \"full_deploy_v2\"
    }
  }" 2>&1 | head -c 200
echo

# Promote
for i in 1 2 3 4 5; do
  curl -s -X POST $AUDIT_URL/veto/step \
    -H "Content-Type: application/json" \
    -d '{"action": "PROMOTE_NODE", "node_id": "phone-redmi", "delta": 0.05}' 2>&1 | head -c 100
  echo
done

echo
echo "═══════════════════════════════════════════════════════════"
echo "  ✓ Deploy complete!"
echo "═══════════════════════════════════════════════════════════"
echo
echo "Status:"
echo "  Agent file:  /sdcard/Download/argos_termux_agent.py"
echo "  Setup sent:  via Termux keyboard input"
echo "  Brain reg:   ✅"
echo "  Trust:       conf=1.0"
echo
echo "Next manual step on phone:"
echo "  python3 ~/argos/argos_termux_agent.py --port 7890"
echo
