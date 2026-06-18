---
argos_import: project_file
source_path: V100_DEPLOYMENT_GUIDE.md
source_abs: F:\debug\argoss\V100_DEPLOYMENT_GUIDE.md
source_ext: .md
source_sha256: ca558f9fdfa1900ea2589e16536ca150e679ff9b0e09b592da69e4a6463b9d10
text_sha256: ca558f9fdfa1900ea2589e16536ca150e679ff9b0e09b592da69e4a6463b9d10
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-08 19:41:31
---

# V100_DEPLOYMENT_GUIDE.md

- Source: `V100_DEPLOYMENT_GUIDE.md`
- Extract: `text`
- SHA256: `ca558f9fdfa1900ea2589e16536ca150e679ff9b0e09b592da69e4a6463b9d10`

## Content

# ARGOS V100 Deployment Package
# Для запуска обученной модели на V100 (16GB)

## ВАЖНО: V100 не поддерживает BF16! Только FP16.

---

## Вариант 1: GGUF (РЕКОМЕНДУЕТСЯ) — работает везде

### Требования:
- llama.cpp или llama-cpp-python
- 6-8GB VRAM (Q4_K_M квантизация)

### Установка:
```bash
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
```

### Запуск Python:
```python
from llama_cpp import Llama

llm = Llama(
    model_path="argos-nemo12b-gguf/unsloth.Q4_K_M.gguf",
    n_gpu_layers=-1,  # Все слои на GPU
    n_ctx=4096,       # Контекст
    verbose=True
)

output = llm(
    "System: You are ARGOS.\nUser: Привет!\nAssistant:",
    max_tokens=512,
    temperature=0.7,
    stop=["User:", "System:"]
)
print(output['choices'][0]['text'])
```

### Запуск сервера (REST API):
```bash
llama-server \
  -m argos-nemo12b-gguf/unsloth.Q4_K_M.gguf \
  --host 0.0.0.0 \
  --port 8080 \
  -c 4096 \
  -ngl 999 \
  --temp 0.7
```

---

## Вариант 2: Merged Model (HuggingFace transformers)

### Требования:
- transformers, torch, accelerate
- 12-16GB VRAM (FP16 + 4-bit)

### Установка:
```bash
pip install transformers torch accelerate bitsandbytes
```

### Запуск:
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# V100: FP16 only, 4-bit quantization
model_path = "argos-nemo12b-merged"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,  # ВАЖНО: FP16, не BF16!
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    quantization_config=bnb_config,
    device_map="auto",
    torch_dtype=torch.float16,
    trust_remote_code=True,
)

tokenizer = AutoTokenizer.from_pretrained(model_path)

# Inference
prompt = "System: You are ARGOS.\nUser: Привет!\nAssistant:"
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

outputs = model.generate(
    **inputs,
    max_new_tokens=512,
    temperature=0.7,
    do_sample=True,
    pad_token_id=tokenizer.eos_token_id,
)

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
```

---

## Вариант 3: Docker (рекомендуется для продакшена)

### Dockerfile:
```dockerfile
FROM nvidia/cuda:12.1-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121

COPY argos-nemo12b-gguf/ /models/

EXPOSE 8080

CMD ["python3", "-m", "llama_cpp.server", 
     "--model", "/models/unsloth.Q4_K_M.gguf",
     "--host", "0.0.0.0", 
     "--port", "8080",
     "--n_gpu_layers", "999",
     "--n_ctx", "4096"]
```

### Сборка и запуск:
```bash
docker build -t argos-v100 .
docker run --gpus all -p 8080:8080 argos-v100
```

---

## Проверка VRAM на V100:

```bash
nvidia-smi
# Ожидается: ~6-8GB занято (GGUF Q4_K_M)
# Или ~12-14GB (Merged FP16 + 4-bit)
```

---

## Что экспортировать с A100:

1. **GGUF** (argos-nemo12b-gguf/) — приоритет #1
2. **Merged** (argos-nemo12b-merged/) — если нужен HF формат

Оба варианта уже генерируются в Cell 6 твоего A100 ноутбука.

---

## Производительность V100:
- GGUF Q4_K_M: ~20-30 tokens/sec
- Merged FP16 4-bit: ~15-25 tokens/sec
- Контекст: до 4096 токенов

**Готово к развёртыванию на V100!**

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
