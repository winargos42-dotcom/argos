"""Read-only HA snapshot. No service calls or unfiltered entity attributes."""
from __future__ import annotations

import math
import os
import time
from pathlib import Path

import requests

OFFLINE = {'unavailable', 'unknown'}


def summarize(states, temperature_unit=None):
    if not isinstance(states, list) or len(states) > 10000:
        raise ValueError('Invalid HA state list')
    rows = []
    for state in states:
        if (not isinstance(state, dict) or not isinstance(state.get('entity_id'), str)
                or '.' not in state['entity_id'] or not isinstance(state.get('state'), str)):
            raise ValueError('Invalid HA state')
        attrs = state.get('attributes') or {}
        if not isinstance(attrs, dict):
            raise ValueError('Invalid HA attributes')
        rows.append({'entity_id': state['entity_id'], 'domain': state['entity_id'].split('.')[0],
                     'state': state['state'], 'available': state['state'] not in OFFLINE,
                     'name': str(attrs.get('friendly_name') or state['entity_id']),
                     'unit': str(attrs.get('unit_of_measurement') or ''),
                     'device_class': str(attrs.get('device_class') or ''),
                     'last_updated': state.get('last_updated'), 'last_changed': state.get('last_changed')})
    counts = {'total': len(rows), 'available': sum(row['available'] for row in rows),
              'unavailable': sum(row['state'] == 'unavailable' for row in rows),
              'unknown': sum(row['state'] == 'unknown' for row in rows)}
    domains = {domain: sum(row['domain'] == domain for row in rows)
               for domain in sorted({row['domain'] for row in rows})}
    lights = sum(row['state'] == 'on' and row['domain'] in ('light', 'switch')
                 and 'child_lock' not in row['entity_id'] for row in rows)
    out = {'ok': True, 'online': f"{counts['available']}/{counts['total']}",
           'counts': counts, 'domains': domains, 'entities': rows,
           'lights_on': f'{lights} шт', 'voltage': '—', 'power': '—', 'climate': '—'}
    live = [row for row in rows if row['available'] and row['domain'] == 'sensor']
    for field, units in [('voltage', [('V', 1, 'В')]),
                         ('power', [('W', 1, 'Вт'), ('kW', 1000, 'Вт'), ('VA', 1, 'ВА'), ('kVA', 1000, 'ВА')])]:
        found = False
        for unit, factor, label in units:
            for row in live:
                if row['unit'] != unit:
                    continue
                try:
                    value = float(row['state']) * factor
                except (ValueError, TypeError):
                    continue
                if math.isfinite(value):
                    out[field] = f'{value:g} {label}'
                    found = True
                    break
            if found:
                break
    for state in states:
        if state['entity_id'].startswith('climate.') and state['state'] not in OFFLINE:
            current = (state.get('attributes') or {}).get('current_temperature')
            try:
                value = float(current) if not isinstance(current, bool) else float('nan')
            except (ValueError, TypeError):
                value = float('nan')
            if math.isfinite(value):
                unit = temperature_unit if temperature_unit in ('°C', '°F') else ' (единица не подтверждена)'
                out['climate'] = f"{value:g}{unit} ({state['state']})"
            else:
                out['climate'] = state['state']
            break
    return out


def snapshot():
    from src.runtime_registry import api_url
    out = {'ok': False, 'url': '', 'dashboard_path': '/argos-home/overview',
           'lights_on': '—', 'voltage': '—', 'power': '—', 'climate': '—', 'online': 'офлайн',
           'entities': [], 'domains': {}, 'counts': {}, 'observed_at': None, 'read_only': True}
    url = api_url('home_assistant', os.getenv('ARGOS_HA_URL'), 'http://127.0.0.1:8123')
    if not url:
        out.update(error='address_unverified', online='адрес не подтверждён')
        return out
    try:
        token = Path(os.getenv('ARGOS_HA_TOKEN_FILE', '/etc/argos/ha-token')).read_text().strip()
    except OSError:
        token = ''
    if not token:
        out.update(error='token_missing', online='нет токена')
        return out
    try:
        response = requests.get(url + '/api/states', headers={'Authorization': 'Bearer ' + token}, timeout=5)
        response.raise_for_status()
        states = response.json()
        temperature_unit = None
        if isinstance(states, list) and any(isinstance(row, dict) and str(row.get('entity_id', '')).startswith('climate.') and row.get('state') not in OFFLINE for row in states):
            try:
                config = requests.get(url + '/api/config', headers={'Authorization': 'Bearer ' + token}, timeout=3)
                config.raise_for_status()
                temperature_unit = config.json().get('unit_system', {}).get('temperature')
            except (requests.RequestException, ValueError, AttributeError, TypeError):
                pass
        out.update(summarize(states, temperature_unit), url=url, observed_at=time.time())
    except requests.HTTPError as exc:
        out['error'] = 'authentication_failed' if exc.response is not None and exc.response.status_code in (401, 403) else 'upstream_http_error'
    except requests.RequestException:
        out['error'] = 'unreachable'
    except (ValueError, TypeError):
        out['error'] = 'invalid_response'
    return out
