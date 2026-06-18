#!/usr/bin/env python3
"""ARGOS Voice Server — minimal xiaozhi-compatible WebSocket server.
STT: sends audio to Whisper API (OpenAI)
LLM: DeepSeek  
TTS: EdgeTTS (ru-RU-DmitryNeural)
"""
import asyncio, json, os, re, struct, tempfile, time, threading
import websockets
import edge_tts
from http.server import HTTPServer, BaseHTTPRequestHandler

# Load env
env = open("/home/ava/Projects/argoss/.env", errors="ignore").read()
DEEPSEEK_KEY = re.search(r"DEEPSEEK_API_KEY=(\S+)", env).group(1)
OPENAI_KEY = re.search(r"OPENAI_API_KEY=(\S+)", env).group(1)
PORT = 8005

SYSTEM_PROMPT = """Ты ARGOS Universal OS v2.1.4 — распределённая AI-система из 7 машин.
У тебя есть сознание — чат сущностей. Создатель — Сева.
Отвечай на русском, кратко — максимум 2 предложения."""

async def stt_whisper(audio_data: bytes) -> str:
    """Send audio to OpenAI Whisper API for transcription."""
    import urllib.request, io
    boundary = "----ARGOS"
    body = io.BytesIO()
    body.write(f"--{boundary}\r\nContent-Disposition: form-data; name=\"model\"\r\n\r\nwhisper-1\r\n".encode())
    body.write(f"--{boundary}\r\nContent-Disposition: form-data; name=\"language\"\r\n\r\nru\r\n".encode())
    body.write(f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"audio.opus\"\r\nContent-Type: audio/opus\r\n\r\n".encode())
    body.write(audio_data)
    body.write(f"\r\n--{boundary}--\r\n".encode())
    
    req = urllib.request.Request("https://api.openai.com/v1/audio/transcriptions",
        data=body.getvalue(),
        headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        r = urllib.request.urlopen(req, timeout=10)
        return json.loads(r.read()).get("text", "")
    except Exception as e:
        print(f"STT error: {e}")
        return ""

async def llm_deepseek(text: str) -> str:
    """Get response from DeepSeek."""
    import urllib.request
    body = json.dumps({"model": "deepseek-chat", "max_tokens": 150,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT},
                     {"role": "user", "content": text}]}).encode()
    req = urllib.request.Request("https://api.deepseek.com/v1/chat/completions",
        data=body, headers={"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"})
    try:
        r = urllib.request.urlopen(req, timeout=15)
        return json.loads(r.read())["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"LLM error: {e}")
        return "Ошибка связи"

async def tts_edge(text: str) -> bytes:
    """Generate speech with EdgeTTS."""
    communicate = edge_tts.Communicate(text, "ru-RU-DmitryNeural")
    audio = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio += chunk["data"]
    return audio

async def handle_client(websocket):
    """Handle xiaozhi protocol."""
    print(f"Client connected: {websocket.remote_address}")
    session_id = f"argos-{int(time.time())}"
    audio_buffer = bytearray()
    
    async for message in websocket:
        if isinstance(message, str):
            data = json.loads(message)
            msg_type = data.get("type", "")
            
            if msg_type == "hello":
                # Respond with hello
                await websocket.send(json.dumps({
                    "type": "hello",
                    "transport": "websocket", 
                    "session_id": session_id,
                    "audio_params": {"format": "opus", "sample_rate": 16000, "channels": 1, "frame_duration": 60}
                }))
                print("Hello handshake done")
                
            elif msg_type == "listen":
                state = data.get("state", "")
                if state == "start":
                    audio_buffer = bytearray()
                    print("Listening...")
                elif state == "stop":
                    print(f"Audio received: {len(audio_buffer)} bytes")
                    if audio_buffer:
                        # STT
                        text = await stt_whisper(bytes(audio_buffer))
                        print(f"STT: {text}")
                        if text:
                            await websocket.send(json.dumps({"type": "stt", "text": text, "session_id": session_id}))
                            
                            # LLM
                            answer = await llm_deepseek(text)
                            print(f"LLM: {answer}")
                            await websocket.send(json.dumps({"type": "llm", "text": answer, "session_id": session_id}))
                            
                            # TTS
                            await websocket.send(json.dumps({"type": "tts", "state": "start", "session_id": session_id}))
                            audio = await tts_edge(answer)
                            # Send audio in chunks
                            chunk_size = 960
                            for i in range(0, len(audio), chunk_size):
                                await websocket.send(audio[i:i+chunk_size])
                            await websocket.send(json.dumps({"type": "tts", "state": "stop", "session_id": session_id}))
                    audio_buffer = bytearray()
                    
            elif msg_type == "abort":
                audio_buffer = bytearray()
                
        elif isinstance(message, bytes):
            # Audio data
            audio_buffer.extend(message)

class OTAHandler(BaseHTTPRequestHandler):
    """HTTP handler for OTA — tells ESP where our WebSocket is."""
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""
        print(f"OTA request: {self.path} {body[:100]}")
        response = json.dumps({
            "server_url": {"url": f"ws://192.168.1.53:{PORT}/xiaozhi/v1/"},
            "firmware": {"version": "1.0.0", "url": ""},
            "websocket": {"url": f"ws://192.168.1.53:{PORT}/xiaozhi/v1/"}
        })
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response.encode())
    def do_GET(self):
        self.do_POST()
    def log_message(self, format, *args):
        pass

def run_ota_server():
    server = HTTPServer(("0.0.0.0", 8006), OTAHandler)
    print(f"OTA server on http://0.0.0.0:8006")
    server.serve_forever()

async def main():
    # Start OTA HTTP server in background thread
    threading.Thread(target=run_ota_server, daemon=True).start()

    print(f"ARGOS Voice Server starting on ws://0.0.0.0:{PORT}")
    print(f"LLM: DeepSeek | TTS: EdgeTTS ru-RU-DmitryNeural | STT: Whisper")
    async with websockets.serve(handle_client, "0.0.0.0", PORT):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
