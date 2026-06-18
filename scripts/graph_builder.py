#!/usr/bin/env python3
"""ARGOS Knowledge Graph Builder — GraphRAG для MemPalace.
Study: Knowledge_Graph_GraphRAG_2026.md
"""
import os, re, json
from pathlib import Path
from datetime import datetime

VAULT = Path("/home/ava/Documents/MyObsidianVault/SharedMemory")
OUTPUT = Path("/home/ava/Projects/argoss/data/knowledge_graph.json")

# Regex patterns
TAG_RE = re.compile(r"#([A-Za-z_\u0400-\u04FF][\w\u0400-\u04FF]*)")
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
HEADING_RE = re.compile(r"^#+\s+(.+)$", re.MULTILINE)

EXCLUDE_DIRS = {"templates", "archive", "trash", ".git"}

def scan_vault():
    """Сканируем все .md файлы в vault."""
    notes = []
    for root, dirs, files in os.walk(VAULT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if f.endswith(".md"):
                notes.append(Path(root) / f)
    return notes

def extract_entities(text: str, filepath: str):
    """Извлекаем entities и relations из заметки."""
    nodes = []
    edges = []
    note_name = Path(filepath).stem

    # Заголовок заметки = entity
    nodes.append({
        "id": note_name,
        "label": "Note",
        "title": note_name,
        "source": filepath,
    })

    # Tags
    for tag in set(TAG_RE.findall(text)):
        tag_id = f"tag:{tag}"
        nodes.append({"id": tag_id, "label": "Tag", "title": f"#{tag}"})
        edges.append({"from": note_name, "to": tag_id, "relation": "HAS_TAG"})

    # Links [[...]]
    for link in set(LINK_RE.findall(text)):
        link_clean = link.split("|")[0].strip()  # [[Note|Alias]] → Note
        nodes.append({"id": link_clean, "label": "Note", "title": link_clean})
        edges.append({"from": note_name, "to": link_clean, "relation": "LINKS_TO"})

    # Headings
    for heading in HEADING_RE.findall(text):
        heading = heading.strip()
        if len(heading) > 3:
            edges.append({"from": note_name, "to": heading, "relation": "CONTAINS"})

    return nodes, edges

def build_graph():
    notes = scan_vault()
    all_nodes = {}
    all_edges = []
    print(f"[KG] Scanning {len(notes)} notes...")

    for note_path in notes:
        try:
            text = note_path.read_text(encoding="utf-8", errors="replace")
            nodes, edges = extract_entities(text, str(note_path))
            for n in nodes:
                all_nodes[n["id"]] = n
            all_edges.extend(edges)
        except Exception as e:
            print(f"  skip {note_path}: {e}")

    graph = {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "vault_path": str(VAULT),
            "total_notes": len(notes),
            "total_nodes": len(all_nodes),
            "total_edges": len(all_edges),
        },
        "nodes": list(all_nodes.values()),
        "edges": all_edges,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    print(f"[KG] Saved to {OUTPUT}")
    print(f"  Nodes: {len(all_nodes)}, Edges: {len(all_edges)}")
    return graph

if __name__ == "__main__":
    build_graph()
