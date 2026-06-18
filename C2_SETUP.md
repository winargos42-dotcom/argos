# C2/Ghost Command Setup
Настройка командования для Argos Swarm

## Быстрый старт

### 1. Создай GitHub Gist (бесплатный C2 сервер)
1. Открой https://gist.github.com
2. Создай новый gist (можно пустой)
3. Скопируй Gist ID из URL
4. Создай GitHub Token: https://github.com/settings/tokens
   - Разрешения: gist

### 2. Настрой .env

Добавь в .env на ВСЕХ узлах:
```env
ARGOS_GIST_ID=your_gist_id
ARGOS_GITHUB_TOKEN=your_token
GHOST_C2_ENABLED=true
```

### 3. Команды Ghost

Через Telegram бота:
```
ghost status          # статус всех узлов
ghost cmd ls -la      # выполнить команду на всех узлах
ghost deploy          # деплой на все узлы
ghost backup          # бэкап со всех узлов
```

### 4. Проверка связи

```bash
curl https://api.github.com/gists/YOUR_GIST_ID
```

## Архитектура

```
[ПК] ←→ [GitHub Gist] ←→ [Azure VM]
  ↑                        ↓
[Telegram] ←────────── [Phone]
```

## Безопасность

- Все команды подписываются ключом
- Шифрование через GPG
- Fallback каналы: P2P прямое соединение
