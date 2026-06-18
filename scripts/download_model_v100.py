#!/usr/bin/env python3
"""
ARGOS — загрузка модели для V100 на ПК (запускать ПОКА ЕСТЬ интернет)
=====================================================================
Скачивает GGUF-модель с HuggingFace в локальную папку и готовит Ollama
Modelfile, чтобы потом ARGOS работал на V100 16GB ПОЛНОСТЬЮ ОФФЛАЙН.

Запуск на ПК (Орион), пока интернет жив:
    python scripts/download_model_v100.py
    python scripts/download_model_v100.py --repo AvaSiG/argos-mistral-nemo-12b-v100 --quant Q5_K_M
    python scripts/download_model_v100.py --no-ollama        # только скачать, без ollama create

После этого интернет можно отключать — модель лежит локально, Ollama её видит.

Устойчив к плавающей сети: huggingface_hub докачивает (resume) прерванные файлы.
Токен берётся из --token, env HF_TOKEN/HUGGINGFACE_TOKEN или .env проекта.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

DEFAULT_REPO = "AvaSiG/argos-mistral-nemo-12b-v100"
FALLBACK_REPO = "AvaSiG/argos-v1-gguf"
# порядок предпочтения квантовок для V100 16GB (баланс качество/память)
QUANT_PREFERENCE = ["Q5_K_M", "Q4_K_M", "Q5_K_S", "Q4_K_S", "Q6_K", "Q8_0"]


def read_token(cli_token: str | None) -> str | None:
    if cli_token:
        return cli_token
    for var in ("HF_TOKEN", "HUGGINGFACE_TOKEN"):
        if os.environ.get(var):
            return os.environ[var]
    # .env проекта
    for env_path in (Path(__file__).resolve().parent.parent / ".env", Path.cwd() / ".env"):
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
                if line.startswith("HF_TOKEN="):
                    return line.split("=", 1)[1].strip()
    return None


def pick_gguf(files: list[str], quant: str | None) -> str | None:
    ggufs = [f for f in files if f.lower().endswith(".gguf")]
    if not ggufs:
        return None
    if quant:  # явный выбор
        for f in ggufs:
            if quant.lower() in f.lower():
                return f
        print(f"  ⚠ квантовка {quant} не найдена, выбираю по предпочтению")
    for q in QUANT_PREFERENCE:
        for f in ggufs:
            if q.lower() in f.lower():
                return f
    return ggufs[0]  # хоть что-то


def download_with_retry(repo, filename, local_dir, token, tries=8):
    from huggingface_hub import hf_hub_download
    for i in range(1, tries + 1):
        try:
            path = hf_hub_download(repo_id=repo, filename=filename, local_dir=local_dir,
                                   token=token, resume_download=True)
            return path
        except Exception as e:
            print(f"  попытка {i}/{tries} не удалась: {str(e)[:120]}")
            time.sleep(min(5 * i, 30))
    return None


def make_modelfile(gguf_path: Path, model_dir: Path) -> Path:
    system = ("Ты — АРГОС (Argos Universal OS), автономная AI-система Всеволода. "
              "Отвечай по-русски, по делу. Выполняй задачи, а не описывай их.")
    content = (
        f"FROM {gguf_path.name}\n\n"
        'TEMPLATE """{{ if .System }}<|im_start|>system\n{{ .System }}<|im_end|>\n{{ end }}'
        '{{ if .Prompt }}<|im_start|>user\n{{ .Prompt }}<|im_end|>\n{{ end }}'
        '<|im_start|>assistant\n{{ .Response }}<|im_end|>\n"""\n\n'
        f'SYSTEM """{system}"""\n\n'
        "PARAMETER temperature 0.7\n"
        "PARAMETER num_ctx 8192\n"
        "PARAMETER stop <|im_end|>\n"
    )
    mf = model_dir / "Modelfile"
    mf.write_text(content, encoding="utf-8")
    return mf


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=DEFAULT_REPO)
    ap.add_argument("--quant", default=None, help="напр. Q5_K_M; иначе авто по предпочтению")
    ap.add_argument("--out", default=str(Path.home() / "argos-models"))
    ap.add_argument("--ollama-name", default="argos-v2")
    ap.add_argument("--no-ollama", action="store_true", help="только скачать, без ollama create")
    ap.add_argument("--token", default=None)
    args = ap.parse_args()

    token = read_token(args.token)
    print(f"токен HF: {'есть ('+token[:8]+'…)' if token else 'НЕТ — приватные репо недоступны'}")

    try:
        from huggingface_hub import HfApi
    except ImportError:
        print("❌ нет huggingface_hub. Установи: pip install huggingface_hub")
        return 1

    api = HfApi(token=token)
    model_dir = Path(args.out)
    model_dir.mkdir(parents=True, exist_ok=True)

    # список файлов репо (с fallback)
    repo = args.repo
    try:
        files = api.list_repo_files(repo)
    except Exception as e:
        print(f"⚠ репо {repo} недоступен ({str(e)[:80]}), пробую {FALLBACK_REPO}")
        repo = FALLBACK_REPO
        try:
            files = api.list_repo_files(repo)
        except Exception as e2:
            print(f"❌ оба репо недоступны: {str(e2)[:80]}")
            return 1

    gguf = pick_gguf(files, args.quant)
    if not gguf:
        print(f"❌ в {repo} нет .gguf файлов. Файлы: {files[:10]}")
        return 1
    print(f"репо: {repo}\nвыбран GGUF: {gguf}")

    # место на диске
    free_gb = shutil.disk_usage(model_dir).free / 1e9
    print(f"свободно на диске: {free_gb:.1f} GB")
    if free_gb < 12:
        print("⚠ меньше 12 GB свободно — крупная модель может не поместиться")

    print("скачиваю (с докачкой при обрыве)…")
    path = download_with_retry(repo, gguf, str(model_dir), token)
    if not path:
        print("❌ не удалось скачать после всех попыток. Повтори позже.")
        return 1
    gguf_path = Path(path)
    print(f"✅ скачано: {gguf_path}  ({gguf_path.stat().st_size/1e9:.2f} GB)")

    mf = make_modelfile(gguf_path, gguf_path.parent)
    print(f"✅ Modelfile: {mf}")

    if args.no_ollama:
        print("\nГотово (без ollama). Оффлайн-регистрация позже:")
        print(f"  cd {gguf_path.parent} && ollama create {args.ollama_name} -f Modelfile")
        return 0

    if not shutil.which("ollama"):
        print("\n⚠ ollama не найден в PATH. Зарегистрируй вручную (оффлайн):")
        print(f"  cd {gguf_path.parent} && ollama create {args.ollama_name} -f Modelfile")
        return 0

    print(f"\nregistering в Ollama как '{args.ollama_name}'…")
    r = subprocess.run(["ollama", "create", args.ollama_name, "-f", str(mf)],
                       cwd=str(gguf_path.parent))
    if r.returncode == 0:
        print(f"✅ Готово. Оффлайн-запуск: ollama run {args.ollama_name}")
        print(f"   В .env ARGOS: OLLAMA_MODEL={args.ollama_name}")
    else:
        print("⚠ ollama create вернул ошибку — зарегистрируй вручную позже")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
