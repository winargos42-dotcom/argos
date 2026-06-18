"""
train_argos_v1.py — Fine-tune Qwen2.5-1.5B-Instruct for ARGOS AI assistant

Usage (on Orion or any CUDA machine):
    python scripts/train_argos_v1.py \
        --dataset data/datasets/train_chat.jsonl \
        --output_dir models/argos-v1-lora \
        --base_model Qwen/Qwen2.5-1.5B-Instruct

Requirements:
    pip install transformers peft trl datasets accelerate bitsandbytes

VRAM estimate (V100 16GB):
    Qwen2.5-1.5B base ~3.2GB
    LoRA r=16, alpha=32 ~200MB additional
    Activation + optimizer ~4-6GB
    Total ~8-10GB → fits comfortably on V100 16GB
"""

from __future__ import annotations

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any

# ── CLI arguments ──────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="ARGOS v1 LoRA fine-tuning")
    p.add_argument("--dataset", required=True, help="Path to .jsonl chat-format dataset")
    p.add_argument("--output_dir", default="models/argos-v1-lora", help="LoRA adapter output dir")
    p.add_argument("--base_model", default="Qwen/Qwen2.5-1.5B-Instruct", help="Base HF model")
    p.add_argument("--epochs", type=int, default=3)
    p.add_argument("--batch_size", type=int, default=4)
    p.add_argument("--lr", type=float, default=2e-4, help="Learning rate")
    p.add_argument("--lora_r", type=int, default=16)
    p.add_argument("--lora_alpha", type=int, default=32)
    p.add_argument("--lora_dropout", type=float, default=0.05)
    p.add_argument("--max_seq_length", type=int, default=512)
    p.add_argument("--warmup_steps", type=int, default=100)
    p.add_argument("--save_steps", type=int, default=500)
    p.add_argument("--logging_steps", type=int, default=50)
    p.add_argument("--bf16", action="store_true", help="Use bfloat16 (Ampere+ only, not V100)")
    p.add_argument("--fp16", action="store_true", help="Use float16 (V100 compatible)")
    p.add_argument("--gradient_checkpointing", action="store_true", default=True)
    p.add_argument("--merge_and_save", type=str, default="", help="If set, merge adapter into full model and save to this dir")
    return p.parse_args()

# ── Helpers ──────────────────────────────────────────────────────────────

def load_chat_dataset(path: str) -> List[Dict[str, Any]]:
    """Load .jsonl with OpenAI chat format {messages:[{role,content},...]}."""
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records

# ── Main ─────────────────────────────────────────────────────────────────

def main():
    args = parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Early imports (heavy libs)
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
    from peft import LoraConfig, get_peft_model, TaskType
    from trl import SFTTrainer, DataCollatorForCompletionOnlyLM
    from datasets import Dataset

    # Detect device
    if torch.cuda.is_available():
        device = "cuda"
        n_gpus = torch.cuda.device_count()
        print(f"[ARGOS-TRAIN] CUDA available: {n_gpus} GPU(s)")
        for i in range(n_gpus):
            print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
    else:
        device = "cpu"
        print("[ARGOS-TRAIN] WARNING: No CUDA — training will be extremely slow")

    # Load tokenizer & model
    print(f"[ARGOS-TRAIN] Loading base model: {args.base_model}")
    tokenizer = AutoTokenizer.from_pretrained(args.base_model, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    dtype = torch.float32
    if args.bf16 and torch.cuda.is_available() and torch.cuda.is_bf16_supported():
        dtype = torch.bfloat16
    elif args.fp16:
        dtype = torch.float16

    model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        torch_dtype=dtype,
        device_map="auto" if device == "cuda" else None,
        trust_remote_code=True,
    )

    if device == "cpu":
        model = model.to("cpu")

    # LoRA config
    lora_cfg = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )
    model = get_peft_model(model, lora_cfg)
    model.print_trainable_parameters()

    # Load dataset
    print(f"[ARGOS-TRAIN] Loading dataset from {args.dataset}")
    raw_records = load_chat_dataset(args.dataset)
    # Convert to HuggingFace Dataset with 'messages' field
    hf_dataset = Dataset.from_list(raw_records)
    # Keep only records with messages
    hf_dataset = hf_dataset.filter(lambda x: isinstance(x.get("messages"), list) and len(x["messages"]) > 0)
    print(f"[ARGOS-TRAIN] Usable samples: {len(hf_dataset)}")

    # Training arguments
    training_args = TrainingArguments(
        output_dir=str(out_dir),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=max(1, 8 // args.batch_size),  # target effective batch 8
        learning_rate=args.lr,
        warmup_steps=args.warmup_steps,
        logging_steps=args.logging_steps,
        save_steps=args.save_steps,
        save_total_limit=2,
        fp16=args.fp16 and not args.bf16,
        bf16=args.bf16,
        gradient_checkpointing=args.gradient_checkpointing,
        optim="adamw_torch",
        group_by_length=True,
        report_to="none",  # disable wandb / tensorboard unless configured
        remove_unused_columns=False,
        max_grad_norm=0.3,
        lr_scheduler_type="cosine",
    )

    # SFTTrainer with chat template applied automatically
    # TRL >=0.9 supports dataset_text_field="messages" + apply_chat_template in formatting_func
    # For broader compatibility we use a simple formatting_func
    def formatting_func(example: Dict[str, Any]) -> str:
        msgs = example.get("messages", [])
        if not msgs:
            return ""
        # Apply chat template (returns string or list of token ids depending on tokenizer)
        text = tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=False)
        return str(text)

    # Data collator that masks prompt tokens and trains only on assistant responses
    # We assume the last message is assistant; everything before is prompt.
    # For simplicity we train on full conversation; later can mask user parts.
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=hf_dataset,
        args=training_args,
        formatting_func=formatting_func,
        max_seq_length=args.max_seq_length,
        dataset_text_field=None,  # because formatting_func returns string directly
        data_collator=None,
    )

    print("[ARGOS-TRAIN] Starting training...")
    trainer.train()

    # Save adapter
    adapter_dir = out_dir / "final_adapter"
    model.save_pretrained(adapter_dir)
    tokenizer.save_pretrained(adapter_dir)
    print(f"[ARGOS-TRAIN] LoRA adapter saved to {adapter_dir}")

    # Optional: merge and save full model
    if args.merge_and_save:
        merge_dir = Path(args.merge_and_save)
        merge_dir.mkdir(parents=True, exist_ok=True)
        print(f"[ARGOS-TRAIN] Merging adapter into base model...")
        merged_model = model.merge_and_unload()
        merged_model.save_pretrained(merge_dir)
        tokenizer.save_pretrained(merge_dir)
        print(f"[ARGOS-TRAIN] Merged model saved to {merge_dir}")

    print("[ARGOS-TRAIN] Done.")


if __name__ == "__main__":
    main()
