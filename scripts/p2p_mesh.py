#!/usr/bin/env python3
"""
ARGOS P2P Mesh — Phase 6.3
Без центрального Brain API. Каждая нода:
  1. Анонсирует себя UDP broadcast/multicast каждые 10с
  2. Слушает анонсы других нод
  3. Если Brain (:5010) не отвечает 30с → голосование за временного лидера
  4. Временный лидер = нода с min(load) + max(uptime)
  5. Все ноды реплицируют MemPalace на лидера
"""
import socket, json, time, subprocess, os
from pathlib import Path
from datetime import datetime
import threading
import requests

MEM_DIR = Path("/home/ava/Projects/argoss/data/mempalace")
P2P_STATE = MEM_DIR / "p2p_state.json"
BROADCAST_PORT = 19876
BROADCAST_INTERVAL = 10
HEALTH_TIMEOUT = 30

NODES = {
    "nexus": {"ip": "192.168.1.53", "weight": 5, "role": "manager"},
    "orion": {"ip": "192.168.1.53", "weight": 10, "role": "worker", "brain_api": True},
    "opi":   {"ip": "192.168.2.168", "weight": 3, "role": "worker"},
}

class P2PMesh:
    def __init__(self):
        self.my_id = self._detect_node()
        self.peers = {}
        self.leader = None
        self.brain_alive = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.settimeout(2)
        self.data = self._load_state()

    def _detect_node(self):
        hostname = socket.gethostname().lower()
        if "nexus" in hostname or "x230" in hostname: return "nexus"
        if "orion" in hostname or "pc" in hostname: return "orion"
        if "opi" in hostname or "orange" in hostname: return "opi"
        return "unknown"

    def _load_state(self):
        if P2P_STATE.exists():
            return json.loads(P2P_STATE.read_text(encoding="utf-8"))
        return {"election_history": [], "leader_changes": 0}

    def _save_state(self):
        P2P_STATE.write_text(json.dumps(self.data, ensure_ascii=False, indent=2))

    def get_my_stats(self):
        """Собирает метрики локальной ноды."""
        try:
            load = os.getloadavg()[0]
            mem = subprocess.run(["free","-m"], capture_output=True, text=True)
            mem_line = [l for l in mem.stdout.splitlines() if l.startswith("Mem:")][0].split()
            total, used = int(mem_line[1]), int(mem_line[2])
        except:
            load, total, used = 0, 0, 0
        return {
            "id": self.my_id,
            "ip": NODES.get(self.my_id, {}).get("ip", "0.0.0.0"),
            "ts": datetime.now().isoformat(),
            "load": round(load, 2),
            "ram_total_mb": total,
            "ram_used_mb": used,
            "uptime_sec": self._get_uptime(),
        }

    def _get_uptime(self):
        try:
            with open("/proc/uptime") as f:
                return float(f.read().split()[0])
        except:
            return 0

    def broadcast(self):
        """Отправляет UDP broadcast + unicast bootstrap с метриками и gossip relay."""
        stats = self.get_my_stats()
        msg = {"type": "heartbeat", "ttl": 3, **stats}
        data = json.dumps(msg, ensure_ascii=False).encode()
        # Broadcast to subnet
        try:
            self.sock.sendto(data, ("<broadcast>", BROADCAST_PORT))
        except Exception:
            pass
        # Also unicast to bootstrap nodes (fallback if multicast blocked)
        for nid, info in NODES.items():
            if nid != self.my_id:
                try:
                    self.sock.sendto(data, (info["ip"], BROADCAST_PORT))
                except Exception:
                    pass

    def listen(self):
        """Слушает UDP на порт 19876 с GossipSub relay."""
        listen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except:
            pass
        listen_sock.bind(("0.0.0.0", BROADCAST_PORT))
        listen_sock.settimeout(5)
        while True:
            try:
                data, addr = listen_sock.recvfrom(2048)
                msg = json.loads(data.decode())
                peer_id = msg.get("id")
                msg_type = msg.get("type", "heartbeat")
                # GossipSub relay: forward to other peers with TTL-1
                ttl = msg.get("ttl", 3)
                if ttl > 1 and peer_id and peer_id != self.my_id:
                    relay = {**msg, "ttl": ttl - 1, "relay_by": self.my_id}
                    relay_data = json.dumps(relay, ensure_ascii=False).encode()
                    for nid, info in NODES.items():
                        if nid != self.my_id and nid != peer_id:
                            try:
                                self.sock.sendto(relay_data, (info["ip"], BROADCAST_PORT))
                            except Exception:
                                pass
                if peer_id:
                    self.peers[peer_id] = {
                        **{k: v for k, v in msg.items() if k not in ("type", "ttl", "relay_by")},
                        "last_seen": datetime.now().isoformat(),
                        "addr": addr[0],
                        "msg_type": msg_type,
                    }
            except socket.timeout:
                continue
            except (json.JSONDecodeError, KeyError):
                continue

    def check_brain(self):
        """Проверяет, жив ли основной Brain API (:5010)."""
        orion = NODES.get("orion", {})
        url = f"http://{orion.get('ip','192.168.1.53')}:5010/brain/nodes"
        try:
            r = requests.get(url, timeout=5)
            self.brain_alive = r.status_code == 200
        except:
            self.brain_alive = False
        return self.brain_alive

    def elect_leader(self):
        """Выбирает временного лидера среди живых нод."""
        if self.brain_alive:
            self.leader = "orion"
            return self.leader

        candidates = {k: v for k, v in self.peers.items()}
        # Add self
        if self.my_id not in candidates:
            candidates[self.my_id] = self.get_my_stats()

        # Filter: last seen < 60s
        now = datetime.now()
        alive = {}
        for nid, info in candidates.items():
            seen = datetime.fromisoformat(info.get("last_seen", "1970-01-01T00:00:00"))
            if (now - seen).total_seconds() < HEALTH_TIMEOUT * 2:
                alive[nid] = info

        if not alive:
            self.leader = self.my_id
            return self.leader

        # Score: lower load = better, higher uptime = better, higher weight = better
        def score(nid, info):
            w = NODES.get(nid, {}).get("weight", 1)
            load = info.get("load", 999)
            up = info.get("uptime_sec", 0)
            return (load + 1) / (up + 60) / max(w, 1)

        best = min(alive.keys(), key=lambda x: score(x, alive[x]))
        if self.leader != best:
            print(f"[P2P] 🗳️ Leader changed: {self.leader} → {best}")
            self.data["election_history"].append({
                "ts": datetime.now().isoformat(),
                "from": self.leader,
                "to": best,
                "reason": "brain_dead" if not self.brain_alive else "health_check"
            })
            self.data["leader_changes"] += 1
            self._save_state()
        self.leader = best
        return self.leader

    def replicate_to_leader(self):
        """Если я не лидер — реплицирую MemPalace на лидера через rsync/ssh."""
        if self.leader == self.my_id:
            return
        leader_info = NODES.get(self.leader, {})
        leader_ip = leader_info.get("ip")
        if not leader_ip:
            return
        # rsync через ssh
        try:
            src = str(MEM_DIR) + "/"
            dst = f"ava@{leader_ip}:/home/ava/Projects/argoss/data/mempalace/"
            r = subprocess.run(
                ["rsync", "-az", "--timeout=30", "-e", "ssh -i /home/ava/.ssh/id_ed25519 -o StrictHostKeyChecking=no",
                 src, dst],
                capture_output=True, timeout=60
            )
            if r.returncode == 0:
                print(f"[P2P] 📡 Replicated MemPalace to {self.leader}")
            else:
                print(f"[P2P] ⚠️ rsync error: {r.stderr.decode()[:100]}")
        except Exception as e:
            print(f"[P2P] ⚠️ replicate error: {e}")

    def run(self):
        print(f"[P2P] 🌐 Starting mesh on {self.my_id} (port {BROADCAST_PORT})")
        # Start listener thread
        t = threading.Thread(target=self.listen, daemon=True)
        t.start()

        last_broadcast = 0
        last_election = 0
        last_replicate = 0

        while True:
            now = time.time()

            if now - last_broadcast > BROADCAST_INTERVAL:
                self.broadcast()
                last_broadcast = now

            if now - last_election > BROADCAST_INTERVAL * 3:
                self.check_brain()
                self.elect_leader()
                last_election = now

            if now - last_replicate > 300:  # 5 мин
                self.replicate_to_leader()
                last_replicate = now

            # Print status
            peer_list = ", ".join([f"{k}:{v.get('ram_used_mb','?')}MB" for k,v in self.peers.items()])
            print(f"[P2P] Leader={self.leader} | Brain={self.brain_alive} | Peers: {peer_list}")

            time.sleep(BROADCAST_INTERVAL)

if __name__ == "__main__":
    mesh = P2PMesh()
    mesh.run()
