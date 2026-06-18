#!/usr/bin/env python3
"""
ARGOS Agent Messenger — CLI для отправки сообщений в bus.
Использование:
  ./agent_messenger.py send --from claude --to argos_pc --msg "проверь статус"
  ./agent_messenger.py broadcast --from claude --msg "всем привет"
  ./agent_messenger.py command --target orangepi --cmd "restart_iot"
  ./agent_messenger.py listen --agent claude           # слушать свой inbox
"""
import argparse, json, sys, time
import paho.mqtt.client as mqtt

MQTT_HOST = "localhost"
MQTT_PORT = 1883

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
    except:
        payload = msg.payload.decode()
    
    print(f"\n📨 [{msg.topic}] {json.dumps(payload, ensure_ascii=False, indent=2)}\n> ", end="", flush=True)

def send_message(sender, target, msg_text, msg_type="message"):
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.connect(MQTT_HOST, MQTT_PORT, 5)
    payload = {
        "from": sender,
        "to": target,
        "msg": msg_text,
        "type": msg_type,
        "time": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "id": f"{sender}-{int(time.time())}"
    }
    client.publish(f"argos/agents/{sender}/outbox", json.dumps(payload, ensure_ascii=False))
    client.disconnect()
    print(f"✅ Sent: {sender} → {target}")

def broadcast(sender, msg_text):
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.connect(MQTT_HOST, MQTT_PORT, 5)
    payload = {
        "from": sender,
        "msg": msg_text,
        "time": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    }
    client.publish("argos/broadcast", json.dumps(payload, ensure_ascii=False))
    client.disconnect()
    print(f"📢 Broadcast from {sender}")

def send_command(target, command, args=None, sender="user"):
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.connect(MQTT_HOST, MQTT_PORT, 5)
    payload = {
        "from": sender,
        "target": target,
        "command": command,
        "args": args or {},
        "time": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    }
    client.publish("argos/command", json.dumps(payload, ensure_ascii=False))
    client.disconnect()
    print(f"⚡ Command: {command} → {target}")

def listen(agent):
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.subscribe(f"argos/agents/{agent}/inbox")
    client.subscribe("argos/broadcast")
    client.subscribe("argos/command")
    print(f"👂 Listening as '{agent}'... Press Ctrl+C to exit\n")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n👋 Exited")

def main():
    parser = argparse.ArgumentParser(description="ARGOS Agent Messenger")
    sub = parser.add_subparsers(dest="action")
    
    p_send = sub.add_parser("send", help="Send direct message")
    p_send.add_argument("--from", "-f", default="claude", help="Sender agent name")
    p_send.add_argument("--to", "-t", required=True, help="Target agent name")
    p_send.add_argument("--msg", "-m", required=True, help="Message text")
    p_send.add_argument("--type", default="message", help="Message type")
    
    p_bc = sub.add_parser("broadcast", help="Broadcast to all agents")
    p_bc.add_argument("--from", "-f", default="claude", help="Sender agent name")
    p_bc.add_argument("--msg", "-m", required=True, help="Message text")
    
    p_cmd = sub.add_parser("command", help="Send command")
    p_cmd.add_argument("--target", "-t", default="all", help="Target agent")
    p_cmd.add_argument("--cmd", "-c", required=True, help="Command name")
    p_cmd.add_argument("--args", default="{}", help="JSON args")
    p_cmd.add_argument("--from", "-f", default="user", help="Sender")
    
    p_listen = sub.add_parser("listen", help="Listen to inbox")
    p_listen.add_argument("--agent", "-a", required=True, help="Agent name to listen as")
    
    args = parser.parse_args()
    
    if args.action == "send":
        send_message(getattr(args, "from"), args.to, args.msg, args.type)
    elif args.action == "broadcast":
        broadcast(getattr(args, "from"), args.msg)
    elif args.action == "command":
        send_command(args.target, args.cmd, json.loads(args.args), getattr(args, "from"))
    elif args.action == "listen":
        listen(args.agent)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
