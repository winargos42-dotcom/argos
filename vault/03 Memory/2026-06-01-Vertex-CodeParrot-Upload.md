# Vertex / GCS — CodeParrot Upload 2026-06-01

## Операция
Загрузка датасета Python-кода из HF bucket в Google Cloud Storage.

## Источник
- **HF bucket:** `AvaSiG/codeparrot-bucket`
- **Файл:** `file-000000000000.json.gz` (255 MB)
- **Описание:** ~22 млн Python-файлов из GitHub (BigQuery)

## Назначение
- **GCS bucket:** `gs://argosssss`
- **Путь:** `datasets/codeparrot/file-000000000000.json.gz`
- **Размер:** 243.22 MiB

## GCP
- **Проект:** argos-489214
- **Сервисный аккаунт:** argoss@argos-489214.iam.gserviceaccount.com
- **Ключ:** `argos-489214-782ee50ae90b.json`

## Следующие шаги
1. Загрузить оставшиеся чанки (file-000000000001+, если есть).
2. Создать Vertex AI CustomJob для fine-tuning на A100/V100.
3. Использовать `lvwerra/codeparrot-clean` для дедупликации.

---
*Сгенерировано: 2026-06-01*
