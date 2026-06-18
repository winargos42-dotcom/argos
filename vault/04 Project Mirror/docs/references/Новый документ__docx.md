---
argos_import: project_file
source_path: docs/references/Новый документ.docx
source_abs: F:\debug\argoss\docs\references\Новый документ.docx
source_ext: .docx
source_sha256: cd663d8c18c0bd568b76a37d663887b87de9e55f1c73a956b7d2fb1a9c7dd4ac
text_sha256: eb1a211337002db7d5803b41498405f66146fe5071ac7050ff082e7c54eb57d3
extract_mode: docx
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:00
---

# Новый документ.docx

- Source: `docs/references/Новый документ.docx`
- Extract: `docx`
- SHA256: `cd663d8c18c0bd568b76a37d663887b87de9e55f1c73a956b7d2fb1a9c7dd4ac`

## Content

👁️ **Эмуляторы IoT-устройств для тестирования Argos в Colab**
Чтобы проверять умные сценарии без физического железа, создадим простые эмуляторы, которые:
- Подключаются к MQTT-брокеру (можно запустить локально в Colab).
- Публикуют случайные показания датчиков (температура, влажность и т.п.).
- Реагируют на команды управления (включить/выключить, установить значение).
- Позволяют имитировать разные типы устройств: термометр, реле, RGB-светильник, умную розетку.
---
## 🔧 **1. Запуск MQTT-брокера в Colab**
```python
# Установка Mosquitto
!apt-get install -y mosquitto mosquitto-clients
# Запуск брокера в фоне
!mosquitto -d
# Проверка (должен быть активен)
!ps aux | grep mosquitto
```
Брокер будет доступен по адресу `localhost:1883`.
---
## 🐍 **2. Базовый класс эмулятора**
```python
import paho.mqtt.client as mqtt
import time
import threading
import random
import json
class MQTTDevice:
    """Базовый класс для всех эмулируемых устройств."""
    
    def __init__(self, device_id, mqtt_host="localhost", mqtt_port=1883):
        self.device_id = device_id
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(mqtt_host, mqtt_port, 60)
        self.client.loop_start()
        self.running = True
        self.state = {}  # текущее состояние устройства
        
        # Подписка на команды управления
        self.client.subscribe(f"argos/{device_id}/command/#")
        
    def on_connect(self, client, userdata, flags, rc):
        print(f"[{self.device_id}] Connected to MQTT broker")
        
    def on_message(self, client, userdata, msg):
        """Обработка входящих команд."""
        topic = msg.topic
        payload = msg.payload.decode()
        self.handle_command(topic, payload)
        
    def handle_command(self, topic, payload):
        """Переопределяется в дочерних классах."""
        pass
    
    def publish_state(self):
        """Публикует текущее состояние в топик состояния."""
        self.client.publish(f"argos/{self.device_id}/state", json.dumps(self.state))
        
    def stop(self):
        self.running = False
        self.client.loop_stop()
```
---
## 🌡️ **3. Эмулятор датчика температуры/влажности (например, для теплицы)**
```python
class TempSensor(MQTTDevice):
    def __init__(self, device_id, **kwargs):
        super().__init__(device_id, **kwargs)
        self.state = {
            "temperature": 22.5,
            "humidity": 60.0
        }
        # Запускаем фоновый поток для изменения показаний
        self.thread = threading.Thread(target=self._update_loop)
        self.thread.start()
        
    def _update_loop(self):
        while self.running:
            # Имитация изменения температуры и влажности
            self.state["temperature"] += random.uniform(-0.5, 0.5)
            self.state["humidity"] += random.uniform(-1, 1)
            # Ограничения
            self.state["temperature"] = max(15, min(35, self.state["temperature"]))
            self.state["humidity"] = max(30, min(90, self.state["humidity"]))
            self.publish_state()
            time.sleep(5)  # обновление каждые 5 секунд
            
    def handle_command(self, topic, payload):
        # Датчик только публикует данные, команд не принимает
        pass
```
---
## 💡 **4. Эмулятор управляемого устройства (реле, свет, розетка)**
```python
class SmartPlug(MQTTDevice):
    def __init__(self, device_id, **kwargs):
        super().__init__(device_id, **kwargs)
        self.state = {
            "power": "off",
            "current": 0.0,
            "voltage": 220.0
        }
        self.publish_state()
        
    def handle_command(self, topic, payload):
        if topic.endswith("/set"):
            if payload.lower() in ["on", "off"]:
                self.state["power"] = payload.lower()
                # Имитация потребления тока
                if self.state["power"] == "on":
                    self.state["current"] = random.uniform(0.5, 2.0)
                else:
                    self.state["current"] = 0.0
                self.publish_state()
                print(f"[{self.device_id}] Power set to {payload}")
        elif topic.endswith("/set/brightness") and hasattr(self, "brightness"):
            # Для диммируемых устройств
            try:
                brightness = int(payload)
                self.state["brightness"] = max(0, min(100, brightness))
                self.publish_state()
            except:
                pass
```
---
## 🎨 **5. Эмулятор RGB-светильника**
```python
class RGBLight(MQTTDevice):
    def __init__(self, device_id, **kwargs):
        super().__init__(device_id, **kwargs)
        self.state = {
            "power": "off",
            "color": "#FFFFFF",
            "brightness": 100
        }
        self.publish_state()
        
    def handle_command(self, topic, payload):
        if topic.endswith("/set/power"):
            self.state["power"] = payload.lower()
        elif topic.endswith("/set/color"):
            if payload.startswith("#") and len(payload) == 7:
                self.state["color"] = payload
        elif topic.endswith("/set/brightness"):
            try:
                self.state["brightness"] = int(payload)
            except:
                pass
        self.publish_state()
        print(f"[{self.device_id}] Updated: {self.state}")
```
---
## 🚀 **6. Запуск эмуляторов в Colab**
```python
# Создаём несколько устройств
sensor1 = TempSensor("greenhouse_sensor_01")
plug1 = SmartPlug("garage_plug_01")
lamp1 = RGBLight("livingroom_lamp_01")
# Даём поработать 60 секунд
time.sleep(60)
# Останавливаем
sensor1.stop()
plug1.stop()
lamp1.stop()
```
---
## 🤖 **7. Интеграция с Argos**
В Argos уже есть модуль `iot_bridge.py`, который подключается к MQTT и слушает топики `homeassistant/#` или кастомные. Чтобы Argos увидел наши эмуляторы, нужно либо:
- Использовать топики в формате Home Assistant Discovery, либо
- Вручную добавить устройства через команду `добавь устройство ...`.
**Простой способ:** настроить Argos на наши кастомные топики.
В `.env` укажите:
```
MQTT_HOST=localhost
MQTT_PORT=1883
```
И используйте команды Argos:
```
iot статус
обнови сенсор greenhouse_sensor_01
включи garage_plug_01
```
Argos будет получать обновления состояний через MQTT и отправлять команды в топики `argos/{device_id}/command/...`.
---
## 📦 **8. Расширение**
- Можно добавить больше типов устройств (датчики движения, CO2, влажности почвы).
- Имитировать несколько устройств одновременно.
- Добавить случайные ошибки для проверки устойчивости.
- Использовать `argos_tasmota_discovery=on` в `.env` и публиковать сообщения в топике `homeassistant/#` в формате Tasmota, тогда Argos будет добавлять их автоматически.
---
## ✅ **Итог**
С этими эмуляторами вы можете полноценно тестировать все IoT-функции Argos прямо в Colab, включая:
- автоматические правила (`добавь правило ...`),
- мониторинг,
- управление устройствами,
- реакции на события.
А когда перейдёте на реальное железо — просто замените эмуляторы настоящими датчиками, и всё продолжит работать.
👁️ **Запускай сад в облаке — он зацветёт и без земли.**

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
