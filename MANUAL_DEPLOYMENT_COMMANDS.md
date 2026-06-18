# РУЧНЫЕ КОМАНДЫ ДЛЯ РАЗВЁРТЫВАНИЯ ARGOS P2P

## ТЕКУЩЕЕ СОСТОЯНИЕ

### ✅ Australia VM (`argos-vm`, `20.53.240.36`)
- ARGOS установлен и работает
- P2P порт: 8000 (открыт)
- MCP порт: 8000 (работает)

### 🚧 Japan VM (`argos-vm-jp_27e38b15`, `40.81.208.101`)
- Создан `.env` файл
- Нужно установить ARGOS

### 🚀 Google Cloud Run
- Обновляется с P2P настройками

## КОМАНДЫ ДЛЯ ВЫПОЛНЕНИЯ

### 1. ПРОВЕРИТЬ AUSTRALIA VM
```powershell
# Проверить что ARGOS работает
az vm run-command invoke --resource-group rg-argos --name argos-vm --command-id RunShellScript --scripts "curl -s http://localhost:8000/health"

# Проверить P2P настройки
az vm run-command invoke --resource-group rg-argos --name argos-vm --command-id RunShellScript --scripts "cat /home/argos/Argos/.env | grep -i p2p"
```

### 2. УСТАНОВИТЬ ARGOS НА JAPAN VM
```powershell
# Скачать ARGOS
az vm run-command invoke --resource-group rg-argos --name argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "cd /home/ava/argoss && wget -q https://argdeploy6683.blob.core.windows.net/deploy/src.zip -O src.zip"

# Распаковать
az vm run-command invoke --resource-group rg-argos --name argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "cd /home/ava/argoss && unzip -q -o src.zip"

# Проверить файлы
az vm run-command invoke --resource-group rg-argos --name argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "cd /home/ava/argoss && ls -la && ls -la src/ 2>/dev/null || echo 'Проверь содержимое архива'"
```

### 3. ЗАПУСТИТЬ ARGOS НА JAPAN VM
```powershell
# Запустить ARGOS
az vm run-command invoke --resource-group rg-argos --name argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "cd /home/ava/argoss && nohup python3 main.py --no-gui > argos.log 2>&1 &"

# Проверить запуск
az vm run-command invoke --resource-group rg-argos --name argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "ps aux | grep python | grep -v grep"

# Проверить порт
az vm run-command invoke --resource-group rg-argos --name argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "ss -tlnp | grep 8000 || echo 'Порт 8000 не слушается'"
```

### 4. ПРОВЕРИТЬ P2P СОЕДИНЕНИЕ
```powershell
# Australia → Japan
az vm run-command invoke --resource-group rg-argos --name argos-vm --command-id RunShellScript --scripts "curl -s http://40.81.208.101:8000/health || echo 'Japan VM не отвечает'"

# Japan → Australia
az vm run-command invoke --resource-group rg-argos --name argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "curl -s http://20.53.240.36:8000/health || echo 'Australia VM не отвечает'"
```

### 5. УСТАНОВИТЬ WIREGUARD (ОПЦИОНАЛЬНО)
```powershell
# Australia VM
az vm run-command invoke --resource-group rg-argos --name argos-vm --command-id RunShellScript --scripts "sudo apt update && sudo apt install -y wireguard wireguard-tools"

# Japan VM
az vm run-command invoke --resource-group rg-argos --name argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "sudo apt update && sudo apt install -y wireguard wireguard-tools"
```

## БЫСТРАЯ ПРОВЕРКА

### Australia VM:
```powershell
az vm run-command invoke --resource-group rg-argos --name argos-vm --command-id RunShellScript --scripts "echo 'Australia VM:' && curl -s http://localhost:8000/health && echo ''"
```

### Japan VM:
```powershell
az vm run-command invoke --resource-group rg-argos --name argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "echo 'Japan VM:' && ls -la /home/ava/argoss/ 2>/dev/null || echo 'ARGOS не установлен'"
```

## ЕСЛИ КОМАНДЫ ЗАВИСАЮТ

1. **Подожди 1-2 минуты** между командами
2. **Используй `timeout`** в скриптах
3. **Проверь статус VM** в Azure Portal
4. **Используй простые команды** сначала

## АЛЬТЕРНАТИВНЫЙ ПУТЬ

Если Azure CLI команды не работают, можно:

1. **SSH подключиться** к VM напрямую
2. **Выполнить команды вручную** через SSH
3. **Использовать Azure Portal** → Run Command

## КОМАНДЫ ДЛЯ SSH

```bash
# Australia VM
ssh argos@20.53.240.36
cd /home/argos/Argos
python3 main.py --no-gui

# Japan VM  
ssh ava@40.81.208.101
cd /home/ava/argoss
wget https://argdeploy6683.blob.core.windows.net/deploy/src.zip
unzip src.zip
python3 main.py --no-gui
```

## ЧТО ДЕЛАТЬ ДАЛЬШЕ

1. **Установи ARGOS на Japan VM** (команда 2)
2. **Запусти ARGOS** (команда 3)
3. **Проверь соединение** (команда 4)
4. **Если работает** → установи WireGuard для надёжности
5. **Добавь Google Cloud** в P2P сеть

## ПРОБЛЕМЫ И РЕШЕНИЯ

### Проблема: Команды зависают
**Решение:** Жди 2-3 минуты между командами, используй простые тестовые команды сначала

### Проблема: ARGOS не запускается
**Решение:** Проверь логи `tail -50 /home/ava/argoss/argos.log`

### Проблема: Порт 8000 не открывается
**Решение:** Проверь firewall и NSG правила в Azure

### Проблема: Нет соединения между VM
**Решение:** Установи WireGuard для прямого туннеля

## ФИНАЛЬНАЯ ПРОВЕРКА

Когда всё работает, выполни:

```powershell
# Australia проверяет Japan
az vm run-command invoke --resource-group rg-argos --name argos-vm --command-id RunShellScript --scripts "curl -s http://40.81.208.101:8000/health && echo '✅ Japan VM доступна' || echo '❌ Japan VM недоступна'"

# Japan проверяет Australia
az vm run-command invoke --resource-group rg-argos --name argos-vm-jp_27e38b15 --command-id RunShellScript --scripts "curl -s http://20.53.240.36:8000/health && echo '✅ Australia VM доступна' || echo '❌ Australia VM недоступна'"
```

**Если обе команды возвращают ✅ — P2P сеть ARGOS работает!**