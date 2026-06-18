#!/usr/bin/env python3
"""
ARGOS WireGuard Mesh Bootstrap — создаёт конфиги и доставляет на узлы.
"""
import subprocess, re
from pathlib import Path

WG_DIR = Path("/etc/wireguard")
NODES = {
    "nexus": {"ip": "10.200.0.1", "endpoint": "192.168.2.1:51820"},
    "orion": {"ip": "10.200.0.2", "endpoint": "192.168.1.53:51820"},
    "opi":   {"ip": "10.200.0.3", "endpoint": "192.168.2.168:51820"},
}

def get_or_gen_key(node):
    priv_file = WG_DIR / f"{node}_private.key"
    pub_file  = WG_DIR / f"{node}_public.key"
    if not priv_file.exists():
        if node == "nexus":
            pass
        else:
            # Генерируем если ещё не было
            subprocess.run(["wg","genkey"], capture_output=True, timeout=5,
                stdout=open(priv_file, "w"))
            subprocess.run(["wg","pubkey"], capture_output=True, timeout=5,
                stdin=open(priv_file), stdout=open(pub_file, "w"))
    return priv_file.read_text().strip(), pub_file.read_text().strip()

def gen_config(node_name):
    keys = {}
    for n in NODES:
        if n == "nexus":
            keys[n] = {
                "priv": (WG_DIR / "nexus_private.key").read_text().strip(),
                "pub":  (WG_DIR / "nexus_public.key").read_text().strip()
            }
        else:
            # Плейсхолдеры или реальные ключи
            p = WG_DIR / f"{n}_public.key"
            if p.exists():
                pub = p.read_text().strip()
            else:
                pub = f"PLACEHOLDER_{n.upper()}_PUB_KEY"
            keys[n] = {"pub": pub}
    
    cfg_lines = [
        "[Interface]",
        f"PrivateKey = {keys[node_name]['priv'] if 'priv' in keys[node_name] else keys['nexus']['priv']}",
        f"Address = {NODES[node_name]['ip']}/24",
        f"ListenPort = 51820",
        "MTU = 1420",
        "PostUp = sysctl -w net.ipv4.ip_forward=1",
        "PostDown = sysctl -w net.ipv4.ip_forward=0",
        "",
    ]
    
    for peer, pcfg in NODES.items():
        if peer == node_name:
            continue
        pub_key = keys[peer].get("pub", f"PLACEHOLDER_{peer.upper()}_PUB_KEY")
        cfg_lines.extend([
            "[Peer]",
            f"PublicKey = {pub_key}",
            f"AllowedIPs = {pcfg['ip']}/32",
            f"Endpoint = {pcfg['endpoint']}",
            "PersistentKeepalive = 25",
            "",
        ])
    
    return "\n".join(cfg_lines)

if __name__ == "__main__":
    WG_DIR.mkdir(exist_ok=True, mode=0o700)
    
    for node in NODES:
        cfg = gen_config(node)
        out = Path(f"/tmp/wg_{node}.conf")
        out.write_text(cfg)
        print(f"[WG] Generated {out} for {node}")
    
    print("\n[WG] To deploy:")
    print("  sudo cp /tmp/wg_nexus.conf /etc/wireguard/wg0.conf")
    print("  sudo wg-quick up wg0")
    print("  scp /tmp/wg_orion.conf AvA@192.168.1.53:...")
    print("  scp /tmp/wg_opi.conf   root@192.168.2.168:...")
