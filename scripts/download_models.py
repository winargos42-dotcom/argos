#!/usr/bin/env python3
"""
Скрипт загрузки моделей для ARGOS Image Generation
Поддерживает FLUX, Stable Diffusion и другие модели
"""

import os
import sys
import requests
from pathlib import Path
from tqdm import tqdm

# Конфигурация моделей
MODELS = {
    "flux1-dev-q8": {
        "name": "FLUX.1-dev Q8",
        "repo": "mo137/FLUX.1-dev_Q8-fp16-fp32-mix_8-to-32-bpw_gguf",
        "files": [
            "flux1-dev-q8_0.gguf",
        ],
        "local_dir": "F:/ROCm/models",
        "description": "FLUX.1-dev квантизированная модель"
    }
}

def download_file(url: str, dest_path: str, token: str = None):
    """Скачать файл с Hugging Face с прогресс-баром"""
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    print(f"Скачивание: {url}")
    print(f"Куда: {dest_path}")
    
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, 'wb') as f, tqdm(
        desc=os.path.basename(dest_path),
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))
    
    print(f"✅ Скачано: {dest_path}")

def download_model(model_key: str, hf_token: str = None):
    """Скачать модель по ключу"""
    if model_key not in MODELS:
        print(f"❌ Неизвестная модель: {model_key}")
        print(f"Доступные: {list(MODELS.keys())}")
        return False
    
    model = MODELS[model_key]
    print(f"\n📥 Загрузка модели: {model['name']}")
    print(f"Описание: {model['description']}")
    
    for filename in model['files']:
        # Формируем URL для скачивания
        url = f"https://huggingface.co/{model['repo']}/resolve/main/{filename}"
        dest = os.path.join(model['local_dir'], filename)
        
        if os.path.exists(dest):
            print(f"⚠️ Файл уже существует: {dest}")
            continue
        
        try:
            download_file(url, dest, hf_token)
        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")
            return False
    
    print(f"\n✅ Модель {model['name']} готова к использованию!")
    return True

def main():
    # Получаем токен
    hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
    
    if len(sys.argv) < 2:
        print("Использование: python download_models.py <model_key>")
        print(f"\nДоступные модели:")
        for key, model in MODELS.items():
            print(f"  {key}: {model['name']} - {model['description']}")
        print("\nПример: python download_models.py flux1-dev-q8")
        return
    
    model_key = sys.argv[1]
    
    if not hf_token:
        print("⚠️ HF_TOKEN не найден в переменных окружения")
        print("Некоторые модели могут требовать токен")
        response = input("Продолжить без токена? (y/n): ")
        if response.lower() != 'y':
            return
    
    success = download_model(model_key, hf_token)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
