#!/usr/bin/env bash
# ARGOS Bootstrap — Phase 7
# Одна команда: curl -sSL https://raw.githubusercontent.com/.../bootstrap.sh | bash
set -e

ARGOS_USER="${ARGOS_USER:-ava}"
ARGOS_HOME="/home/${ARGOS_USER}"
ARGOS_DIR="${ARGOS_HOME}/Projects/argoss"
REPO="https://github.com/AvA-ARGOS/argos-hivemind.git"
BRANCH="${ARGOS_BRANCH:-main}"

echo "================================================================"
echo "            🚀 ARGOS BOOTSTRAP PHASE 7 — SELF-REPLICATION         "
echo "================================================================"
echo "Node: $(hostname) | Arch: $(uname -m) | Date: $(date)"

# 1. Detect hardware
ARCH=$(uname -m)
RAM_MB=$(free -m 2>/dev/null | awk '/^Mem:/{print $2}' || echo "0")
CPU_CORES=$(nproc 2>/dev/null || echo "1")
HAS_DOCKER=$(command -v docker &>/dev/null && echo "yes" || echo "no")

echo "[Bootstrap] RAM: ${RAM_MB}MB | Cores: ${CPU_CORES} | Docker: ${HAS_DOCKER}"

# 2. Install base dependencies
install_deps() {
    echo "[Bootstrap] Installing deps..."
    if command -v apt-get &>/dev/null; then
        sudo apt-get update -qq
        sudo apt-get install -y -qq git python3 python3-venv python3-pip curl wget rsync docker.io docker-compose 2>/dev/null || true
    elif command -v pacman &>/dev/null; then
        sudo pacman -S --noconfirm --needed git python python-pip curl wget rsync docker docker-compose 2>/dev/null || true
    elif command -v apk &>/dev/null; then
        sudo apk add --no-cache git python3 py3-pip curl wget rsync docker docker-cli-compose 2>/dev/null || true
    fi
}

install_deps

# 3. Install Docker if missing (Phase 7 edge case: old phone/router)
if [ "$HAS_DOCKER" = "no" ]; then
    echo "[Bootstrap] Installing Docker..."
    curl -fsSL https://get.docker.com | sh 2>/dev/null || {
        echo "[Bootstrap] ⚠️ Docker install failed — using pip podman fallback"
        pip3 install --user podman-compose 2>/dev/null || true
    }
    sudo usermod -aG docker "$ARGOS_USER" 2>/dev/null || true
fi

# 4. Clone repo
if [ ! -d "$ARGOS_DIR" ]; then
    echo "[Bootstrap] Cloning $REPO..."
    git clone --depth 1 -b "$BRANCH" "$REPO" "$ARGOS_DIR" 2>/dev/null || {
        echo "[Bootstrap] ⚠️ Git clone failed — using fallback tarball"
        mkdir -p "$ARGOS_DIR"
        curl -sL "https://github.com/AvA-ARGOS/argos-hivemind/archive/refs/heads/${BRANCH}.tar.gz" | tar xz -C /tmp
        cp -r "/tmp/argos-hivemind-${BRANCH}"/* "$ARGOS_DIR/"
    }
fi

cd "$ARGOS_DIR"

# 5. Generate .env.docker (Phase 3 compat)
ENV_FILE="$ARGOS_DIR/.env.docker"
cat > "$ENV_FILE" <<ENV
# ARGOS Phase 7 Auto-Generated Env
ARGOS_NODE=$(hostname)
ARGOS_IP=$(hostname -I | awk '{print $1}')
ARGOS_ARCH=$ARCH
ARGOS_RAM=$RAM_MB
ARGOS_CORES=$CPU_CORES
ENV

# 6. Setup Python venv
if [ ! -d "$ARGOS_DIR/.venv" ]; then
    echo "[Bootstrap] Creating venv..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -q -r requirements.txt 2>/dev/null || pip install -q requests 2>/dev/null
else
    source .venv/bin/activate
fi

# 7. Install systemd units
echo "[Bootstrap] Installing systemd units..."
sudo cp "$ARGOS_DIR/systemd/argos-*.service" /etc/systemd/system/ 2>/dev/null || true
sudo cp "$ARGOS_DIR/systemd/argos-*.timer" /etc/systemd/system/ 2>/dev/null || true
sudo systemctl daemon-reload 2>/dev/null || true

# 8. Start core (Phase 1.5 lightweight)
echo "[Bootstrap] Starting Phase 1.5 core..."
if [ "$HAS_DOCKER" = "yes" ] || command -v docker &>/dev/null; then
    docker compose -f docker-compose.core.yml up -d 2>/dev/null || {
        echo "[Bootstrap] ⚠️ Docker compose failed — starting systemd fallback"
        sudo systemctl enable --now argos-p2p-mesh argos-memory argos-self-heal 2>/dev/null || true
    }
else
    echo "[Bootstrap] No Docker — running systemd fallback"
    sudo systemctl enable --now argos-p2p-mesh argos-memory argos-self-heal 2>/dev/null || true
fi

# 9. Join P2P mesh
echo "[Bootstrap] Joining P2P mesh..."
python3 "$ARGOS_DIR/scripts/p2p_mesh.py" &

# 10. Report
NODE_ID=$(hostname)
IP=$(hostname -I | awk '{print $1}')
echo ""
echo "================================================================"
echo "                   🎉 ARGOS BOOTSTRAP COMPLETE                    "
echo "================================================================"
echo "Node ID: $NODE_ID"
echo "IP:      $IP"
echo "Dir:     $ARGOS_DIR"
echo "Docker:  $HAS_DOCKER"
echo ""
echo "Next steps:"
echo "  1. Add SSH key: ssh-copy-id ${ARGOS_USER}@${IP}"
echo "  2. Check mesh:   python3 ${ARGOS_DIR}/scripts/p2p_mesh.py"
echo "  3. Check status: systemctl list-units | grep argos"
echo "================================================================"
