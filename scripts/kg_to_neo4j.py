#!/usr/bin/env python3
"""Convert ARGOS Knowledge Graph to Neo4j CSV import format."""
import json, csv
from pathlib import Path

KG_PATH = Path("/home/ava/Projects/argoss/data/knowledge_graph.json")
OUT_DIR = Path("/home/ava/Projects/argoss/data/neo4j_import")

def convert():
    with open(KG_PATH, encoding="utf-8") as f:
        kg = json.load(f)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Nodes: id:ID,title,label,source
    with open(OUT_DIR / "nodes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id:ID", "title", ":LABEL", "source"])
        for n in kg["nodes"]:
            w.writerow([
                n["id"],
                n.get("title", ""),
                n.get("label", "Unknown"),
                n.get("source", ""),
            ])

    # Edges: :START_ID,relation,:END_ID
    with open(OUT_DIR / "edges.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([":START_ID", ":TYPE", ":END_ID"])
        for e in kg["edges"]:
            w.writerow([e["from"], e["relation"], e["to"]])

    print(f"[Neo4j] {OUT_DIR}/nodes.csv: {len(kg['nodes'])} rows")
    print(f"[Neo4j] {OUT_DIR}/edges.csv: {len(kg['edges'])} rows")
    print("Import: neo4j-admin import --nodes nodes.csv --relationships edges.csv")

if __name__ == "__main__":
    convert()
