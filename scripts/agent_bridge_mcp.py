#!/usr/bin/env python3
"""
ARGOS MCP ↔ Message Bus Bridge
Позволяет ARGOS MCP получать команды из MQTT bus и отправлять ответы.
Запускается как отдельный агент, слушает argos/agents/argos_laptop/inbox,
пересылает в MCP localhost:8000/mcp, ответ публикует обратно в bus.
"""
import json, time, urllib.request
import paho.mqtt.client as mqtt

MQTT_HOST = "localhost"
MQTT_PORT = 1883
MCP_URL = "http://localhost:8000/mcp"

def mcp_call(tool_name, arguments):
    """Вызов MCP инструмента через HTTP JSON-RPC"""
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments},
        "id": int(time.time())
    }
    try:
        req = urllib.request.Request(MCP_URL, data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
    except:
        return
    
    topic = msg.topic
    if topic == "argos/agents/argos_laptop/inbox":
        msg_type = payload.get("type", "message")
        sender = payload.get("from", "unknown")
        msg_data = payload.get("msg", {})
        msg_id = payload.get("id", "")
        
        if msg_type == "command" and isinstance(msg_data, dict):
            cmd = msg_data.get("command", "")
            args = msg_data.get("args", {})
            print(f"[{time.strftime('%H:%M:%S')}] Command from {sender}: {cmd}")
            
            # Route to MCP tool
            if cmd == "status":
                result = mcp_call("status", {})
            elif cmd == "providers":
                result = mcp_call("providers", {})
            elif cmd == "ask":
                result = mcp_call("ask", {"prompt": args.get("prompt",""), "model": args.get("model","llama3.1:8b")})
            else:
                result = {"result": f"Unknown command: {cmd}"}
            
            # Reply to bus
            reply = {
                "from": "argos_laptop",
                "to": sender,
                "msg": {"reply_to": cmd, "result": result},
                "type": "reply",
                "time": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
                "id": f"reply-{msg_id}"
            }
            client.publish(f"argos/agents/{sender}/inbox", json.dumps(reply, ensure_ascii=False))
            print(f"  → Replied to {sender}")
        
        elif msg_type == "message":
            print(f"[{time.strftime('%H:%M:%S')}] Message from {sender}: {str(msg_data)[:80]}")

def main():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.subscribe("argos/agents/argos_laptop/inbox")
    client.subscribe("argos/broadcast")
    
    # Heartbeat
    def heartbeat():
        while True:
            time.sleep(60)
            client.publish("argos/heartbeat", json.dumps({
                "agent": "argos_laptop",
                "status": "online",
                "time": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
            }))
    import threading
    threading.Thread(target=heartbeat, daemon=True).start()
    
    print(f"[{time.strftime('%H:%M:%S')}] MCP Bridge active. Listening argos_laptop inbox...")
    client.loop_forever()

if __name__ == "__main__":
    main()
