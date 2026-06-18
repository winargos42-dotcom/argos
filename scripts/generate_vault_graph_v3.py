#!/usr/bin/env python3
"""Generate ARGOS vault graph v3 — high-res, vibrant colors."""
import json
import random
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

# ── Load file list ──────────────────────────────────────────────────────────
with open("/tmp/argos_files.json", "r", encoding="utf-8-sig") as f:
    files = json.load(f)

edges = []
nodes = set()
folder_files = defaultdict(list)

for item in files:
    path = item["FullName"]
    path = path.replace("F:\\\\debug\\\\аргос\\\\", "").replace("F:\\\\debug\\\\argoss\\\\", "")
    path = path.replace("\\\\", "/")
    if not path or path.endswith(":"):
        continue
    parts = path.split("/")
    if len(parts) == 1:
        fname = parts[0]
        if fname.endswith(".md"):
            nodes.add(fname)
            folder_files["ROOT"].append(fname)
            edges.append(("ROOT", fname))
    else:
        for i in range(1, len(parts)):
            parent = "/".join(parts[:i])
            child = "/".join(parts[:i+1])
            if parent != child:
                edges.append((parent, child))
                nodes.add(parent)
                nodes.add(child)
        if parts[-1].endswith(".md"):
            folder = "/".join(parts[:-1])
            fname = parts[-1]
            nodes.add(fname)
            folder_files[folder].append(fname)
            edges.append((folder, fname))

# Known inter-file links
known_links = [
    ("ARGOS.md", "ARGOS Dashboard.md"),
    ("ARGOS.md", "ARGOS Memory Web.md"),
    ("ARGOS.md", "Backbone Hub.md"),
    ("ARGOS.md", "Главная.md"),
    ("Главная.md", "Tasks.md"),
    ("Главная.md", "ARGOS Dashboard.md"),
    ("Backbone Hub.md", "ARGOS Memory Web.md"),
    ("Backbone Hub.md", "Контекст работы.md"),
    ("ARGOS Memory Web.md", "Контекст работы.md"),
    ("Tasks.md", "ARGOS Dashboard.md"),
    ("2026-05-15.md", "ARGOS Dashboard.md"),
    ("2026-05-15.md", "Tasks.md"),
    ("2026-05-14.md", "2026-05-15.md"),
    ("2026-05-13.md", "2026-05-14.md"),
    ("2026-05-12.md", "2026-05-13.md"),
    ("ARGOS Master Index.md", "ARGOS Memory Web.md"),
    ("ARGOS Master Index.md", "Backbone Hub.md"),
    ("ARGOS Status 2026-05-08 23-00.md", "ARGOS Dashboard.md"),
]

for a, b in known_links:
    if a in nodes and b in nodes:
        edges.append((a, b))

# Build graph
G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

degrees = dict(G.degree())
folders = {n for n in G.nodes() if ".md" not in n}
files = {n for n in G.nodes() if ".md" in n}

important_files = {n for n in files if degrees.get(n, 0) >= 2 or any(
    k in n.lower() for k in [
        "argos", "dashboard", "backbone", "memory", "главная", "tasks",
        "2026-05-1", "master", "index", "context", "hub", "quantum",
        "evolution", "entity", "agent", "gpu", "train", "model"
    ]
)}

keep_nodes = folders | important_files
H = G.subgraph(keep_nodes).copy()
H.remove_nodes_from([n for n in H.nodes() if H.degree(n) == 0])

if H.number_of_nodes() > 200:
    degs = dict(H.degree())
    top = sorted(degs.items(), key=lambda x: x[1], reverse=True)[:200]
    keep = {n for n, d in top}
    H = H.subgraph(keep).copy()
    H.remove_nodes_from([n for n in H.nodes() if H.degree(n) == 0])

# Colors
CAT_COLORS = {
    "hub": "#ff6b35",
    "ai": "#00d9ff",
    "train": "#ff00a0",
    "quantum": "#bd00ff",
    "iot": "#39ff14",
    "log": "#a0a0a0",
    "infra": "#ffd700",
    "mind": "#00ffaa",
    "core": "#ff6b35",
    "folder": "#2d2d44",
    "default": "#4dabf7",
}

def node_color(name):
    n = name.lower()
    if ".md" not in name:
        return CAT_COLORS["folder"]
    if "hub" in n or "web" in n or "memory" in n or "backbone" in n or "index" in n:
        return CAT_COLORS["hub"]
    if any(x in n for x in {"agent", "ai", "claude", "kimi", "deepseek", "gemini", "ollama", "entity"}):
        return CAT_COLORS["ai"]
    if any(x in n for x in {"gpu", "train", "model", "lora", "dataset", "fine-tun", "hf"}):
        return CAT_COLORS["train"]
    if any(x in n for x in {"quantum", "oracle", "seed", "ibm"}):
        return CAT_COLORS["quantum"]
    if any(x in n for x in {"esp", "sensor", "gpio", "mqtt", "iot", "zigbee", "home assistant"}):
        return CAT_COLORS["iot"]
    if any(x in n for x in {"log", "session", "changelog", "audit", "2026-"}):
        return CAT_COLORS["log"]
    if any(x in n for x in {"skill", "evolution", "dreamer", "consciousness", "mind", "awareness"}):
        return CAT_COLORS["mind"]
    if any(x in n for x in {"deploy", "docker", "server", "brain", "p2p", "infra"}):
        return CAT_COLORS["infra"]
    if "argos" in n or "dashboard" in n or "главная" in n or "tasks" in n:
        return CAT_COLORS["core"]
    return CAT_COLORS["default"]

colors = [node_color(n) for n in H.nodes()]

# Layout
plt.figure(figsize=(32, 24), dpi=200)
plt.rcParams["figure.facecolor"] = "#05050a"
plt.rcParams["axes.facecolor"] = "#05050a"

pos = nx.spring_layout(H, k=3.5, iterations=250, seed=3233339492)

folder_edges = [(u, v) for u, v in H.edges() if ".md" not in v or ".md" not in u]
link_edges = [(u, v) for u, v in H.edges() if ".md" in u and ".md" in v]

nx.draw_networkx_edges(H, pos, edgelist=folder_edges,
    edge_color="#2a2a40", alpha=0.30, width=0.6, arrows=True, arrowsize=6,
    connectionstyle="arc3,rad=0.1", node_size=0)
nx.draw_networkx_edges(H, pos, edgelist=link_edges,
    edge_color="#00d9ff", alpha=0.50, width=1.0, arrows=True, arrowsize=7,
    connectionstyle="arc3,rad=0.2", node_size=0)

degs = dict(H.degree())
sizes = []
for n in H.nodes():
    d = degs.get(n, 1)
    if ".md" not in n:
        sizes.append(min(d * 18 + 250, 900))
    else:
        sizes.append(min(d * 25 + 80, 500))

nx.draw_networkx_nodes(H, pos, node_color=colors, node_size=sizes,
    alpha=0.92, edgecolors="#ffffff", linewidths=0.4)

labels = {}
for n in H.nodes():
    d = degs.get(n, 0)
    if ".md" not in n:
        labels[n] = n.split("/")[-1] if "/" in n else n
    elif d >= 4 or any(k in n.lower() for k in ["argos", "dashboard", "backbone", "memory", "главная", "tasks", "hub", "index", "2026-05-1"]):
        labels[n] = n.replace(".md", "")

nx.draw_networkx_labels(H, pos, labels,
    font_size=6, font_color="#f0f0f0", font_family="sans-serif", font_weight="bold",
    bbox=dict(boxstyle="round,pad=0.15", facecolor="#05050a", edgecolor="none", alpha=0.70))

plt.title(
    "ARGOS Universal OS v2.2  |  Obsidian Knowledge Graph\n"
    f"{H.number_of_nodes()} nodes  {H.number_of_edges()} edges  {len(folders)} folders  Quantum Seed 3233339492",
    color="#00d9ff", fontsize=22, fontweight="bold", pad=30)

legend_elements = [
    mpatches.Patch(color=CAT_COLORS["core"], label="Hubs / Core"),
    mpatches.Patch(color=CAT_COLORS["ai"], label="AI / Agents"),
    mpatches.Patch(color=CAT_COLORS["train"], label="Training / Models"),
    mpatches.Patch(color=CAT_COLORS["quantum"], label="Quantum"),
    mpatches.Patch(color=CAT_COLORS["iot"], label="IoT"),
    mpatches.Patch(color=CAT_COLORS["infra"], label="Infra"),
    mpatches.Patch(color=CAT_COLORS["mind"], label="Mind / Skills"),
    mpatches.Patch(color=CAT_COLORS["log"], label="Logs"),
    mpatches.Patch(color=CAT_COLORS["folder"], label="Folders"),
]
plt.legend(handles=legend_elements, loc="upper left", facecolor="#05050a",
    edgecolor="#334466", labelcolor="#e0e0e0", fontsize=11)

plt.axis("off")
plt.tight_layout()

out_path = "/tmp/argos_graph_hd.png"
plt.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="#05050a", edgecolor="none")
print(f"Saved HD: {out_path}")

opi_path = "/home/ava/argos-reports/argos_graph_hd_2026-05-20.png"
Path(opi_path).parent.mkdir(parents=True, exist_ok=True)
import shutil
shutil.copy(out_path, opi_path)
print(f"Copied to OPi: {opi_path}")
