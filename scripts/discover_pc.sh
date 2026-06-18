#!/bin/bash
# Обновляет IP ПК (Orion/DESKTO) в /etc/hosts по MAC-адресу
# MAC: 2c:fd:a1:b7:e8:e0
# Запускать: cron каждые 5 минут

PC_MAC="2c:fd:a1:b7:e8:e0"
PC_HOSTNAME="orion-pc"
SUBNET="192.168.1"
HOSTS_FILE="/etc/hosts"
ENV_FILE="/home/ava/Projects/argoss/.env"

# Сканируем сеть
nmap -sn "${SUBNET}.0/24" -oG - 2>/dev/null | grep "Up" | while read -r line; do
    IP=$(echo "$line" | grep -oP '\d+\.\d+\.\d+\.\d+')
    MAC=$(arp -n "$IP" 2>/dev/null | grep -oP '([0-9a-f]{2}:){5}[0-9a-f]{2}' | head -1)
    if [[ "${MAC,,}" == "${PC_MAC,,}" ]]; then
        echo "$IP"
        exit 0
    fi
done > /tmp/pc_ip_new.txt

NEW_IP=$(cat /tmp/pc_ip_new.txt 2>/dev/null | head -1)
if [[ -z "$NEW_IP" ]]; then
    echo "[discover_pc] ПК не найден в сети $(date)"
    exit 1
fi

OLD_IP=$(grep "$PC_HOSTNAME" "$HOSTS_FILE" 2>/dev/null | awk '{print $1}')
if [[ "$NEW_IP" == "$OLD_IP" ]]; then
    echo "[discover_pc] IP не изменился: $NEW_IP $(date)"
    exit 0
fi

echo "[discover_pc] Обновляем IP ПК: $OLD_IP → $NEW_IP $(date)"

# /etc/hosts
sudo sed -i "/$PC_HOSTNAME/d" "$HOSTS_FILE"
echo "$NEW_IP  $PC_HOSTNAME orion" | sudo tee -a "$HOSTS_FILE" > /dev/null

# .env
if grep -q "PC_IP=" "$ENV_FILE" 2>/dev/null; then
    sed -i "s/^PC_IP=.*/PC_IP=$NEW_IP/" "$ENV_FILE"
else
    echo "PC_IP=$NEW_IP" >> "$ENV_FILE"
fi

# Обновляем Brain API знание о ПК
curl -s -X POST "http://localhost:5001/brain/register" \
    -H "Content-Type: application/json" \
    -d "{\"node_id\":\"argos-pc\",\"address\":\"$NEW_IP\",\"status\":\"online\"}" \
    > /dev/null 2>&1

echo "[discover_pc] Готово: $PC_HOSTNAME → $NEW_IP"
