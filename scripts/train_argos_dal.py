"""
Дообучение argos-v1 на датасете Словаря Даля + русской классики.
Запускается на ПК (GPU: RX580 4GB VRAM).
Использует QLoRA для минимального VRAM.
"""
import json, os, sys
from pathlib import Path

# Конфиг
DATASET = "argos_dal_full_dataset.jsonl"
BASE_MODEL = "unsloth/tinyllama-chat-bnb-4bit"  # Уже использовали для argos-v1
OUTPUT_DIR = "models/argos_dal_v1"
HF_REPO = "AvaSiG/argos-dataset"
HF_TOKEN = "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"

TRAIN_CONFIG = {
    "max_seq_length": 512,
    "r": 32,           # LoRA rank (меньше = быстрее)
    "lora_alpha": 64,
    "num_epochs": 1,   # 1 эпоха для быстрого результата
    "batch_size": 2,
    "learning_rate": 2e-4,
    "warmup_steps": 50,
    "save_steps": 200,
}

script = f"""
#!/usr/bin/env python3
# Дообучение argos-v1 на датасете Даля (QLoRA, 1 эпоха)
import json, os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

from datasets import Dataset
from transformers import TrainingArguments
from trl import SFTTrainer

try:
    from unsloth import FastLanguageModel
    USE_UNSLOTH = True
except:
    USE_UNSLOTH = False
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from peft import LoraConfig, get_peft_model
    import torch

print("Загружаю датасет...")
examples = []
with open(r"F:\\debug\\argoss\\data\\{DATASET}") as f:
    for line in f:
        try: examples.append(json.loads(line.strip()))
        except: pass
print(f"Датасет: {{len(examples)}} примеров")

# Форматируем в ChatML
def format_example(ex):
    msgs = ex.get("messages", [])
    text = ""
    for m in msgs:
        role = m.get("role","user")
        content = m.get("content","")
        text += f"<|im_start|>{{role}}\\n{{content}}<|im_end|>\\n"
    return {{"text": text}}

dataset = Dataset.from_list([format_example(e) for e in examples])
print(f"Отформатировано: {{len(dataset)}} примеров")

if USE_UNSLOTH:
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="{BASE_MODEL}",
        max_seq_length={TRAIN_CONFIG['max_seq_length']},
        load_in_4bit=True,
    )
    model = FastLanguageModel.get_peft_model(
        model, r={TRAIN_CONFIG['r']}, lora_alpha={TRAIN_CONFIG['lora_alpha']},
        target_modules=["q_proj","k_proj","v_proj","o_proj"],
        use_gradient_checkpointing=True,
    )
else:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from peft import LoraConfig, get_peft_model, TaskType
    
    tokenizer = AutoTokenizer.from_pretrained("{BASE_MODEL}")
    bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
    model = AutoModelForCausalLM.from_pretrained("{BASE_MODEL}", quantization_config=bnb_config, device_map="auto")
    
    lora_config = LoraConfig(r={TRAIN_CONFIG['r']}, lora_alpha={TRAIN_CONFIG['lora_alpha']}, 
        target_modules=["q_proj","k_proj","v_proj","o_proj"], task_type=TaskType.CAUSAL_LM)
    model = get_peft_model(model, lora_config)

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length={TRAIN_CONFIG['max_seq_length']},
    args=TrainingArguments(
        output_dir=r"F:\\debug\\argoss\\{OUTPUT_DIR}",
        num_train_epochs={TRAIN_CONFIG['num_epochs']},
        per_device_train_batch_size={TRAIN_CONFIG['batch_size']},
        learning_rate={TRAIN_CONFIG['learning_rate']},
        warmup_steps={TRAIN_CONFIG['warmup_steps']},
        save_steps={TRAIN_CONFIG['save_steps']},
        logging_steps=50,
        fp16=True,
        report_to="none",
    ),
)

print("Начинаю обучение...")
trainer.train()
print("Обучение завершено!")

# Сохраняем
trainer.save_model()
tokenizer.save_pretrained(r"F:\\debug\\argoss\\{OUTPUT_DIR}")
print(f"Модель сохранена в {OUTPUT_DIR}")

# Загружаем на HF
try:
    model.push_to_hub("AvaSiG/argos-dal-v1", token="{HF_TOKEN}")
    tokenizer.push_to_hub("AvaSiG/argos-dal-v1", token="{HF_TOKEN}")
    print("✅ Модель на HuggingFace: AvaSiG/argos-dal-v1")
except Exception as e:
    print(f"HF upload: {{e}}")
"""

# Сохраняем скрипт для ПК
with open("/home/ava/Projects/argoss/scripts/train_on_pc.py", "w") as f:
    f.write(script)

print("train_on_pc.py создан ✅")
