#!/usr/bin/env python3
"""ARGOS Knowledge Graph Analytics — centrality, clusters, insights."""
import json
from pathlib import Path
from collections import defaultdict, Counter

KG_PATH = Path("/home/ava/Projects/argoss/data/knowledge_graph.json")

def analyze():
    with open(KG_PATH, encoding="utf-8") as f:
        kg = json.load(f)

    nodes = {n["id"]: n for n in kg["nodes"]}
    edges = kg["edges"]

    # Degree centrality
    degree = defaultdict(int)
    for e in edges:
        degree[e["from"]] += 1
        degree[e["to"]] += 1

    top_nodes = Counter(degree).most_common(10)
    print("=== Top 10 Connected Nodes ===")
    for nid, deg in top_nodes:
        label = nodes.get(nid, {}).get("label", "?")
        title = nodes.get(nid, {}).get("title", nid)
        print(f"  {deg:4d} | {label:10s} | {title}")

    # Relation distribution
    rel_dist = Counter(e["relation"] for e in edges)
    print("\n=== Relation Distribution ===")
    for rel, cnt in rel_dist.most_common(10):
        print(f"  {cnt:5d} | {rel}")

    # Tag distribution
    tags = [n["title"] for n in kg["nodes"] if n.get("label") == "Tag"]
    print(f"\nTotal tags: {len(tags)}")
    print(f"Total notes: {len([n for n in kg['nodes'] if n.get('label') == 'Note'])}")
    print(f"Density: {len(edges) / max(len(nodes) * (len(nodes)-1) / 2, 1):.6f}")

if __name__ == "__main__":
    analyze()
