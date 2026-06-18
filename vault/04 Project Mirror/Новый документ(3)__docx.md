---
argos_import: project_file
source_path: Новый документ(3).docx
source_abs: F:\debug\argoss\Новый документ(3).docx
source_ext: .docx
source_sha256: ebe75df9737af9ff71efeb672d409aea41c25ee3c5d4503277a9820e71cb8652
text_sha256: 7ae3179f5ca5650073c6b10d5734a3a21a223d221d5089c3440f93580c452b98
extract_mode: docx
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# Новый документ(3).docx

- Source: `Новый документ(3).docx`
- Extract: `docx`
- SHA256: `ebe75df9737af9ff71efeb672d409aea41c25ee3c5d4503277a9820e71cb8652`

## Content

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
grist_git_sync.py — двусторонняя синхронизация между Grist и Git.
Позволяет версионировать конфигурации, метаданные узлов и журналы.
"""
import os
import json
import csv
import io
import subprocess
import requests
from datetime import datetime
import hashlib
import time
class GristGitSync:
    """
    Синхронизирует таблицы Grist с Git-репозиторием.
    - Выгружает таблицы в CSV и коммитит их.
    - При обнаружении изменений в Git (новый коммит) обновляет Grist.
    """
    
    def __init__(self, grist_api_key, grist_doc_id, grist_server="https://docs.getgrist.com",
                 git_repo_path=".", git_branch="main", sync_interval=60):
        self.grist_api_key = grist_api_key
        self.grist_doc_id = grist_doc_id
        self.grist_server = grist_server
        self.git_repo_path = git_repo_path
        self.git_branch = git_branch
        self.sync_interval = sync_interval
        self.last_commit_hash = self._get_current_commit()
        self.running = True
        
    # ------------------------------------------------------------------
    # Grist API методы
    # ------------------------------------------------------------------
    def _grist_request(self, method, endpoint, data=None):
        """Базовый запрос к Grist API."""
        url = f"{self.grist_server}/api/docs/{self.grist_doc_id}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.grist_api_key}",
            "Content-Type": "application/json"
        }
        response = requests.request(method, url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def list_tables(self):
        """Возвращает список таблиц в документе."""
        return self._grist_request("GET", "tables")
    
    def export_table_csv(self, table_id):
        """Экспортирует таблицу в CSV (через API)."""
        # Grist API может отдавать CSV через другой endpoint
        url = f"{self.grist_server}/api/docs/{self.grist_doc_id}/tables/{table_id}/data"
        headers = {"Authorization": f"Bearer {self.grist_api_key}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        # Преобразуем JSON в CSV
        if data and 'records' in data:
            output = io.StringIO()
            writer = csv.writer(output)
            # Заголовки
            writer.writerow(data['records'][0]['fields'].keys())
            # Строки
            for record in data['records']:
                writer.writerow(record['fields'].values())
            return output.getvalue()
        return ""
    
    def import_table_csv(self, table_id, csv_content):
        """Импортирует CSV в таблицу (заменяет данные)."""
        # Grist API для загрузки данных
        url = f"{self.grist_server}/api/docs/{self.grist_doc_id}/tables/{table_id}/data"
        headers = {"Authorization": f"Bearer {self.grist_api_key}", "Content-Type": "text/csv"}
        response = requests.post(url, headers=headers, data=csv_content)
        response.raise_for_status()
        return response.json()
    
    # ------------------------------------------------------------------
    # Git методы
    # ------------------------------------------------------------------
    def _git_command(self, cmd):
        """Выполняет Git-команду в репозитории."""
        result = subprocess.run(cmd, cwd=self.git_repo_path, shell=True,
                                capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Git error: {result.stderr}")
        return result.stdout.strip()
    
    def _get_current_commit(self):
        """Возвращает хеш текущего коммита."""
        try:
            return self._git_command("git rev-parse HEAD")
        except:
            return None
    
    def commit_csvs(self, tables_data, message=None):
        """
        Сохраняет CSV-представления таблиц в файлы и коммитит их.
        tables_data: dict {table_name: csv_content}
        """
        # Создаём папку для хранения слепков, если нет
        snapshots_dir = os.path.join(self.git_repo_path, "grist_snapshots")
        os.makedirs(snapshots_dir, exist_ok=True)
        
        # Записываем CSV-файлы
        for table_name, csv_content in tables_data.items():
            file_path = os.path.join(snapshots_dir, f"{table_name}.csv")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(csv_content)
            self._git_command(f"git add {file_path}")
        
        # Коммит
        if not message:
            message = f"Grist snapshot {datetime.now().isoformat()}"
        self._git_command(f'git commit -m "{message}"')
        self.last_commit_hash = self._get_current_commit()
        print(f"Committed: {message}")
    
    def get_changed_tables(self, from_commit=None, to_commit=None):
        """
        Определяет, какие таблицы изменились между коммитами.
        Возвращает список имён таблиц.
        """
        if not from_commit:
            from_commit = self.last_commit_hash
        if not to_commit:
            to_commit = "HEAD"
        
        # Получаем список изменённых файлов в папке grist_snapshots
        diff = self._git_command(f"git diff --name-only {from_commit} {to_commit} -- grist_snapshots/")
        files = diff.split('\n')
        tables = []
        for f in files:
            if f.endswith('.csv'):
                table_name = os.path.basename(f)[:-4]
                tables.append(table_name)
        return tables
    
    def load_csv_from_git(self, table_name, commit_hash=None):
        """Загружает CSV-слепок таблицы из Git."""
        if not commit_hash:
            commit_hash = "HEAD"
        file_path = f"grist_snapshots/{table_name}.csv"
        try:
            content = self._git_command(f"git show {commit_hash}:{file_path}")
            return content
        except:
            return None
    
    # ------------------------------------------------------------------
    # Цикл синхронизации
    # ------------------------------------------------------------------
    def sync_grist_to_git(self):
        """Выгружает все таблицы из Grist в Git."""
        tables = self.list_tables()
        tables_data = {}
        for table in tables.get('tables', []):
            table_id = table['id']
            csv_content = self.export_table_csv(table_id)
            tables_data[table_id] = csv_content
        if tables_data:
            self.commit_csvs(tables_data, "Auto-sync from Grist")
    
    def sync_git_to_grist(self):
        """Если в Git есть новые коммиты, обновляет изменённые таблицы в Grist."""
        current_commit = self._get_current_commit()
        if current_commit != self.last_commit_hash:
            changed_tables = self.get_changed_tables(self.last_commit_hash, current_commit)
            for table_name in changed_tables:
                csv_content = self.load_csv_from_git(table_name, current_commit)
                if csv_content:
                    self.import_table_csv(table_name, csv_content)
                    print(f"Updated Grist table {table_name} from Git")
            self.last_commit_hash = current_commit
    
    def sync_loop(self):
        """Бесконечный цикл синхронизации (для фонового потока)."""
        while self.running:
            try:
                self.sync_grist_to_git()
                self.sync_git_to_grist()
            except Exception as e:
                print(f"Sync error: {e}")
            time.sleep(self.sync_interval)
    
    def start(self):
        import threading
        self.thread = threading.Thread(target=self.sync_loop)
        self.thread.daemon = True
        self.thread.start()
        print("Grist-Git sync started")
    
    def stop(self):
        self.running = False
# ------------------------------------------------------------------
# Пример использования
if __name__ == "__main__":
    # Параметры (в реальности берутся из .env)
    GRIST_API_KEY = os.getenv("GRIST_API_KEY", "your_key")
    GRIST_DOC_ID = os.getenv("GRIST_DOC_ID", "your_doc_id")
    
    sync = GristGitSync(GRIST_API_KEY, GRIST_DOC_ID, git_repo_path=".")
    sync.start()
    
    try:
        time.sleep(300)  # работаем 5 минут
    finally:
        sync.stop()

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
