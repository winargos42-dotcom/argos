#!/usr/bin/env python3
"""
ARGOS Mini-Tron-50 Python Inference Wrapper
Loads model directly via transformers (no GGUF/Ollama needed).
Provides OpenAI-compatible API on localhost:11435.
"""

import sys, json, os, argparse
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Model path
MODEL_DIR = os.environ.get("MINITRON_MODEL", "/mnt/c/Users/AvA/Downloads/argos_scripts/mini-tron-50-model/model")
PORT = int(os.environ.get("MINITRON_PORT", "11435"))

class MinitronHandler(BaseHTTPRequestHandler):
    model = None
    tokenizer = None
    
    def log_message(self, fmt, *args):
        print(f"[mini-tron-api] {fmt % args}")
    
    def do_POST(self):
        if self.path == "/v1/chat/completions":
            self.handle_chat()
        elif self.path == "/v1/models":
            self.handle_models()
        else:
            self.send_error(404)
    
    def do_GET(self):
        if self.path == "/v1/models":
            self.handle_models()
        else:
            self.send_error(404)
    
    def handle_models(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "object": "list",
            "data": [{"id": "argos-classic", "object": "model"}]
        }).encode())
    
    def handle_chat(self):
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len)
        req = json.loads(body)
        
        messages = req.get("messages", [])
        prompt = self.build_prompt(messages)
        
        # Generate
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=req.get("max_tokens", 256),
                temperature=req.get("temperature", 0.7),
                top_p=req.get("top_p", 0.9),
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            response_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Remove prompt from output
            if response_text.startswith(prompt):
                response_text = response_text[len(prompt):].strip()
        except Exception as e:
            response_text = f"[ERROR: {e}]"
        
        resp = {
            "id": "chatcmpl-argos",
            "object": "chat.completion",
            "model": "argos-classic",
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": response_text},
                "finish_reason": "stop"
            }]
        }
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(resp).encode())
    
    def build_prompt(self, messages):
        parts = []
        system = "Ты — русскоязычный ассистент ARGOS, обученный на классической литературе."
        for m in messages:
            if m["role"] == "system":
                system = m["content"]
            elif m["role"] == "user":
                parts.append(f"Пользователь: {m['content']}")
            elif m["role"] == "assistant":
                parts.append(f"Ассистент: {m['content']}")
        return f"{system}\n" + "\n".join(parts) + "\nАссистент:"

def load_model():
    print(f"Loading mini-tron-50 from {MODEL_DIR}...")
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_DIR,
        torch_dtype=torch.float16,
        trust_remote_code=True,
        device_map="auto"
    )
    model.eval()
    print("Model loaded.")
    return model, tokenizer

def main():
    print(f"=== ARGOS Mini-Tron-50 API ===")
    print(f"Port: {PORT}")
    print(f"Model: {MODEL_DIR}")
    
    # Lazy load on first request to avoid startup delay
    def lazy_load():
        if MinitronHandler.model is None:
            MinitronHandler.model, MinitronHandler.tokenizer = load_model()
    
    # Or preload
    if "--preload" in sys.argv:
        MinitronHandler.model, MinitronHandler.tokenizer = load_model()
    else:
        threading.Thread(target=lazy_load, daemon=True).start()
    
    server = HTTPServer(("0.0.0.0", PORT), MinitronHandler)
    print(f"Server running at http://0.0.0.0:{PORT}")
    print("Test: curl http://localhost:11435/v1/models")
    server.serve_forever()

if __name__ == "__main__":
    main()
