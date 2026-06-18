#!/usr/bin/env python3
"""Generate ARGOS vault graph for Reddit."""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

# ── Load links ──────────────────────────────────────────────────────────────
with open("/tmp/vault_links.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

# Build edges
edges = []
node_folders = defaultdict(set)
for item in raw:
    src = item.get("from", "").replace(".md", "")
    dst = item.get("to", "")
    if src and dst:
        edges.append((src, dst))
        # guess folder from first path segment of source file
        # we don't have full path here, use heuristics from dst name

# ── Build graph ─────────────────────────────────────────────────────────────
G = nx.DiGraph()
G.add_edges_from(edges)

print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")

# Filter to nodes with decent degree (avoid hairball)
degrees = dict(G.degree())
MIN_DEG = 5
main_nodes = [n for n, d in degrees.items() if d >= MIN_DEG]
print(f"Main nodes (deg>={MIN_DEG}): {len(main_nodes)}")

# Subgraph
H = G.subgraph(main_nodes).copy()
print(f"Subgraph: {H.number_of_nodes()} nodes, {H.number_of_edges()} edges")

# If still too many, keep top by degree
if H.number_of_nodes() > 120:
    sorted_nodes = sorted(H.degree(), key=lambda x: x[1], reverse=True)[:120]
    top_nodes = [n for n, d in sorted_nodes]
    H = H.subgraph(top_nodes).copy()
    print(f"Filtered to top 120: {H.number_of_nodes()} nodes")

# ── Colors by category heuristics ───────────────────────────────────────────
def node_color(name: str) -> str:
    n = name.lower()
    if "hub" in n or "web" in n or n in {"backbone", "argos memory web", "карта памяти"}:
        return "#ff6b35"      # orange — hubs
    if any(x in n for x in {"agent", "провайдер", "provider", "ai", "claude", "kimi", "deepseek", "gemini", "ollama"}):
        return "#00d9ff"      # cyan — ai/agents
    if any(x in n for x in {"gpu", "train", "model", "lora", "dataset", "fine-tun", "hf", "huggingface"}):
        return "#ff00a0"      # magenta — training/ai
    if any(x in n for x in {"quantum", "oracle", "seed", "ibm"}):
        return "#bd00ff"      # purple — quantum
    if any(x in n for x in {"esp", "sensor", "gpio", "mqtt", "iot", "zigbee", "home assistant"}):
        return "#39ff14"      # green — iot
    if any(x in n for x in {"log", "session", "changelog", "audit", "2026-"}):
        return "#a0a0a0"      # gray — logs
    if any(x in n for x in {"project", "release", "deploy", "p2p", "docker", "server", "brain"}):
        return "#ffd700"      # gold — infra
    if any(x in n for x in {"skill", "evolution", "dreamer", "consciousness", "mind", "awareness"}):
        return "#00ffaa"      # teal — mind/skills
    return "#4dabf7"          # blue — default

colors = [node_color(n) for n in H.nodes()]

# ── Layout ──────────────────────────────────────────────────────────────────
plt.figure(figsize=(24, 18), dpi=150)
plt.rcParams["figure.facecolor"] = "#0a0a0f"
plt.rcParams["axes.facecolor"] = "#0a0a0f"

pos = nx.spring_layout(H, k=2.5, iterations=150, seed=3233339492)

# Draw edges (curved)
nx.draw_networkx_edges(
    H, pos,
    edge_color="#334466",
    alpha=0.25,
    width=0.4,
    arrows=True,
    arrowsize=6,
    connectionstyle="arc3,rad=0.15",
    node_size=0,
)

# Draw nodes
sizes = [degrees.get(n, 5) * 25 + 80 for n in H.nodes()]
nx.draw_networkx_nodes(
    H, pos,
    node_color=colors,
    node_size=sizes,
    alpha=0.92,
    edgecolors="#ffffff",
    linewidths=0.3,
)

# Labels for larger nodes only
labels = {n: n for n in H.nodes() if degrees.get(n, 0) >= 12}
nx.draw_networkx_labels(
    H, pos, labels,
    font_size=6,
    font_color="#e0e0e0",
    font_family="sans-serif",
    font_weight="bold",
    bbox=dict(boxstyle="round,pad=0.15", facecolor="#0a0a0f", edgecolor="none", alpha=0.7),
)

# Title
plt.title(
    "👁️ ARGOS Universal OS v2.2 — Knowledge Graph\n"
    f"{H.number_of_nodes()} nodes · {H.number_of_edges()} connections · Quantum Seed 3233339492",
    color="#00d9ff",
    fontsize=18,
    fontweight="bold",
    pad=20,
)

# Legend
legend_elements = [
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#ff6b35", markersize=8, label="Hubs / Memory Web"),
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#00d9ff", markersize=8, label="AI / Agents"),
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#ff00a0", markersize=8, label="Training / Models"),
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#bd00ff", markersize=8, label="Quantum"),
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#39ff14", markersize=8, label="IoT / Sensors"),
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#ffd700", markersize=8, label="Infra / P2P"),
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#00ffaa", markersize=8, label="Mind / Skills"),
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#a0a0a0", markersize=8, label="Logs / Sessions"),
]
plt.legend(
    handles=legend_elements,
    loc="upper right",
    facecolor="#0a0a0f",
    edgecolor="#334466",
    labelcolor="#e0e0e0",
    fontsize=9,
)

plt.axis("off")
plt.tight_layout()

out_path = "/tmp/argos_graph.png"
plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="#0a0a0f", edgecolor="none")
print(f"Saved: {out_path}")

# Also copy to OPi reports
opi_path = "/home/ava/argos-reports/argos_graph_2026-05-20.png"
Path(opi_path).parent.mkdir(parents=True, exist_ok=True)
import shutil
shutil.copy(out_path, opi_path)
print(f"Copied to OPi: {opi_path}")
