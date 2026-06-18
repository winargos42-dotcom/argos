#!/usr/bin/env python3
"""
ARGOS V100 Fine-tuning — локальное обучение на Tesla V100-SXM2-16GB.

Модель:  Qwen/Qwen2.5-7B-Instruct (7B, входит в 16GB с QLoRA)
Данные:  AvaSiG/argos-dataset (+ опционально ru-thinking-reasoning)
Метод:   QLoRA (4-bit) + LoRA адаптеры
Вывод:   I:/argos-training/argos-qwen2.5-7b-v1
         + push to HF: AvaSiG/argos-qwen2.5-7b-v1

GPU:  Tesla V100-SXM2-16GB  (CUDA 12.x)
HF:   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
"""
import os, sys, json, time
from pathlib import Path
from datetime import datetime

# Monkey-patch: torch 2.4 не имеет set_submodule (добавлен в 2.5)
try:
    import torch.nn
    if not hasattr(torch.nn.Module, 'set_submodule'):
        def _set_submodule(self, target, module):
            parts = target.split('.')
            parent = self
            for p in parts[:-1]:
                parent = getattr(parent, p)
            setattr(parent, parts[-1], module)
        torch.nn.Module.set_submodule = _set_submodule
except Exception:
    pass

# ── Config ────────────────────────────────────────────
HF_TOKEN    = "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"
BASE_MODEL  = "Qwen/Qwen2.5-7B-Instruct"
OUTPUT_DIR  = "I:/argos-training/argos-qwen2.5-7b-v1"
HF_REPO_ID  = "AvaSiG/argos-qwen2.5-7b-v1"
DATA_DIR    = "I:/argos-datasets"

DATASETS = [
    ("AvaSiG/argos-dataset",              "train"),   # основной датасет ARGOS
]

# LoRA параметры
LORA_R      = 16
LORA_ALPHA  = 32
LORA_DROP   = 0.05
TARGET_MODS = ["q_proj", "k_proj", "v_proj", "o_proj",
                "gate_proj", "up_proj", "down_proj"]

# Обучение
MAX_SEQ_LEN  = 1024
BATCH_SIZE   = 1         # QLoRA на 16GB — OOM защита
GRAD_ACCUM   = 16        # эффективный batch=16
EPOCHS       = 3
LR           = 2e-4
WARMUP_RATIO = 0.03
MAX_STEPS    = -1        # -1 = все эпохи

# ── Setup ─────────────────────────────────────────────
os.environ["HF_TOKEN"] = HF_TOKEN
os.environ["HUGGINGFACE_HUB_TOKEN"] = HF_TOKEN
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def check_gpu():
    import torch
    if not torch.cuda.is_available():
        log("CUDA недоступна! Проверьте PyTorch CUDA установку.")
        sys.exit(1)
    gpu_name = torch.cuda.get_device_name(0)
    mem_total = torch.cuda.get_device_properties(0).total_memory / 1e9
    log(f"GPU: {gpu_name} ({mem_total:.1f}GB)")
    return gpu_name

def load_dataset_combined():
    from datasets import load_dataset, concatenate_datasets
    import os

    os.makedirs(DATA_DIR, exist_ok=True)
    splits = []

    for ds_name, split_name in DATASETS:
        try:
            log(f"Загрузка датасета: {ds_name}")
            ds = load_dataset(ds_name, split=split_name,
                              token=HF_TOKEN,
                              cache_dir=DATA_DIR)
            log(f"  {ds_name}: {len(ds)} примеров, колонки: {ds.column_names}")
            splits.append(ds)
        except Exception as e:
            log(f"  Пропускаем {ds_name}: {e}")

    if not splits:
        log("Ни один датасет не загружен!")
        sys.exit(1)

    combined = concatenate_datasets(splits) if len(splits) > 1 else splits[0]
    log(f"Итого: {len(combined)} примеров")
    return combined

def format_example(ex):
    """Унифицированный формат чата для Qwen2.5."""
    # Пробуем разные форматы колонок
    if "instruction" in ex and "output" in ex:
        instruction = ex.get("instruction", "")
        input_text  = ex.get("input", "")
        output      = ex.get("output", "")
        if input_text:
            user_msg = f"{instruction}\n\n{input_text}"
        else:
            user_msg = instruction
        return {
            "text": f"<|im_start|>system\nТы ARGOS — самовоспроизводящаяся AI-система.<|im_end|>\n"
                    f"<|im_start|>user\n{user_msg}<|im_end|>\n"
                    f"<|im_start|>assistant\n{output}<|im_end|>"
        }
    elif "prompt" in ex and "completion" in ex:
        return {
            "text": f"<|im_start|>user\n{ex['prompt']}<|im_end|>\n"
                    f"<|im_start|>assistant\n{ex['completion']}<|im_end|>"
        }
    elif "text" in ex:
        return {"text": ex["text"]}
    elif "content" in ex:
        return {"text": ex["content"]}
    else:
        cols = {k: str(v)[:200] for k, v in ex.items() if v}
        return {"text": " ".join(cols.values())}

def main():
    log("=" * 60)
    log("ARGOS V100 Training — Qwen2.5-7B QLoRA")
    log("=" * 60)

    check_gpu()

    import torch
    from transformers import (
        AutoModelForCausalLM, AutoTokenizer,
        TrainingArguments, BitsAndBytesConfig
    )
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from trl import SFTTrainer, SFTConfig
    from huggingface_hub import login

    login(token=HF_TOKEN, add_to_git_credential=False)

    # ── Quantization config (4-bit QLoRA) ─────────────
    log("Настройка 4-bit квантизации...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    # ── Tokenizer ─────────────────────────────────────
    log(f"Загрузка токенизатора: {BASE_MODEL}")
    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL, token=HF_TOKEN, trust_remote_code=True
    )
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # ── Model ─────────────────────────────────────────
    log(f"Загрузка модели: {BASE_MODEL} (4-bit)")
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=bnb_config,
        device_map="auto",
        token=HF_TOKEN,
        trust_remote_code=True,
        torch_dtype=torch.bfloat16,
    )
    model = prepare_model_for_kbit_training(model)

    # ── LoRA ──────────────────────────────────────────
    log("Применяем LoRA адаптеры...")
    lora_config = LoraConfig(
        r=LORA_R,
        lora_alpha=LORA_ALPHA,
        target_modules=TARGET_MODS,
        lora_dropout=LORA_DROP,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # ── Dataset ───────────────────────────────────────
    dataset = load_dataset_combined()
    dataset = dataset.map(format_example, remove_columns=dataset.column_names,
                          desc="Форматирование")
    dataset = dataset.filter(lambda x: len(x["text"]) > 50 and len(x["text"]) < 8000)
    log(f"Датасет после фильтрации: {len(dataset)} примеров")

    # Разбивка train/eval
    split = dataset.train_test_split(test_size=0.05, seed=42)
    train_ds = split["train"]
    eval_ds  = split["test"]
    log(f"Train: {len(train_ds)}, Eval: {len(eval_ds)}")

    # ── Training args ─────────────────────────────────
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    training_args = SFTConfig(
        output_dir=OUTPUT_DIR,
        num_train_epochs=EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRAD_ACCUM,
        gradient_checkpointing=True,
        optim="paged_adamw_8bit",
        learning_rate=LR,
        bf16=True,
        max_grad_norm=0.3,
        warmup_ratio=WARMUP_RATIO,
        lr_scheduler_type="cosine",
        logging_steps=10,
        eval_steps=100,
        save_steps=200,
        save_total_limit=3,
        eval_strategy="steps",
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        report_to="none",
        max_length=MAX_SEQ_LEN,
        dataset_text_field="text",
        packing=True,
        push_to_hub=True,
        hub_model_id=HF_REPO_ID,
        hub_token=HF_TOKEN,
        hub_strategy="checkpoint",
    )

    # ── Trainer ───────────────────────────────────────
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        processing_class=tokenizer,
    )

    log("START: ОБУЧЕНИЕ НАЧАЛОСЬ!")
    log(f"  Модель: {BASE_MODEL}")
    log(f"  Датасет: {len(train_ds)} примеров")
    log(f"  Epochs: {EPOCHS}, LR: {LR}")
    log(f"  Вывод: {OUTPUT_DIR}")
    log(f"  HF Push: {HF_REPO_ID}")

    trainer.train()

    log("OK: Обучение завершено. Сохраняем...")
    trainer.model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    log("PUSH: Push to HuggingFace Hub...")
    trainer.push_to_hub()

    log(f"✓ Готово! Модель: https://huggingface.co/{HF_REPO_ID}")

if __name__ == "__main__":
    main()
