# ARGOS «Вспомнить Всё» — Spaced Repetition + Mini-Tron-50

**Дата:** 2026-05-14  
**Статус:** Интеграция готова к деплою  
**Vault:** `/home/ava/Projects/argoss/vault`

---

## 🧠 Часть 1: Spaced Repetition в Obsidian

### Цель
Автоматическое интервальное повторение заметок ARGOS: идеи, команды, архитектура, железо — всё закрепляется по кривой Эббингауза.

### Плагин
**`obsidian-spaced-repetition`** by Stephen Mwangi  
- 470K+ загрузок, поддержка русского, SM-2/Anki алгоритм
- GitHub: `st3v3nmw/obsidian-spaced-repetition`

### Установка

```
Settings → Community plugins → Browse → "Spaced Repetition" → Install → Enable
```

### Настройка для ARGOS

**Settings → Spaced Repetition:**

| Параметр | Значение | Почему |
|----------|----------|--------|
| Flashcard tags | `#flashcards` | Тег для карточек |
| Card separator | `::` | Формат `Вопрос::Ответ` |
| Multiline card separator | `?` | Многострочные карточки |
| Enable Cloze | ✅ | `==выделение==` → cloze deletion |
| bury sibling cards | ✅ | Не показывать связанные подряд |
| Review notification | ✅ | Напоминание о повторении |

### Форматы карточек (примеры из vault'а)

**Single-line (простой факт):**
```markdown
Какой IP у argos-pc? :: 192.168.1.66
#flashcards
```

**Multi-line (команда с контекстом):**
```markdown
Как запустить KolibriOS в Termux?
?
```bash
qemu-system-i386 -fda kolibri.img -boot a
```
#flashcards/ARGOS
```

**Cloze (заполнить пропуск):**
```markdown
ESP8266 подключён к WiFi ==SiG== с IP ==192.168.1.181==
#flashcards/IoT
```

**Reversed (двусторонняя):**
```markdown
192.168.1.66 ::: argos-pc (GPU-сервер)
#flashcards/P2P
```

### Workflow «Вспомнить Всё»

1. **При чтении лога** выделяешь ключевые факты `==так==`
2. **Добавляешь** `#flashcards` в конец заметки
3. **Плагин** сам найдёт карточки при следующем review
4. **Ctrl+P → "Review flashcards"** — пошёл повтор

---

## 🤖 Часть 2: Mini-Tron-50 — русская классика в ARGOS

### Контекст
Пользователь (13.05.2026) запросил установку полного ML/AI стека и поделился ссылками:
- Habr: «Мини-Трон-50» (статья 1034858)
- HuggingFace: `Imperius/mini-tron-50` — диалоговая LLM 50M параметров
- Датасет: `ru-classic` — русская классика XIX–XX века
- Codeberg: парсер, токенайзер BPE, NanoGPT реализации

### Архитектура интеграции

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  argos-laptop   │────▶│  Ollama Local   │◀────│  mini-tron-50  │
│  (compute,ai)   │     │  (GGUF / RAW)   │     │  (50M params) │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                              │
                              ▼
                        ┌─────────────────┐
                        │   Obsidian MCP  │
                        │   (vault query) │
                        └─────────────────┘
```

### Шаг 1: Конвертация в GGUF для Ollama

```bash
# На ПК (argos-pc, RX 580) или Colab
pip install transformers llama-cpp-python

# Скачать с HF
git clone https://huggingface.co/Imperius/mini-tron-50
cd mini-tron-50

# Конвертация PyTorch → GGUF
python3 << 'EOF'
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model = AutoModelForCausalLM.from_pretrained(
    "./",
    torch_dtype=torch.float16,
    trust_remote_code=True
)
tokenizer = AutoTokenizer.from_pretrained("./", trust_remote_code=True)

# Save as llama.cpp compatible
from llama_cpp import Llama
# ... или используем convert_hf_to_gguf.py из llama.cpp
EOF
```

### Шаг 2: Ollama Modelfile

```dockerfile
# /home/ava/Projects/argoss/models/mini-tron-50/Modelfile
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
```

```bash
ollama create argos-classic -f Modelfile
ollama run argos-classic
```

### Шаг 3: Интеграция с Brain API

```python
# argos_brain_api.py — добавить provider
PROVIDERS = {
    "ollama_local": "http://localhost:11434",
    "ollama_pc": "http://192.168.1.66:11434",
    "cloudflare": "https://api.cloudflare.com...",
    "argos-classic": "http://localhost:11434",  # ← mini-tron-50
}

async def ask_classic(prompt: str) -> str:
    """Диалоговая модель на русской классике"""
    return await ollama_chat("argos-classic", prompt)
```

### Шаг 4: Датасет ru-classic для дообучения

```bash
# Скачать датасет
git clone https://huggingface.co/datasets/Imperius/ru-classic

# Использовать для LoRA / full fine-tune
# Формат: .txt файлы с произведениями (Чехов, Достоевский, Толстой...)

# Подготовка для Instruction Tuning
cat > ru_classic_instruction.jsonl << 'EOF'
{"instruction": "Перескажи суть отрывка", "input": "...", "output": "..."}
{"instruction": "Объясни метафору", "input": "...", "output": "..."}
EOF
```

---

## 📦 ML/AI Stack (установлен 13.05.2026)

### Python (pip)
```
numpy pandas scipy scikit-learn xgboost catboost lightgbm
torch torchvision torchaudio tensorflow keras
transformers langchain llamaindex openai anthropic
opencv-python ultralytics pillow spacy nltk
```

### Arch Linux (pacman)
```
python-numpy python-pandas python-scipy python-scikit-learn
python-xgboost python-pytorch python-torchvision python-torchaudio
python-tensorflow python-keras python-transformers
python-opencv python-pillow python-spacy python-nltk
android-tools android-udev openjdk-src qemu-full lxc dnsmasq
```

### AUR (yay)
```
python-langchain python-llamaindex-core waydroid waydroid-image
```

---

## 🔗 Связи
- [[2026-05-14.md]] — Daily Note (установлены пакеты 13.05)
- [[AI Providers]] — Ollama, Cloudflare, теперь + argos-classic
- [[ARGOS System Architecture 2026-05-07]] — куда встроить mini-tron-50
- [[ARGOS Train Dataset v1.0]] — шаблон датасетов для дообучения
- [[Backbone Hub]]

[[Backbone Hub]]
