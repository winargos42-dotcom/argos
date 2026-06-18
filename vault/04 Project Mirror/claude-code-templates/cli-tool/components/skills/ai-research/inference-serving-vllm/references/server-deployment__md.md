---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/inference-serving-vllm/references/server-deployment.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\inference-serving-vllm\references\server-deployment.md
source_ext: .md
source_sha256: eb6f58d5daaabdda7be7347ae5f6d6925f739145eabece38659bb14c8cd8595c
text_sha256: 7db618ec40b865fe2efacf46c04c3d5dc233fc64a3c63d26451afb97b795113e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:31
---

# server-deployment.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/inference-serving-vllm/references/server-deployment.md`
- Extract: `text`
- SHA256: `eb6f58d5daaabdda7be7347ae5f6d6925f739145eabece38659bb14c8cd8595c`

## Content

# Server Deployment Patterns

## Contents
- Docker deployment
- Kubernetes deployment
- Load balancing with Nginx
- Multi-node distributed serving
- Production configuration examples
- Health checks and monitoring

## Docker deployment

**Basic Dockerfile**:
```dockerfile
FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

RUN apt-get update && apt-get install -y python3-pip
RUN pip install vllm

EXPOSE 8000

CMD ["vllm", "serve", "meta-llama/Llama-3-8B-Instruct", \
     "--host", "0.0.0.0", "--port", "8000", \
     "--gpu-memory-utilization", "0.9"]
```

**Build and run**:
```bash
docker build -t vllm-server .
docker run --gpus all -p 8000:8000 vllm-server
```

**Docker Compose** (with metrics):
```yaml
version: '3.8'
services:
  vllm:
    image: vllm/vllm-openai:latest
    command: >
      --model meta-llama/Llama-3-8B-Instruct
      --gpu-memory-utilization 0.9
      --enable-metrics
      --metrics-port 9090
    ports:
      - "8000:8000"
      - "9090:9090"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

## Kubernetes deployment

**Deployment manifest**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-server
spec:
  replicas: 2
  selector:
    matchLabels:
      app: vllm
  template:
    metadata:
      labels:
        app: vllm
    spec:
      containers:
      - name: vllm
        image: vllm/vllm-openai:latest
        args:
          - "--model=meta-llama/Llama-3-8B-Instruct"
          - "--gpu-memory-utilization=0.9"
          - "--enable-prefix-caching"
        resources:
          limits:
            nvidia.com/gpu: 1
        ports:
        - containerPort: 8000
          name: http
        - containerPort: 9090
          name: metrics
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 30
---
apiVersion: v1
kind: Service
metadata:
  name: vllm-service
spec:
  selector:
    app: vllm
  ports:
  - port: 8000
    targetPort: 8000
    name: http
  - port: 9090
    targetPort: 9090
    name: metrics
  type: LoadBalancer
```

## Load balancing with Nginx

**Nginx configuration**:
```nginx
upstream vllm_backend {
    least_conn;  # Route to least-loaded server
    server localhost:8001;
    server localhost:8002;
    server localhost:8003;
}

server {
    listen 80;

    location / {
        proxy_pass http://vllm_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;

        # Timeouts for long-running inference
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Metrics endpoint
    location /metrics {
        proxy_pass http://localhost:9090/metrics;
    }
}
```

**Start multiple vLLM instances**:
```bash
# Terminal 1
vllm serve MODEL --port 8001 --tensor-parallel-size 1

# Terminal 2
vllm serve MODEL --port 8002 --tensor-parallel-size 1

# Terminal 3
vllm serve MODEL --port 8003 --tensor-parallel-size 1

# Start Nginx
nginx -c /path/to/nginx.conf
```

## Multi-node distributed serving

For models too large for single node:

**Node 1** (master):
```bash
export MASTER_ADDR=192.168.1.10
export MASTER_PORT=29500
export RANK=0
export WORLD_SIZE=2

vllm serve meta-llama/Llama-2-70b-hf \
  --tensor-parallel-size 8 \
  --pipeline-parallel-size 2
```

**Node 2** (worker):
```bash
export MASTER_ADDR=192.168.1.10
export MASTER_PORT=29500
export RANK=1
export WORLD_SIZE=2

vllm serve meta-llama/Llama-2-70b-hf \
  --tensor-parallel-size 8 \
  --pipeline-parallel-size 2
```

## Production configuration examples

**High throughput** (batch-heavy workload):
```bash
vllm serve MODEL \
  --max-num-seqs 512 \
  --gpu-memory-utilization 0.95 \
  --enable-prefix-caching \
  --trust-remote-code
```

**Low latency** (interactive workload):
```bash
vllm serve MODEL \
  --max-num-seqs 64 \
  --gpu-memory-utilization 0.85 \
  --enable-chunked-prefill
```

**Memory-constrained** (40GB GPU for 70B model):
```bash
vllm serve TheBloke/Llama-2-70B-AWQ \
  --quantization awq \
  --tensor-parallel-size 1 \
  --gpu-memory-utilization 0.95 \
  --max-model-len 4096
```

## Health checks and monitoring

**Health check endpoint**:
```bash
curl http://localhost:8000/health
# Returns: {"status": "ok"}
```

**Readiness check** (wait for model loaded):
```bash
#!/bin/bash
until curl -f http://localhost:8000/health; do
    echo "Waiting for vLLM to be ready..."
    sleep 5
done
echo "vLLM is ready!"
```

**Prometheus scraping**:
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'vllm'
    static_configs:
      - targets: ['localhost:9090']
    metrics_path: '/metrics'
    scrape_interval: 15s
```

**Grafana dashboard** (key metrics):
- Requests per second: `rate(vllm_request_success_total[5m])`
- TTFT p50: `histogram_quantile(0.5, vllm_time_to_first_token_seconds_bucket)`
- TTFT p99: `histogram_quantile(0.99, vllm_time_to_first_token_seconds_bucket)`
- GPU cache usage: `vllm_gpu_cache_usage_perc`
- Active requests: `vllm_num_requests_running`

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
