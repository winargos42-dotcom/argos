#!/usr/bin/env python3
"""Generate ARGOS vault graph from file structure + known links."""
import json
import re
import random
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

# ── Load file list ──────────────────────────────────────────────────────────
with open("/tmp/argos_files.json", "r", encoding="utf-8-sig") as f:
    files = json.load(f)

# Build folder tree and key files
edges = []
nodes = set()
folder_files = defaultdict(list)

for item in files:
    path = item["FullName"]
    # Normalize
    path = path.replace("F:\\\\debug\\\\аргос\\\\", "").replace("F:\\\\debug\\\\argoss\\\\", "")
    path = path.replace("\\\\", "/")
    if not path or path.endswith(":"):
        continue
    parts = path.split("/")
    if len(parts) == 1:
        # Root file
        fname = parts[0]
        if fname.endswith(".md"):
            nodes.add(fname)
            folder_files["ROOT"].append(fname)
            edges.append(("ROOT", fname))
    else:
        # Build folder hierarchy
        for i in range(1, len(parts)):
            parent = "/".join(parts[:i])
            child = "/".join(parts[:i+1])
            if parent != child:
                edges.append((parent, child))
                nodes.add(parent)
                nodes.add(child)
        # File in folder
        if parts[-1].endswith(".md"):
            folder = "/".join(parts[:-1])
            fname = parts[-1]
            nodes.add(fname)
            folder_files[folder].append(fname)
            edges.append((folder, fname))

# Add known inter-file links from vault knowledge
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
    ("ARGOS_COMPLETE_DOCUMENTATION.md.md", "ARGOS.md"),
    ("ARGOS_STATUS__md.md", "ARGOS.md"),
]

for a, b in known_links:
    if a in nodes and b in nodes:
        edges.append((a, b))

# ── Build graph ─────────────────────────────────────────────────────────────
G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

print(f"Total nodes: {G.number_of_nodes()}, edges: {G.number_of_edges()}")

# Filter: keep only folders + files with degree >= 2 + root files
degrees = dict(G.degree())
# Identify folders vs files
folders = {n for n in G.nodes() if ".md" not in n}
files = {n for n in G.nodes() if ".md" in n}

# Keep folders and important files
important_files = {n for n in files if degrees.get(n, 0) >= 2 or any(
    k in n.lower() for k in [
        "argos", "dashboard", "backbone", "memory", "главная", "tasks",
        "2026-05-1", "master", "index", "context", "hub", "quantum",
        "evolution", "entity", "agent", "gpu", "train", "model"
    ]
)}

keep_nodes = folders | important_files
H = G.subgraph(keep_nodes).copy()

# Remove isolated
H.remove_nodes_from([n for n in H.nodes() if H.degree(n) == 0])
print(f"Filtered: {H.number_of_nodes()} nodes, {H.number_of_edges()} edges")

# If too many, trim
if H.number_of_nodes() > 200:
    degs = dict(H.degree())
    top = sorted(degs.items(), key=lambda x: x[1], reverse=True)[:200]
    keep = {n for n, d in top}
    H = H.subgraph(keep).copy()
    H.remove_nodes_from([n for n in H.nodes() if H.degree(n) == 0])
    print(f"Top 200: {H.number_of_nodes()} nodes, {H.number_of_edges()} edges")

# ── Colors ──────────────────────────────────────────────────────────────────
def node_color(name):
    n = name.lower()
    if ".md" not in name:
        if "project mirror" in n or "pm" in n:
            return "#1a1a2e"  # dark — Project Mirror folders
        return "#2d2d44"  # folder
    if "hub" in n or "web" in n or "memory" in n or "backbone" in n or "index" in n:
        return "#ff6b35"
    if any(x in n for x in {"agent", "ai", "claude", "kimi", "deepseek", "gemini", "ollama", "entity"}):
        return "#00d9ff"
    if any(x in n for x in {"gpu", "train", "model", "lora", "dataset", "fine-tun", "hf"}):
        return "#ff00a0"
    if any(x in n for x in {"quantum", "oracle", "seed", "ibm"}):
        return "#bd00ff"
    if any(x in n for x in {"esp", "sensor", "gpio", "mqtt", "iot", "zigbee", "home assistant"}):
        return "#39ff14"
    if any(x in n for x in {"log", "session", "changelog", "audit", "2026-"}):
        return "#a0a0a0"
    if any(x in n for x in {"skill", "evolution", "dreamer", "consciousness", "mind", "awareness"}):
        return "#00ffaa"
    if any(x in n for x in {"deploy", "docker", "server", "brain", "p2p", "infra"}):
        return "#ffd700"
    if "argos" in n or "dashboard" in n or "главная" in n or "tasks" in n:
        return "#ff6b35"
    return "#4dabf7"

colors = [node_color(n) for n in H.nodes()]

# ── Layout ──────────────────────────────────────────────────────────────────
plt.figure(figsize=(28, 22), dpi=150)
plt.rcParams["figure.facecolor"] = "#05050a"
plt.rcParams["axes.facecolor"] = "#05050a"

pos = nx.spring_layout(H, k=3.0, iterations=200, seed=3233339492)

# Edge types
folder_edges = [(u, v) for u, v in H.edges() if ".md" not in v or ".md" not in u]
link_edges = [(u, v) for u, v in H.edges() if ".md" in u and ".md" in v]

nx.draw_networkx_edges(H, pos, edgelist=folder_edges,
    edge_color="#2a2a40", alpha=0.35, width=0.5, arrows=True, arrowsize=5,
    connectionstyle="arc3,rad=0.1", node_size=0)
nx.draw_networkx_edges(H, pos, edgelist=link_edges,
    edge_color="#00d9ff", alpha=0.45, width=0.8, arrows=True, arrowsize=6,
    connectionstyle="arc3,rad=0.2", node_size=0)

# Node sizes
degs = dict(H.degree())
sizes = []
for n in H.nodes():
    d = degs.get(n, 1)
    if ".md" not in n:
        sizes.append(min(d * 15 + 200, 800))
    else:
        sizes.append(min(d * 20 + 60, 400))

nx.draw_networkx_nodes(H, pos, node_color=colors, node_size=sizes,
    alpha=0.9, edgecolors="#ffffff", linewidths=0.3)

# Labels
labels = {}
for n in H.nodes():
    d = degs.get(n, 0)
    if ".md" not in n:
        labels[n] = n.split("/")[-1] if "/" in n else n
    elif d >= 3 or any(k in n.lower() for k in ["argos", "dashboard", "backbone", "memory", "главная", "tasks", "hub", "index", "2026-05-1"]):
        labels[n] = n.replace(".md", "")

nx.draw_networkx_labels(H, pos, labels,
    font_size=5, font_color="#e8e8e8", font_family="sans-serif", font_weight="bold",
    bbox=dict(boxstyle="round,pad=0.12", facecolor="#05050a", edgecolor="none", alpha=0.65))

# Title
plt.title(
    "👁️ ARGOS Universal OS v2.2 — Obsidian Knowledge Graph\n"
    f"{H.number_of_nodes()} nodes · {H.number_of_edges()} connections · {len(folders)} folders · Quantum Seed 3233339492",
    color="#00d9ff", fontsize=20, fontweight="bold", pad=25)

# Legend
legend_elements = [
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#ff6b35", markersize=10, label="Hubs / Core"),
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#00d9ff", markersize=10, label="AI / Agents"),
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#ff00a0", markersize=10, label="Training / Models"),
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#bd00ff", markersize=10, label="Quantum"),
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#39ff14", markersize=10, label="IoT"),
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#ffd700", markersize=10, label="Infra"),
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#00ffaa", markersize=10, label="Mind / Skills"),
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#a0a0a0", markersize=10, label="Logs"),
    plt.Line2D([0], [0], marker="s", color="w", markerfacecolor="#2d2d44", markersize=10, label="Folders"),
]
plt.legend(handles=legend_elements, loc="upper left", facecolor="#05050a",
    edgecolor="#334466", labelcolor="#e0e0e0", fontsize=10)

plt.axis("off")
plt.tight_layout()

out_path = "/tmp/argos_graph.png"
plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="#05050a", edgecolor="none")
print(f"Saved: {out_path}")

# Copy to OPi
opi_path = "/home/ava/argos-reports/argos_graph_2026-05-20.png"
Path(opi_path).parent.mkdir(parents=True, exist_ok=True)
import shutil
shutil.copy(out_path, opi_path)
print(f"Copied to OPi: {opi_path}")
