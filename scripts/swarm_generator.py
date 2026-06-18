#!/usr/bin/env python3
"""
ARGOS Swarm Generator — генерирует docker-compose для N сервисов.
Phase 3: 150 сервисов = swarm stack deploy.
"""
import yaml
from pathlib import Path
from datetime import datetime

# Шаблон одного сервиса
SERVICE_TEMPLATE = {
    "image": "{image}",
    "deploy": {
        "replicas": 1,
        "restart_policy": {"condition": "any", "delay": "5s", "max_attempts": 3},
        "resources": {
            "limits": {"cpus": "0.5", "memory": "256M"},
            "reservations": {"cpus": "0.1", "memory": "64M"}
        },
        "labels": ["argos.component={type}"]
    },
    "networks": ["argos_overlay"],
    "logging": {"driver": "json-file", "options": {"max-size": "10m", "max-file": "3"}},
}

def generate_service(name, s_type, image, ports=None, env=None, volumes=None):
    s = {
        "image": image,
        "deploy": {
            "replicas": 1,
            "restart_policy": {"condition": "any", "delay": "5s", "max_attempts": 3},
            "resources": {
                "limits": {"cpus": "0.5", "memory": "256M"},
                "reservations": {"cpus": "0.1", "memory": "64M"}
            },
            "labels": [f"argos.component={s_type}"]
        },
        "networks": ["argos_overlay"],
        "logging": {"driver": "json-file", "options": {"max-size": "10m", "max-file": "3"}}
    }
    if ports:
        s["ports"] = ports
    if env:
        s["environment"] = env
    if volumes:
        s["volumes"] = volumes
    return {name: s}

def generate_swarm_stack(service_count=24, output=None):
    """Генерирует docker-compose.yml с N сервисами."""
    services = {}
    
    # Core services (всегда присутствуют)
    services.update(generate_service("traefik", "gateway", "traefik:v3.0",
        ports=["80:80", "443:443"],
        volumes=["/var/run/docker.sock:/var/run/docker.sock"]))
    services.update(generate_service("prometheus", "monitor", "prom/prometheus",
        ports=["9090:9090"],
        volumes=["prom_data:/prometheus"]))
    services.update(generate_service("grafana", "monitor", "grafana/grafana",
        ports=["3000:3000"],
        volumes=["grafana_data:/var/lib/grafana"]))
    
    # Auto-generated services: sensor-N, worker-N, inference-N
    for i in range(service_count - 3):
        idx = i + 1
        # Микс типов: sensor, worker, inference, proxy, db, cache
        types = ["sensor", "worker", "inference", "proxy", "db", "cache"]
        t = types[i % len(types)]
        name = f"argos-{t}-{idx:03d}"
        
        images = {
            "sensor": "alpine:latest",
            "worker": "python:3.11-slim",
            "inference": "ollama/ollama:latest",
            "proxy": "nginx:alpine",
            "db": "postgres:15-alpine",
            "cache": "redis:7-alpine"
        }
        
        services.update(generate_service(name, t, images[t]))
    
    compose = {
        "version": "3.8",
        "services": services,
        "networks": {
            "argos_overlay": {"driver": "overlay", "attachable": True}
        },
        "volumes": {
            "prom_data": {"driver": "local"},
            "grafana_data": {"driver": "local"}
        }
    }
    
    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w") as f:
            yaml.dump(compose, f, default_flow_style=False, allow_unicode=True)
        print(f"[Swarm] Generated {len(services)} services → {output}")
    return compose

if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/argos_swarm.yml"
    generate_swarm_stack(n, out)
    print(f"[Swarm] Total: {n} services | Deploy: docker stack deploy -c {out} argos")
