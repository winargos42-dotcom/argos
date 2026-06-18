#!/usr/bin/env python3
"""
ARGOS Phase 3 Architect — генератор конфигурации HiveMind GPU mesh.
Создаёт WireGuard mesh + swarm join tokens для 3 узлов.
"""
import yaml, subprocess
from pathlib import Path
from datetime import datetime

# Конфигурация узлов Phase 3
NODES = {
    "orion": {
        "role": "master",
        "ip": "192.168.1.53",
        "gpu": "RX580 8GB",
        "cpu": "Ryzen 7",
        "services": ["brain-api", "distributed-inference", "model-training", "entity-council-gpu"],
        "weight": 10  # голос в консенсусе
    },
    "nexus": {
        "role": "manager",
        "ip": "192.168.1.53",
        "gpu": "Intel iGPU",
        "cpu": "i5-3320M",
        "services": ["gateway", "monitoring", "autonomy-core", "storage", "p2p-hub"],
        "weight": 5
    },
    "opi": {
        "role": "worker",
        "ip": "192.168.2.168",
        "gpu": "Mali-G52",
        "cpu": "Cortex-A55",
        "services": ["edge-inference", "zigbee-bridge", "ha-local", "backup-node"],
        "weight": 3
    }
}

# WireGuard mesh — каждый узел знает всех
WG_PORT = 51820

def gen_wireguard_config(node_name, cfg):
    """Генерирует wg0.conf для узла."""
    # Уникальный ключ — в реальности генерируем через `wg genkey`
    priv_key = f"PRIVATE_{node_name.upper()}_KEY"
    
    peers = []
    for peer_name, peer_cfg in NODES.items():
        if peer_name == node_name:
            continue
        peers.append({
            "PublicKey": f"PUBLIC_{peer_name.upper()}_KEY",
            "AllowedIPs": f"10.200.0.{list(NODES.keys()).index(peer_name)+1}/32",
            "Endpoint": f"{peer_cfg['ip']}:{WG_PORT}",
            "PersistentKeepalive": 25
        })
    
    idx = list(NODES.keys()).index(node_name) + 1
    config = {
        "Interface": {
            "PrivateKey": priv_key,
            "Address": f"10.200.0.{idx}/24",
            "ListenPort": WG_PORT,
            "MTU": 1420,
            "PostUp": "sysctl -w net.ipv4.ip_forward=1",
            "PostDown": "sysctl -w net.ipv4.ip_forward=0"
        },
        "Peer": peers
    }
    return config

def gen_swarm_join_token():
    """Получает токен от текущего swarm manager (Nexus)."""
    try:
        r = subprocess.run(["docker","swarm","join-token","-q","worker"],
            capture_output=True, text=True, timeout=10)
        return r.stdout.strip() if r.returncode == 0 else "TOKEN_NOT_AVAILABLE"
    except: return "TOKEN_NOT_AVAILABLE"

def gen_architecture_doc():
    doc = {
        "project": "ARGOS Phase 3",
        "date": datetime.now().isoformat(),
        "description": "HiveMind GPU mesh — 150 сервисов, distributed LLM, P2P consensus",
        "nodes": NODES,
        "network": {
            "overlay": "argos_overlay (Docker swarm)",
            "wireguard": "10.200.0.0/24 mesh",
            "discovery": "mDNS + custom gossip"
        },
        "components": {
            "distributed_inference": {
                "engine": "vLLM / Ray Serve",
                "gpu_nodes": ["orion"],
                "cpu_nodes": ["nexus", "opi"],
                "model_sharding": "pipeline parallelism across Orion+OPi"
            },
            "consensus": {
                "algorithm": " Raft + weight voting",
                "quorum": "sum(weights) // 2 + 1",
                "current_quorum": 9,  # (10+5+3)//2+1 = 9
                "total_weight": 18
            },
            "self_modification": {
                "trigger": "Idea champion score > 20",
                "workflow": "Codegen → Test → Deploy → Monitor → Rollback if fail",
                "safety": "Kill switch + consensus + git rollback"
            }
        },
        "deployment": {
            "phase_1": "24 services (current)",
            "phase_2": "48 services",
            "phase_3": "150 services",
            "scaling": "Swarm auto-scale based on CPU/GPU load",
            "rollback": "docker service update --rollback"
        }
    }
    return doc

def generate_all():
    out_dir = Path("/home/ava/Projects/argoss/config/phase3")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # WireGuard configs
    for name, cfg in NODES.items():
        wg = gen_wireguard_config(name, cfg)
        (out_dir / f"wg_{name}.yml").write_text(yaml.dump(wg, allow_unicode=True))
    
    # Swarm join
    token = gen_swarm_join_token()
    (out_dir / "swarm_tokens.txt").write_text(
        f"# Generated: {datetime.now().isoformat()}\n"
        f"Worker token: {token}\n"
        f"Manager command: docker swarm join --token {token} 192.168.2.1:2377\n"
        f"# For Orion/OPi: copy this command and run as root\n"
    )
    
    # Architecture doc
    doc = gen_architecture_doc()
    (out_dir / "architecture.yml").write_text(yaml.dump(doc, allow_unicode=True))
    
    print(f"[Phase3] Generated configs in {out_dir}")
    print(f"  - WireGuard: {len(NODES)} nodes")
    print(f"  - Swarm token: {token[:20]}...")
    print(f"  - Architecture: {len(doc['components'])} components")

if __name__ == "__main__":
    generate_all()
