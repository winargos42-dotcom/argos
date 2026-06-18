# ARGOS машины — аудит 2026-06-17

## Статус на 2026-06-17T11:35:05.908817+00:00

| Машина | Адрес | Статус | Роль | Сервисы |
|--------|-------|--------|------|---------|
| PC Orion | 192.168.1.72 | online | GPU inference + brain | llama-server:8082, brain:5001 |
| Laptop X230 | 192.168.1.53 | online | CLI/code gen + brain | brain:5001 |
| OrangePi | 192.168.2.168 | online (via PC registry) | IoT/reports | reports, z2m |
| Railway | argos-v2-production.up.railway.app | online | cloud proxy | /health, /brain/nodes |
| GCP Cloud Run | argos-core-m3gk27ccqa-uc.a.run.app | 500 error | gemini/openai proxy | unavailable |
| GCP VM Sentinel | 35.194.61.206 | TCP open, SSH key denied | cloud VM | 22/5001/8080/443/80 open, HTTP timeout |
| GCP VM Arcus | 34.53.142.129 | TCP open, SSH timeout | cloud VM | ports open but no response |
| GCP VM Zenith | 104.155.192.165 | TCP open, SSH timeout | cloud VM | ports open but no response |

## MCP ACP память

- `argos-memory` MCP сервер запускается из `argos_mcp_server.py` режим stdio.
- Инструменты: `knowledge_know`, `knowledge_recall`, `selfmodel_update`, `selfmodel_get`.
- Brain-режим: `brain_status`, `brain_nodes`.
- Знания сохранены в `Cromolab_Memory/knowledge/known.json`.

## GCP Vertex

- В коде есть `vertex_configs/vertex_job_nemo_codeparrot.yaml` и `vertex_training/train_nemo_codeparrot.py`.
- GCP proxy Cloud Run (`argos-core-m3gk27ccqa-uc.a.run.app`) сейчас возвращает 500/503.
- Прямые GCP VM доступны по TCP, но brain/HTTP не отвечает (возможно firewall/процессы не запущены).

## Рекомендации

1. Проверить GCP Cloud Run logs (`gcloud logging read`).
2. На GCP VM запустить brain сервис или открыть firewall для 5001.
3. Разобраться с SSH-ключами для VM (особенно 35.194.61.206 — key denied).
