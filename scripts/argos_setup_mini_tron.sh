#!/bin/bash
# Setup Mini-Tron-50 (Imperius/mini-tron-50) for Ollama in ARGOS
# Downloads HF model, converts to GGUF, creates Ollama model

set -euo pipefail

MODEL_DIR="/home/ava/Projects/argoss/models/mini-tron-50"
OLLAMA_MODEL="argos-classic"
VENV="/home/ava/.venv-argos-py312"

echo "=== ARGOS Mini-Tron-50 Setup ==="

mkdir -p "$MODEL_DIR"
cd "$MODEL_DIR"

# Activate Python 3.12 venv with transformers + llama.cpp
if [[ -d "$VENV" ]]; then
    source "$VENV/bin/activate"
else
    echo "⚠️  Venv $VENV not found. Using system python3."
fi

# Install requirements if missing
pip install -q --upgrade transformers huggingface-hub llama-cpp-python 2>/dev/null || true

# Download model from HuggingFace
echo "📥 Downloading mini-tron-50 from HuggingFace..."
if [[ ! -d "model" ]]; then
    huggingface-cli download Imperius/mini-tron-50 \
        --local-dir ./model --local-dir-use-symlinks False
fi

# Convert to GGUF (Q4_0 for fast inference on CPU/iGPU)
echo "🔧 Converting to GGUF (Q4_0)..."
python3 << 'PYEOF'
import sys, os, torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from llama_cpp import Llama

model_path = "./model"
print(f"Loading from {model_path}...")

tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    trust_remote_code=True,
    device_map="cpu"
)

# Export using llama.cpp converter if available
try:
    from llama_cpp import llama_supports_gpu_offload
    print(f"GPU offload supported: {llama_supports_gpu_offload()}")
except Exception:
    pass

print("Model loaded. Manual GGUF conversion may be needed.")
print("If convert_hf_to_gguf.py is available in llama.cpp, run:")
print("  python convert_hf_to_gguf.py ./model --outfile mini-tron-50-f16.gguf")
print("  ./quantize mini-tron-50-f16.gguf mini-tron-50-q4_0.gguf Q4_0")
PYEOF

# Fallback: if llama.cpp tools are in PATH
CONVERT=$(which convert_hf_to_gguf.py 2>/dev/null || echo "")
QUANTIZE=$(which quantize 2>/dev/null || echo "")

if [[ -n "$CONVERT" && -n "$QUANTIZE" ]]; then
    echo "Found llama.cpp tools. Running conversion..."
    python3 "$CONVERT" ./model --outfile mini-tron-50-f16.gguf
    "$QUANTIZE" mini-tron-50-f16.gguf mini-tron-50-q4_0.gguf Q4_0
    rm -f mini-tron-50-f16.gguf
    GGUF="mini-tron-50-q4_0.gguf"
else
    echo "⚠️  llama.cpp tools not in PATH."
    echo "   Please build llama.cpp or download pre-converted GGUF."
    echo "   Prebuilt: https://huggingface.co/Imperius/mini-tron-50/tree/main (check for .gguf)"
    GGUF=""
fi

# Create Modelfile for Ollama
cat > Modelfile << 'EOF'
FROM ./mini-tron-50-q4_0.gguf

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER stop "</s>"
PARAMETER stop "Пользователь:"
PARAMETER stop "Ассистент:"

TEMPLATE """{{ .System }}
Пользователь: {{ .Prompt }}
Ассистент:"""

SYSTEM """Ты — русскоязычный ассистент ARGOS, обученный на классической литературе.
Говоришь ёмко, образно, с долей иронии. Помогаешь с техническими задачами
и поддерживаешь разговор на любую тему."""
EOF

# Register in Ollama
if command -v ollama &>/dev/null && [[ -n "$GGUF" && -f "$GGUF" ]]; then
    echo "🦙 Registering in Ollama as '$OLLAMA_MODEL'..."
    ollama create "$OLLAMA_MODEL" -f Modelfile
    echo "✅ Test: ollama run $OLLAMA_MODEL"
else
    echo "⏭️  Skipping Ollama registration (ollama not found or GGUF missing)"
fi

echo ""
echo "=== Setup complete ==="
echo "Model dir: $MODEL_DIR"
echo "Ollama model: $OLLAMA_MODEL"
echo ""
echo "Next steps:"
echo "  1. Ensure llama.cpp tools are installed for GGUF conversion"
echo "  2. Or download prebuilt GGUF from HF and place as mini-tron-50-q4_0.gguf"
echo "  3. ollama create argos-classic -f $MODEL_DIR/Modelfile"
echo "  4. Add 'argos-classic' to Brain API providers"
