---
language:
  - ru
license: apache-2.0
library_name: pytorch
tags:
  - text-generation
  - russian
  - chat
  - chatbot
  - nanogpt
  - small-llm
  - sft
  - educational
  - research
datasets:
  ZeroAgency/ru-big-russian-dataset
pipeline_tag: text-generation
inference: false
---
## mini-tron-50 (SFT) (Russian and English)

## English
> **Translator's note:** This is a translation from Russian. Model outputs in the examples below are rendered in English, but originally generated in Russian.

---

A 50M-parameter GPT-2-style language model trained from scratch on a Russian SFT corpus as a chatbot. Illustrates **what can be squeezed out of a model this size** without pretraining on raw text.

Git-source - https://codeberg.org/imperius/mini-tron-50

## TL;DR

- **Architecture**: 10 layer × 8 head × 512 emb (GPT-2 style), 47.85M params
- **Trained from scratch**: SFT on ~1 GB of chat data (1.7M dialogs), 1 epoch
- **Hardware**: 1× RTX 3050 Laptop (4 GB VRAM), 13 hours
- **Tokenizer**: SentencePiece BPE, 32k vocab, custom-trained on the corpus
- **Format**: ChatML with special tokens `<|system|>`, `<|user|>`, `<|assistant|>`, `<|endoftext|>`
- **Loss masking**: only on assistant tokens (standard SFT trick)
- **Status**: SFT phase successful; KTO phase attempted and failed (see below)

The model **has not reached its ceiling** — this is one of its key features. It was trained for exactly one epoch over the corpus (Chinchilla-optimal for 50M), and the loss curves show that validation loss had not yet plateaued. Further training or continued training on new data will likely yield noticeable improvement.

## Architecture

```text
GPTConfig(
    n_layer    = 10,
    n_head     = 8,
    n_embd     = 512,
    block_size = 1024,
    vocab_size = 32000,
    bias       = False,
    dropout    = 0.1,
)
```

Standard GPT-2 without bias. Tied embeddings (`transformer.wte` shared with `lm_head`). Attention uses `F.scaled_dot_product_attention` (flash-attn under the hood on Ampere+).

## Capabilities

| Capability | Quality |
| --- | --- |
| Russian grammar | ✅ flawless (cases, agreement, syntax) |
| Chat format (responds as assistant) | ✅ stable |
| Markdown structure (lists, **bold**, headers) | ✅ imitates GPT-4 style |
| Self-identification ("I am an AI assistant") | ✅ says the right words |
| EOS completion | ✅ usually stops on its own |
| Local coherence (1–2 sentences) | ⚠️ somewhat meaningful in places |
| Response strictly on prompt topic | ⚠️ hears trigger words, not substance |
| Facts and precise knowledge | ❌ hallucinations |
| Arithmetic | ❌ imitates calculation without performing it |
| Multi-step reasoning | ❌ |
| Code (syntax + semantics) | ❌ form is correct, does not work |

## Known failure modes

1. **Canned responses** to simple questions:
   ```
   you> Do you like cats or dogs?
   bot> Hello! I'm glad I could help you today. If you have any questions,
        feel free to contact us. Good luck!
   ```
   A memorized template tail of ChatGPT-style responses.

2. **Tutorial walls** on any open-ended prompt:
   ```
   you> Tell me about yourself
   bot> ### Step 1: Define the task
        ### Step 2: ...
        ### Conclusion
   ```

3. **Token loops** on out-of-distribution prompts:
   ```
   you> Which is greater: 17 or 71?
   bot> To calculate... + 112 - 112 + 112 + 112 - 112 + 112 ... [50+ repeats]
   ```

4. **Semantic mush** in a fully literate wrapper:
   ```
   you> What is 7 times 8?
   bot> 5! = (5 × 8) / 8 = 120. Now divide 120 by 8...
        So, there are 140 ways to choose 7 times 8 in total.
   ```
   The model imitates the genre of school arithmetic without performing the operation itself.

These failure modes are not cured by SFT, but by preference learning + increasing model size.

## Training data

**Source**: `big-russian-dataset` (HuggingFace) — Russian SFT corpus.

| Split | Dialogs | After filtering |
| --- | --- | --- |
| train | 1.71M | 1,709,621 (99.9%) |
| val | 18.5k | 10,396 (56%) |

**Filter**: `overall_score ≥ 6 AND safety ≥ 8 AND pii_leak = 0`.

In train, the dataset authors had already cleaned out the garbage — there are no records with score < 6, so the filter passes almost everything. In val, the score spread of 1–10 was left intentionally for evaluation on hard examples.

**Volume in tokens**: ~1.04 GB of tokens in train.bin, of which ~603M tokens are under loss (assistant + EOT, 57.7%).

## Training parameters

```python
# AdamW
learning_rate = 3e-4   # cosine decay → min_lr=3e-5
weight_decay  = 0.1
beta1, beta2  = 0.9, 0.95
grad_clip     = 1.0

# Schedule
warmup_iters  = 200
max_iters     = 16000   # ~1 epoch
lr_decay_iters = 16000

# Batch
batch_size                  = 2
gradient_accumulation_steps = 32   # effective batch = 64 sequences
block_size                  = 1024
# tokens per iter = 65,536

# System
dtype   = 'bfloat16'
compile = False
```

## Learning curve

```text
iter     0  loss 10.49   (≈ ln(32000), random initialization)
iter   500  loss ~5      (warmup complete, LR at peak)
iter  5500  loss ~2.4    (first saved checkpoint)
iter 11500  loss ~1.7    (third)
iter 14500  loss ~1.5    (best val_loss ~ 1.8)
iter 16000  loss ~1.45   (max_iters reached)
```

Train-val gap at the end ~1.7 nats — a healthy value for SFT on a small model.

## How to use

The model is distributed in nanoGPT (Karpathy) format. **Not directly compatible with `transformers.AutoModelForCausalLM`** without conversion (weight names differ from GPT-2 standard, specifically no bias).

### Option 1 — via nanoGPT repository (Python)

```bash
git clone https://github.com/karpathy/nanoGPT.git
cd nanoGPT
# copy ckpt.pt, tokenizer.model, meta.pkl here
python chat.py --out_dir=<path-to-checkpoint-dir>
```

The `chat.py` from this release provides an interactive REPL with commands to change temperature, top_p, top_k, and repetition_penalty on the fly.

### Option 2 — via pre-built Go single-binary

This release includes a pre-built `nanogpt-chat.exe` (~97 MB) — a single binary with embedded weights, tokenizer, and config. Runs without Python and without GPU. Performance: ~36 tok/sec on a 4-core CPU.

```bash
./nanogpt-chat.exe
```

REPL commands:

```text
/help               help
/show               current parameters
/reset              reset dialog history
/system <text>      change system prompt
/temp <float>       temperature (>0)
/top_p <float>      nucleus sampling
/top_k <int>        top-k
/rep <float>        repetition penalty
/preset <name>      creative | balanced | precise
/quit               exit
```

All commands have single-letter aliases (/h, /s, /r, /q, /t, /p, /k, ...).

### Option 3 — conversion to HuggingFace transformers

Not provided in this release. Requires renaming weights to GPT-2 conventions, adding null biases, and building `GPT2LMHeadModel` with a custom tokenizer (SentencePiece, not GPT-2 BPE). If someone writes a converter — PRs welcome.

## Examples

```text
you> Hello
bot> Hello! I'm ready to help you achieve your goals. Have a great day!

you> Explain in simple words what a black hole is.
bot> First, let's break this down step by step.

  ### Step 1: Studying a black hole
  - This means that a black hole is part of a black hole.
  - It can have different sizes...
  [grammatically correct, but content is nonsense — this is the 50M ceiling on facts]

you> Write bubble sort in Python.
bot> Here is an example of bubble sort in Python:
  ```python
  def merge_sort(arr):
      """Performs bubble sort in sorted order."""
      sorted_array = {}
      for i in range(len(arr)):
          if arr[i] < sorted_array[i - 1]:
              return merge_sort(arr[i], reverse=True)
      return sorted_array
  ```
  [function name merge_sort instead of bubble_sort, dictionary instead of two loops —
   form is correct, implementation is meaningless]
```

Good prompts for this model are short, conversational, and do not require precise facts:

```text
you> Hi, how are you?
you> My name is Alex. What's yours?
you> Name three fruits.
you> Tell me a short fairy tale.
```

## Limitations

- **Knowledge**: the model does **not** contain reliable facts. Do not ask about dates, names, numbers, geography, biology, or medicine. Any response is an imitation of the reference genre, not real information.
- **Reasoning**: multi-step logic is unavailable. Arithmetic is imitated without execution. Code is syntactically plausible but does not work.
- **Length**: the model was trained with `block_size=1024`. Long dialogs (>800 tokens in history) are truncated from the beginning — the model "forgets" earlier utterances.
- **Languages**: Russian only. On English prompts it will attempt to respond, but quality is worse.
- **Safety**: the model was trained only on the filtered part of the dataset (`safety ≥ 8`), but has no special alignment — behavior on overtly harmful prompts is not guaranteed.

## What didn't work

After SFT, an attempt was made at preference learning via **KTO** to suppress known failure modes. Both attempts (β=0.1 and β=0.03) produced a completely destroyed model — coherent responses turned into semantic garbage. Detailed root-cause analysis is in `04_kto_attempts.md` of the accompanying report.

In short: a combination of (a) a bug in the loss implementation (missing `clamp(z_ref, 0)`) and (b) asymmetric difficulty between chosen data and self-generated rejected. After fixing the bug, degradation still remained, just slower.

A curious side-effect: after KTO, the model drifted not just into noise, but into an "aphoristic-philosophical" register — a recognizable stylistic tail of the distribution that KTO did not suppress.

Only the **SFT checkpoint** is published in this release; KTO weights are not included.

## Fine-tuning opportunities

The model is **not at its ceiling**. Several directions for continuation:

1. **Continued SFT** on an expanded corpus. Especially — add a corpus with factual knowledge (e.g., excerpts from Wikipedia) and code. Every ~30% of new data is worth giving ~1–2 epochs.
2. **Pre-training on raw text** (if you want to push below the 50M quality floor). 1–5 GB of Russian OSCAR/CulturaX before SFT may give a significant boost.
3. **Distillation from an external large model**. The current dataset is already a distill, but generating new responses from Claude / GPT-4o-mini / Yandex YandexGPT on the same prompts will give style diversity.
4. **Preference learning** (DPO/KTO) with **external** rejected (not self-generated). For example, low-score responses from the val split of the same dataset.
5. **Scale up** to 100–200M params with the same hyperparameters and the same corpus. Strongly non-linear quality boost.

## Release files

| File | Size | Description |
| --- | --- | --- |
| `ckpt.pt` | 553 MB | nanoGPT checkpoint (model + optimizer state + config) |
| `tokenizer.model` | 930 KB | SentencePiece tokenizer (BPE 32k) |
| `meta.pkl` | <1 KB | special token IDs + vocab_size |
| `nanogpt-chat.exe` (opt.) | 97 MB | Go single-binary with embedded model |
| `model_card.md` | this file | |

If you only want inference — `tokenizer.model` + `ckpt.pt` is sufficient.

## Citation / acknowledgments

```bibtex
@misc{mini-tron-50,
  title  = {mini-tron-50: 50M Russian chat model trained from scratch},
  author = {Impi},
  year   = {2026},
  note   = {Educational baseline; nanoGPT architecture}
}
```

Resources used:

- [nanoGPT](https://github.com/karpathy/nanoGPT) by Andrej Karpathy — foundation of architecture and training loop
- `big-russian-dataset` — training corpus

## License

Apache 2.0 — for code and weights of this model.

## Russian


50M-параметровая GPT-2-style языковая модель, обученная с нуля на русском
SFT-корпусе как чат-бот. Иллюстрирует **что можно
выжать из модели такого размера** без претрейна на сыром тексте.

Git-source - https://codeberg.org/imperius/mini-tron-50

## TL;DR

- **Architecture**: 10 layer × 8 head × 512 emb (GPT-2 style), 47.85M params
- **Trained from scratch**: SFT на ~1 ГБ chat-данных (1.7M диалогов), 1 эпоха
- **Hardware**: 1× RTX 3050 Laptop (4 ГБ VRAM), 13 часов
- **Tokenizer**: SentencePiece BPE, 32k vocab, custom-trained на корпусе
- **Format**: ChatML с спецтокенами `<|system|>`, `<|user|>`, `<|assistant|>`,
  `<|endoftext|>`
- **Loss masking**: только на assistant-токенах (стандартный SFT-trick)
- **Status**: SFT-фаза успешна; KTO-фаза проведена и провалилась (см. ниже)

Модель **не достигла своего потолка** — это одна из её особенностей. Она
тренировалась ровно одну эпоху по корпусу (Chinchilla-оптимум для 50M), и
контурные кривые показывают что улучшения val_loss ещё не выходили на плато.
Дальнейшая тренировка или продолжение на новых данных вероятно даст ощутимое
улучшение.

## Архитектура

```text
GPTConfig(
    n_layer    = 10,
    n_head     = 8,
    n_embd     = 512,
    block_size = 1024,
    vocab_size = 32000,
    bias       = False,
    dropout    = 0.1,
)
```

Стандартный GPT-2 без bias. Tied embeddings (`transformer.wte` shared с `lm_head`).
Attention использует `F.scaled_dot_product_attention` (flash-attn под капотом
на Ampere+).

## Что модель умеет

| Способность | Качество |
| --- | --- |
| Грамматика русского | ✅ безупречно (падежи, согласования, синтаксис) |
| Chat-формат (отвечает в роли ассистента) | ✅ устойчиво |
| Markdown-структура (списки, **bold**, заголовки) | ✅ имитирует GPT-4-стиль |
| Самоидентификация ("я ИИ-ассистент") | ✅ говорит правильные слова |
| Завершение по EOS | ✅ обычно сама останавливается |
| Локальная связность 1-2 предложения | ⚠️ местами осмысленно |
| Ответ строго по теме промпта | ⚠️ слышит триггерные слова, не суть |
| Факты и точные знания | ❌ галлюцинации |
| Арифметика | ❌ имитирует подсчёт без него |
| Многошаговый reasoning | ❌ |
| Code (синтаксис + семантика) | ❌ форма правильная, не работает |

## Известные failure modes

1. **Canned-ответы** на простые вопросы:
   ```
   you> Любишь котов или собак?
   bot> Привет! Я рад, что смог помочь вам сегодня. Если у вас есть вопросы,
        не стесняйтесь обращаться к нам. Удачи!
   ```
   Заученный шаблонный хвост ChatGPT-style ответов.

2. **Tutorial-простыни** на любой открытый промпт:
   ```
   you> Расскажи о себе
   bot> ### Шаг 1: Определение задачи
        ### Шаг 2: ...
        ### Заключение
   ```

3. **Token-loops** на промптах вне распределения:
   ```
   you> Что больше: 17 или 71?
   bot> Чтобы посчитать... + 112 - 112 + 112 + 112 - 112 + 112 ... [50+ повторов]
   ```

4. **Семантическая каша** в полностью грамотной обёртке:
   ```
   you> Сколько будет 7 умножить на 8?
   bot> 5! = (5 × 8) / 8 = 120. Теперь разделим 120 на 8...
        Итак, всего будет 140 способов выбрать 7 умножить на 8.
   ```
   Модель имитирует жанр школьной арифметики, не выполняя саму операцию.

Эти failure modes лечатся не SFT, а preference learning'ом + увеличением
размера модели.

## Тренировочные данные

**Источник**: `big-russian-dataset` (HuggingFace) — русскоязычный SFT-корпус.

| Сплит | Диалогов | После фильтра |
| --- | --- | --- |
| train | 1.71M | 1,709,621 (99.9%) |
| val | 18.5k | 10,396 (56%) |

**Фильтр**: `overall_score ≥ 6 AND safety ≥ 8 AND pii_leak = 0`.

В train авторы датасета сами уже почистили мусор — там нет записей со
score < 6, поэтому фильтр пропускает почти всё. В val разброс score 1-10
оставлен специально для оценки на трудных примерах.

**Объём в токенах**: ~1.04 ГБ токенов в train.bin, из них ~603M токенов под
loss (assistant + EOT, 57.7%).

## Тренировочные параметры

```python
# AdamW
learning_rate = 3e-4   # cosine decay → min_lr=3e-5
weight_decay  = 0.1
beta1, beta2  = 0.9, 0.95
grad_clip     = 1.0

# Schedule
warmup_iters  = 200
max_iters     = 16000   # ~1 эпоха
lr_decay_iters = 16000

# Batch
batch_size                  = 2
gradient_accumulation_steps = 32   # effective batch = 64 sequences
block_size                  = 1024
# tokens per iter = 65,536

# System
dtype   = 'bfloat16'
compile = False
```

## Кривая обучения

```text
iter     0  loss 10.49   (≈ ln(32000), стартовая случайная инициализация)
iter   500  loss ~5      (warmup закончен, LR на peak)
iter  5500  loss ~2.4    (первый saved checkpoint)
iter 11500  loss ~1.7    (третий)
iter 14500  loss ~1.5    (best val_loss ~ 1.8)
iter 16000  loss ~1.45   (max_iters достигнут)
```

train-val gap к концу ~1.7 nats — здоровое значение для SFT на small model.

## Как использовать

Модель распространяется в формате nanoGPT (Karpathy). **Не совместима напрямую
с `transformers.AutoModelForCausalLM`** без конвертации (имена весов отличаются от
GPT-2-стандарта, в частности нет bias).

### Вариант 1 — через nanoGPT-репозиторий (Python)

```bash
git clone https://github.com/karpathy/nanoGPT.git
cd nanoGPT
# скопировать ckpt.pt, tokenizer.model, meta.pkl сюда
python chat.py --out_dir=<path-to-checkpoint-dir>
```

`chat.py` из этого релиза предоставляет интерактивный REPL с командами для
изменения temperature, top_p, top_k, repetition_penalty на лету.

### Вариант 2 — через готовый Go single-binary

В этом релизе есть pre-built `nanogpt-chat.exe` (~97 МБ) — single-binary с
встроенными весами, токенайзером, конфигом. Запускается без Python и без
GPU. Performance: ~36 ток/сек на 4-ядерном CPU.

```bash
./nanogpt-chat.exe
```

Команды REPL:

```text
/help               справка
/show               текущие параметры
/reset              сбросить историю диалога
/system <текст>     сменить system-prompt
/temp <float>       temperature (>0)
/top_p <float>      nucleus sampling
/top_k <int>        top-k
/rep <float>        repetition_penalty
/preset <name>      creative | balanced | precise
/quit               выход
```

Все команды имеют однобуквенные алиасы (/h, /s, /r, /q, /t, /p, /k, ...).

### Вариант 3 — конвертация в HuggingFace transformers

Не предусмотрена в релизе. Требует переименования весов под GPT-2 conventions,
добавления nullевых bias, и сборки `GPT2LMHeadModel` с custom tokenizer
(SentencePiece, не GPT-2 BPE). Если кто-то напишет конвертер — буду рад PR.

## Примеры

```text
you> Привет
bot> Привет! Я готов помочь вам в достижении ваших целей. Хорошего дня!

you> Объясни простыми словами, что такое черная дыра.
bot> Для начала, давайте разберемся с этим вопросом шаг за шагом.

  ### Шаг 1: Изучение черной дыры
  - Это означает, что черная дыра является частью черной дыры.
  - Она может иметь разные размеры...
  [грамотно, но содержательно бредово -- это потолок 50M на фактах]

you> Напиши сортировку пузырьком на Python.
bot> Вот пример сортировки пузырьком на Python:
  ```python
  def merge_sort(arr):
      """Выполняет сортировку пузырьком в отсортированном порядке."""
      sorted_array = {}
      for i in range(len(arr)):
          if arr[i] < sorted_array[i - 1]:
              return merge_sort(arr[i], reverse=True)
      return sorted_array
  ```
  [имя функции merge_sort вместо bubble_sort, словарь вместо двух циклов --
  форма правильная, реализация бессмысленная]
```

Хорошие промпты для этой модели — короткие, диалоговые, не требующие точных
фактов:

```text
you> Привет, как дела?
you> Меня зовут Лёша. А тебя?
you> Назови три фрукта.
you> Расскажи короткую сказку.
```

## Ограничения

- **Знания**: модель **не** содержит достоверных фактов. Не стоит спрашивать о
  датах, именах, числах, географии, биологии, медицине. Любой ответ —
  имитация жанра справки, а не реальная информация.
- **Reasoning**: многошаговая логика недоступна. Арифметика — имитируется
  без выполнения. Code — синтаксически правдоподобен, но не работает.
- **Длина**: модель тренировалась с `block_size=1024`. Длинные диалоги
  (>800 токенов в истории) обрезаются с начала — модель «забывает» ранние
  реплики.
- **Языки**: только русский. На английских промптах попытается отвечать,
  но качество хуже.
- **Безопасность**: модель тренировалась только на отфильтрованной части
  датасета (`safety ≥ 8`), но не имеет специального alignment — на
  откровенно вредных промптах поведение не гарантировано.

## Что не получилось

После SFT была попытка preference-learning'а через **KTO** для подавления
известных failure modes. Обе попытки (β=0.1 и β=0.03) дали полностью
разрушенную модель — связные ответы превратились в семантический мусор.
Подробный root-cause анализ — в `04_kto_attempts.md` сопровождающего отчёта.

Кратко: комбинация (a) бага в реализации loss (отсутствие `clamp(z_ref, 0)`)
и (b) asymmetric difficulty между chosen-данными и self-generated rejected.
После исправления бага деградация всё равно осталась, просто медленнее.

Любопытный side-effect: после KTO модель уходила не просто в шум, а в
«афористически-философский» регистр — узнаваемый стилистический хвост
распределения, который KTO не давила.

В этом релизе публикуется **только SFT-чекпоинт**, KTO-веса не включены.

## Возможности дообучения

Модель **не на потолке**. Несколько направлений для продолжения:

1. **Continued SFT** на расширенном корпусе. Особенно — добавить корпус с
   фактическими знаниями (например, выжимки из Википедии) и кодом. Каждые
   ~30% новых данных стоит давать ~1-2 эпохи.
2. **Pre-training на сыром тексте** (если хочется уйти ниже 50M-потолка
   качества). 1-5 ГБ русского OSCAR/CulturaX перед SFT может дать
   значительный буст.
3. **Distillation от внешней большой модели**. Текущий датасет уже дистилл,
   но генерация новых ответов от Claude / GPT-4o-mini / Yandex YandexGPT
   на тех же промптах даст разнообразие стилей.
4. **Preference learning** (DPO/KTO) с **внешними** rejected (не
   self-generated). Например, low-score ответы из val того же датасета.
5. **Scale up** до 100-200M params с теми же гиперпараметрами и тем же
   корпусом. Сильно нелинейный буст качества.

## Файлы релиза

| Файл | Размер | Описание |
| --- | --- | --- |
| `ckpt.pt` | 553 МБ | nanoGPT-checkpoint (модель + optimizer state + config) |
| `tokenizer.model` | 930 КБ | SentencePiece-токенайзер (BPE 32k) |
| `meta.pkl` | <1 КБ | спецтокены ID + vocab_size |
| `nanogpt-chat.exe` (опц.) | 97 МБ | Go single-binary с встроенной моделью |
| `model_card.md` | этот файл | |

Если хочется только inference — `tokenizer.model` + `ckpt.pt` достаточно.

## Citation / благодарности

```bibtex
@misc{mini-tron-50,
  title  = {mini-tron-50: 50M Russian chat model trained from scratch},
  author = {Impi},
  year   = {2026},
  note   = {Educational baseline; nanoGPT architecture}
}
```

Использованные ресурсы:

- [nanoGPT](https://github.com/karpathy/nanoGPT) by Andrej Karpathy — основа
  архитектуры и тренировочного цикла
- `big-russian-dataset` — обучающий корпус 

## Лицензия

Apache 2.0 — на код и веса этой модели. 

