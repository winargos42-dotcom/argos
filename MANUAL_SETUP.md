# MANUAL SETUP GUIDE - ARGOS GPU
# Шаг 1: Скачать модель вручную

# Откройте PowerShell и выполните:

# 1. Создать папку
mkdir F:\ROCm\models -Force

# 2. Скачать модель (это займет 5-10 минут)
curl -L -o F:\ROCm\models\tinyllama-1.1b-chat-q4_k_m.gguf "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"

# 3. Проверить размер (должно быть ~600 MB)
Get-Item F:\ROCm\models\tinyllama-1.1b-chat-q4_k_m.gguf

# Шаг 2: Запустить llama-server с GPU

# 1. Убить старые процессы
taskkill /F /IM llama-server.exe 2>$null
taskkill /F /IM ollama.exe 2>$null

# 2. Запустить llama-server
& "C:\Users\AvA\.docker\bin\inference\llama-server.exe" -m "F:\ROCm\models\tinyllama-1.1b-chat-q4_k_m.gguf" --port 11437 -ngl 999 --host 127.0.0.1

# 3. Проверить в другом окне PowerShell:
curl http://localhost:11437/health

# Шаг 3: Запустить Ollama (CPU fallback)

$env:OLLAMA_NUM_THREADS = "4"
$env:OLLAMA_MODELS = "F:\model"
ollama serve

# Шаг 4: VM Sweden через Azure Portal

# 1. Откройте https://portal.azure.com
# 2. Найдите VM "ollama" (Resource Group: rg-argos)
# 3. Перейдите в Serial Console
# 4. Выполните:
sudo docker start ollama
# или если не запущен:
sudo docker run -d --name ollama -p 11434:11434 -v ollama:/root/.ollama ollama/ollama

# 5. Установите модель:
sudo docker exec ollama ollama pull poilopr57/argoss
