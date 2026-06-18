#!/usr/bin/env python3
"""ARGOS KG Query — GraphRAG для MemPalace.
Study: Knowledge_Graph_GraphRAG_2026.md

Usage:
    python scripts/kg_query.py "GPU inference failure"
"""
import json, re, sys
from pathlib import Path
from collections import defaultdict

KG_PATH = Path("/home/ava/Projects/argoss/data/knowledge_graph.json")

def load_graph():
    with open(KG_PATH, encoding="utf-8") as f:
        return json.load(f)

def build_index(graph):
    """Build adjacency list and node map."""
    nodes = {n["id"]: n for n in graph["nodes"]}
    adj = defaultdict(list)
    for e in graph["edges"]:
        adj[e["from"]].append((e["to"], e["relation"]))
        adj[e["to"]].append((e["from"], e["relation"]))  # Undirected for traversal
    return nodes, adj

def search_nodes(query: str, nodes: dict, top_k: int = 5):
    """Find nodes matching query keywords."""
    keywords = set(re.findall(r"[a-zA-Z_\u0400-\u04FF]+", query.lower()))
    scores = []
    for nid, n in nodes.items():
        title = n.get("title", "").lower()
        label = n.get("label", "").lower()
        score = len(keywords & set(title.split())) + len(keywords & set(label.split()))
        if score > 0:
            scores.append((score, nid, n))
    scores.sort(reverse=True)
    return scores[:top_k]

def traverse(node_id: str, adj: dict, depth: int = 2):
    """BFS traversal up to depth hops."""
    visited = {node_id}
    frontier = {node_id}
    results = []
    for d in range(depth):
        next_frontier = set()
        for nid in frontier:
            for neighbor, relation in adj.get(nid, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    next_frontier.add(neighbor)
                    results.append((nid, relation, neighbor, d + 1))
        frontier = next_frontier
    return results

def query_kg(query: str, depth: int = 2, top_k: int = 5):
    graph = load_graph()
    nodes, adj = build_index(graph)
    matches = search_nodes(query, nodes, top_k)
    context = []
    for score, nid, node in matches:
        context.append(f"## {node.get('title', nid)} (score={score})")
        context.append(f"Type: {node.get('label', 'unknown')}")
        paths = traverse(nid, adj, depth)
        for src, rel, dst, dist in paths[:10]:
            src_title = nodes.get(src, {}).get("title", src)
            dst_title = nodes.get(dst, {}).get("title", dst)
            context.append(f"  [{dist}-hop] {src_title} --{rel}--> {dst_title}")
        context.append("")
    return "\n".join(context)

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "ARGOS system"
    print(query_kg(q))
