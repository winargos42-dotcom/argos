# Проверка HF Token — Чеклист (Автоматический)

Дата: 2026-05-05
Статус: ✅ Токен рабочий
Токен: `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` (Fine-Grained, создан 2026-05-04)

---

## ⚡ Быстрая проверка (копируй в PowerShell)

```powershell
# Проверка через доступ к приватному датасету (Fine-Grained токен)
$token = "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"
Invoke-RestMethod -Uri "https://huggingface.co/api/datasets/AvaSiG/argos-dataset" `
  -Method GET -Headers @{"Authorization"="Bearer $token"} -TimeoutSec 15

# Если видишь детали датасета — токен РАБОТАЕТ ✅
# Если ошибка — токен протух, создавай новый: https://huggingface.co/settings/tokens
```

---

## ❗ Важно: Fine-Grained vs Read

| Тип токена | `/api/whoami` | Доступ к датасетам | Inference API |
|-----------|---------------|-------------------|---------------|
| **Read** | ✅ Работает | ✅ Да | ✅ Да |
| **Fine-Grained** | ❌ Не работает | ✅ Да | ✅ Да |
| **Write** | ✅ Работает | ✅ Да | ✅ Да |

**Вывод:** Fine-Grained токены не работают с `whoami`, но отлично работают с датасетами. Проверяй через датасет!

---

## 🔄 Что делать если токен не работает

1. Открыть https://huggingface.co/settings/tokens
2. Проверить статус токена:
   - Если `Inactive` — нажать **Activate**
   - Если `Expired` — создать новый
3. Создать новый токен:
   - Тип: **Fine-Grained**
   - Права: ✅ Repositories (read), ✅ Datasets (read/write)
   - Скопировать токен (начинается с `hf_`)
4. Обновить `.env`:
   ```env
   HF_TOKEN=hf_ваш_новый_токен
   HUGGINGFACE_TOKEN=hf_ваш_новый_токен
   ```

---

## 📍 Где используется

- **ARGOS .env:** `F:\debug\argoss\.env` (строки 429-433)
- **Colab Secrets:** `HF_TOKEN = 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`
- **Obsidian Mirror:** `05 SharedMemory Mirror/claude/project_argos_training__shared.md`

---

## ✅ Результат проверки 2026-05-05

```json
{
  "token": "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",
  "type": "Fine-Grained",
  "created": "2026-05-04",
  "whoami": "N/A (Fine-Grained limitation)",
  "dataset_access": "✅ OK (AvaSiG/argos-dataset)",
  "status": "ACTIVE",
  "env_updated": "2026-05-05 03:45"
}
```

---

## Ссылки

- HF Tokens: https://huggingface.co/settings/tokens
- ARGOS Dataset: https://huggingface.co/datasets/AvaSiG/argos-dataset
- Colab Notebook: `colab/ARGOS_Train_Colab.ipynb`

---

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Human Sessions Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Human Sessions Hub]]
