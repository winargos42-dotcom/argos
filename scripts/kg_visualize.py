#!/usr/bin/env python3
"""Generate HTML visualization of ARGOS Knowledge Graph using vis.js."""
import json
from pathlib import Path

KG_PATH = Path("/home/ava/Projects/argoss/data/knowledge_graph.json")
OUT_HTML = Path("/home/ava/Projects/argoss/data/kg_visualization.html")

def generate():
    with open(KG_PATH, encoding="utf-8") as f:
        kg = json.load(f)

    nodes_js = []
    for n in kg["nodes"][:500]:  # Limit for perf
        color = {"Note": "#4CAF50", "Tag": "#2196F3"}.get(n.get("label", ""), "#9E9E9E")
        nodes_js.append(f"{{id: '{n['id']}', label: '{n.get('title', n['id'])[:30]}', color: '{color}', title: '{n.get('title', '')}'}}")

    edges_js = []
    for e in kg["edges"][:3000]:  # Limit for perf
        edges_js.append(f"{{from: '{e['from']}', to: '{e['to']}', label: '{e.get('relation', '')}'}}")

    html = f"""<!DOCTYPE html>
<html><head><title>ARGOS Knowledge Graph</title>
<script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<style>body {{margin:0; background:#1e1e1e; color:#eee; font-family:sans-serif;}}
#mynetwork {{width:100vw; height:100vh; border:1px solid #444;}}
h2 {{padding:10px; margin:0; background:#333;}}</style>
</head><body>
<h2>ARGOS Knowledge Graph — {len(kg['nodes'])} nodes, {len(kg['edges'])} edges</h2>
<div id="mynetwork"></div>
<script>
  var nodes = new vis.DataSet([{','.join(nodes_js)}]);
  var edges = new vis.DataSet([{','.join(edges_js)}]);
  var container = document.getElementById('mynetwork');
  var data = {{nodes: nodes, edges: edges}};
  var options = {{nodes: {{shape: 'dot', size: 10, font: {{color: '#eee'}}}},
    edges: {{font: {{color: '#aaa', size: 10}}, arrows: {{to: {{enabled: true, scaleFactor: 0.5}}}}}},
    physics: {{stabilization: false}},
    interaction: {{hover: true}}}};
  var network = new vis.Network(container, data, options);
</script></body></html>"""

    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"[Viz] {OUT_HTML} generated ({len(kg['nodes'])} nodes, {len(kg['edges'])} edges)")
    print(f"  Limited to {len(nodes_js)} nodes + {len(edges_js)} edges for browser performance")

if __name__ == "__main__":
    generate()
