"""Build an additive read-only HA dashboard from the actual entity catalog."""

def build(states):
    groups = {name: [] for name in ['Электричество', 'ARGOS · узлы и Panel 7', 'Свет и выключатели', 'Климат и датчики', 'Интеграции ARGOS']}
    for row in states:
        entity = row.get('entity_id', '')
        domain = entity.split('.')[0]
        attrs = row.get('attributes') or {}
        if not entity or '.' not in entity:
            continue
        if domain == 'automation' and 'argos' in entity:
            group = 'Интеграции ARGOS'
        elif domain in ('sensor', 'binary_sensor') and '.argos_' in entity:
            group = 'ARGOS · узлы и Panel 7'
        elif domain == 'sensor' and attrs.get('device_class') in ('voltage', 'current', 'power', 'apparent_power', 'energy', 'frequency'):
            group = 'Электричество'
        elif domain in ('switch', 'light'):
            group = 'Свет и выключатели'
        elif domain == 'climate' or (domain in ('sensor', 'binary_sensor') and attrs.get('device_class') in ('temperature', 'humidity', 'door', 'window', 'opening', 'motion', 'occupancy', 'problem')):
            group = 'Климат и датчики'
        else:
            continue
        groups[group].append({'entity': entity, 'type': 'simple-entity',
                              'tap_action': {'action': 'none'}, 'hold_action': {'action': 'none'},
                              'double_tap_action': {'action': 'none'}})
    cards = [{'type': 'markdown', 'content': '# ARGOS · Дом\nРеальные состояния Home Assistant. Эта панель только для чтения: недоступные устройства не считаются выключенными.\n\n[Открыть ARGOS на этой машине (локальная сеть)](/local/argos.html) · [Обзор HA](/lovelace)'}]
    cards += [{'type': 'entities', 'title': name, 'show_header_toggle': False,
               'state_color': False, 'entities': rows} for name, rows in groups.items() if rows]
    return {'title': 'ARGOS · Дом', 'views': [{'title': 'Дом', 'path': 'overview', 'icon': 'mdi:home-analytics', 'cards': cards}]}

BRIDGE_HTML = '''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Открыть ARGOS</title><style>body{font:18px/1.6 system-ui;margin:10vh auto;max-width:600px;padding:20px}a{display:inline-block;padding:14px;border:1px solid;border-radius:10px}</style><h1>Рабочая панель ARGOS</h1><p>Переход к ARGOS на той же машине в локальной сети. Вход выполняется отдельным ключом ARGOS.</p><a id="argos">Открыть ARGOS →</a><p>При доступе к Home Assistant через внешний прокси используйте настроенный внешний адрес ARGOS.</p><script>const url=new URL(location.href);url.protocol='http:';if(url.hostname==='[::1]')url.hostname='127.0.0.1';url.port=['127.0.0.1','localhost','[::1]'].includes(url.hostname)?'8080':'8081';url.pathname='/ui';url.search='';url.hash='';document.getElementById('argos').href=url.href;</script></html>'''
