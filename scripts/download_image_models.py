#!/usr/bin/env python3
"""
ARGOS Image Generator - Установщик моделей
Скачивает все настроенные модели из Hugging Face
"""

import os
import sys
import requests
from pathlib import Path

# Модели для ARGOS Image Generation
# ВАЖНО: Многие FLUX модели требуют подтверждения лицензии на Hugging Face
# Перед скачиванием необходимо:
# 1. Иметь аккаунт на Hugging Face
# 2. Принять лицензионное соглашение на странице модели
# 3. Сгенерировать токен с правами read

MODELS_CONFIG = {
    "flux1-dev": {
        "name": "FLUX.1-dev (оригинал)",
        "repo": "black-forest-labs/FLUX.1-dev",
        "files": ["flux1-dev.safetensors"],
        "size": "~23GB",
        "description": "Оригинальная FLUX.1-dev от Black Forest Labs",
        "license_required": True,
        "note": "Требует принятия лицензии на сайте Hugging Face"
    },
    "flux-schnell": {
        "name": "FLUX.1-schnell",
        "repo": "black-forest-labs/FLUX.1-schnell",
        "files": ["flux1-schnell.safetensors"],
        "size": "~23GB",
        "description": "Ускоренная версия FLUX.1 (4 шага)",
        "license_required": True,
        "note": "Требует принятия лицензии на сайте Hugging Face"
    }
}

def get_hf_token():
    """Получить HF токен из переменных окружения"""
    for var in ["HF_TOKEN", "HUGGINGFACE_TOKEN", "HUGGINGFACE_TOKEN0"]:
        token = os.getenv(var)
        if token:
            return token
    return None

def list_repo_files(repo: str, token: str = None):
    """Получить список файлов в репозитории"""
    url = f"https://huggingface.co/api/models/{repo}/tree/main"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            files = response.json()
            return [f['path'] for f in files if f['type'] == 'file']
        elif response.status_code == 401:
            print(f"  ❌ Требуется авторизация для {repo}")
            print(f"     Убедитесь, что вы приняли лицензию на https://huggingface.co/{repo}")
            return None
        elif response.status_code == 403:
            print(f"  ❌ Доступ запрещен к {repo}")
            print(f"     Возможно, требуется подтверждение лицензии")
            return None
        else:
            print(f"  ❌ Ошибка {response.status_code} для {repo}")
            return None
    except Exception as e:
        print(f"  ❌ Ошибка подключения: {e}")
        return None

def download_file(repo: str, filename: str, dest_dir: str, token: str = None):
    """Скачать файл с Hugging Face"""
    url = f"https://huggingface.co/{repo}/resolve/main/{filename}"
    dest_path = os.path.join(dest_dir, filename)
    
    if os.path.exists(dest_path):
        print(f"  ⚠️  {filename} уже существует")
        return True
    
    print(f"  📥 Скачивание {filename}...")
    
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        os.makedirs(dest_dir, exist_ok=True)
        
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r  Прогресс: {percent:.1f}%", end='', flush=True)
        
        print(f"\n  ✅ {filename} скачан!")
        return True
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print(f"\n  ❌ Ошибка авторизации. Проверьте токен и лицензию.")
        elif e.response.status_code == 403:
            print(f"\n  ❌ Доступ запрещен. Возможно, нужно принять лицензию на сайте.")
        else:
            print(f"\n  ❌ HTTP ошибка: {e}")
        if os.path.exists(dest_path):
            os.remove(dest_path)
        return False
    except Exception as e:
        print(f"\n  ❌ Ошибка: {e}")
        if os.path.exists(dest_path):
            os.remove(dest_path)
        return False

def main():
    print("=" * 60)
    print("ARGOS Image Generator - Установщик моделей")
    print("=" * 60)
    print()
    
    token = get_hf_token()
    if token:
        print(f"✅ HF токен найден: {token[:10]}...")
    else:
        print("⚠️  HF токен не найден!")
        print("Установите переменную окружения HF_TOKEN")
        print("Некоторые модели могут быть недоступны без токена")
        print()
    
    print("ДОСТУПНЫЕ МОДЕЛИ:")
    print("-" * 60)
    for i, (key, model) in enumerate(MODELS_CONFIG.items(), 1):
        print(f"  {i}. {model['name']}")
        print(f"     Репозиторий: {model['repo']}")
        print(f"     Размер: {model['size']}")
        print(f"     {model['description']}")
        if model.get('license_required'):
            print(f"     ⚠️  {model['note']}")
        print()
    
    print("-" * 60)
    print()
    print("ИНСТРУКЦИЯ:")
    print("1. Перейдите на страницу модели на Hugging Face")
    print("2. Примите лицензионное соглашение (если требуется)")
    print("3. Сгенерируйте токен доступа (Settings -> Access Tokens)")
    print("4. Установите токен: setx HF_TOKEN ваш_токен")
    print()
    
    dest_dir = "F:/ROCm/models"
    print(f"Директория загрузки: {dest_dir}")
    print()
    
    # Показываем доступные модели в репозиториях
    print("ПРОВЕРКА ДОСТУПНЫХ ФАЙЛОВ...")
    for key, model in MODELS_CONFIG.items():
        print(f"\n📦 {model['name']}:")
        files = list_repo_files(model['repo'], token)
        if files:
            safetensors = [f for f in files if f.endswith('.safetensors') or f.endswith('.gguf')]
            if safetensors:
                print(f"  Найдены файлы:")
                for f in safetensors[:5]:  # Показываем первые 5
                    print(f"    - {f}")
            else:
                print(f"  ⚠️  Файлы .safetensors/.gguf не найдены")
        else:
            print(f"  ❌ Не удалось получить список файлов")
    
    print("\n" + "=" * 60)
    print("Для скачивания конкретной модели используйте:")
    print("  python scripts/download_image_models.py <номер>")
    print("=" * 60)

if __name__ == "__main__":
    main()
