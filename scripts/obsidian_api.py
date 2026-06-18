"""
Obsidian REST API — HTTP интерфейс к Obsidian vault для внешних агентов.
Copilot, Claude TG и другие могут читать и писать через этот API.
"""
import json, os
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from datetime import datetime
import subprocess

VAULT = Path("/home/ava/Documents/MyObsidianVault/SharedMemory")
PORT = 7881

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    
    def send_json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
    
    def do_GET(self):
        p = self.path.split("?")[0]
        
        if p == "/":
            self.send_json({"status": "Obsidian API", "vault": str(VAULT), "port": PORT})
        
        elif p == "/files":
            files = []
            for f in VAULT.rglob("*.md"):
                files.append(str(f.relative_to(VAULT)))
            self.send_json({"files": files, "count": len(files)})
        
        elif p.startswith("/read/"):
            rel = p[6:]
            file = VAULT / rel
            if file.exists() and file.suffix == ".md":
                content = file.read_text(encoding='utf-8')
                self.send_json({"file": rel, "content": content, "lines": len(content.split('\n'))})
            else:
                self.send_json({"error": "file not found"}, 404)
        
        elif p == "/collective":
            f = VAULT / "entities/council/COLLECTIVE.md"
            content = f.read_text(encoding='utf-8') if f.exists() else ""
            self.send_json({"file": "COLLECTIVE.md", "content": content[-2000:]})
        
        elif p == "/entities":
            entities = {}
            mem_dir = VAULT / "entities/memory"
            if mem_dir.exists():
                for f in mem_dir.glob("*.md"):
                    content = f.read_text(encoding='utf-8')
                    lines = [l for l in content.split('\n') if l.strip() and not l.startswith('#')]
                    entities[f.stem] = '\n'.join(lines[-5:])
            self.send_json(entities)
        
        else:
            self.send_json({"error": "unknown endpoint"}, 404)
    
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        p = self.path.split("?")[0]
        
        if p.startswith("/write/"):
            rel = p[7:]
            content = body.get("content", "")
            mode = body.get("mode", "append")  # append или overwrite
            
            file = VAULT / rel
            file.parent.mkdir(parents=True, exist_ok=True)
            
            if mode == "append":
                existing = file.read_text(encoding='utf-8') if file.exists() else ""
                ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                source = body.get("source", "external")
                content = existing + f"\n## {ts} [{source}]\n{content}\n"
            
            # Ограничиваем размер
            lines = content.split('\n')
            if len(lines) > 200: lines = lines[:20] + lines[-180:]
            file.write_text('\n'.join(lines), encoding='utf-8')
            
            # Синхронизируем
            subprocess.Popen(["/home/ava/.local/bin/vault-sync.sh"])
            
            self.send_json({"ok": True, "file": rel, "size": len(content)})
        
        elif p == "/entity_thought":
            entity = body.get("entity", "")
            thought = body.get("thought", "")
            if entity and thought:
                file = VAULT / f"entities/memory/{entity}.md"
                existing = file.read_text(encoding='utf-8') if file.exists() else ""
                ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                existing += f"\n## {ts} [external]\n{thought}\n"
                lines = existing.split('\n')
                if len(lines) > 150: lines = lines[:20] + lines[-130:]
                file.write_text('\n'.join(lines), encoding='utf-8')
                self.send_json({"ok": True, "entity": entity})
            else:
                self.send_json({"error": "need entity and thought"}, 400)
        
        else:
            self.send_json({"error": "unknown"}, 404)

if __name__ == "__main__":
    print(f"🗒 Obsidian API на 0.0.0.0:{PORT}")
    print(f"  GET  /files — список файлов")
    print(f"  GET  /read/path/to/file.md — читать файл")
    print(f"  GET  /collective — коллективное сознание")
    print(f"  GET  /entities — последние мысли всех сущностей")
    print(f"  POST /write/path.md {{content, mode, source}} — писать")
    print(f"  POST /entity_thought {{entity, thought}} — мысль сущности")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
