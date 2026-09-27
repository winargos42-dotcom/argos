"""Pure MQTT diagnostic schemas. Callers supply ONLY fresh observations.

Adapters own probe deadlines and timestamps: on stale/error input publish source
OFFLINE and normalize disconnected/unknown fields. Retained ONLINE must never be
reused as freshness evidence. Bridge startup/reconnect stays OFFLINE until fresh
observations; LWT publishes bridge OFFLINE. No command entities are created. Worker service_ready describes transport only,
not TPU inference readiness.
"""
import math
import re

BRIDGE_AVAILABILITY_TOPIC = 'argos/nodes/bridge/availability'
STATE_EXPIRY_SECONDS = 90
ROLES = frozenset(('worker','server','gateway','primary','secondary','accelerator'))
ERRORS = frozenset(('timeout','unreachable','stale','unauthenticated','invalid_response',
                    'not_configured','service_unavailable','unknown_error'))
ID = re.compile(r'[a-z0-9][a-z0-9_-]{0,63}\Z')


def _identifier(value):
    return isinstance(value,str) and ID.fullmatch(value) is not None


def normalize_state(observation: dict) -> dict:
    if not isinstance(observation,dict):
        raise ValueError('observation must be a dictionary')
    connected=observation.get('connected')
    connected=connected if type(connected) is bool else None
    ready=observation.get('service_ready')
    uptime=observation.get('uptime_seconds')
    error=observation.get('error')
    role=observation.get('role')
    node_id=observation.get('node_id')
    result = {
        'connected':connected,
        'service_ready':ready if connected is True and type(ready) is bool else None,
        'role':role if isinstance(role,str) and role in ROLES else None,
        'uptime_seconds':uptime if connected is True and type(uptime) in (int,float)
            and 0 <= uptime <= 3155760000 and math.isfinite(uptime) else None,
        'node_id':node_id if _identifier(node_id) else None,
        'error':None if error is None else error if isinstance(error,str) and error in ERRORS else 'unknown_error',
    }
    if observation.get('status_source') == 'coral_accelerator_api':
        result.update(status_source='coral_accelerator_api', readiness_scope='signed_status',
                      inference_verified=False,
                      authenticated=observation.get('authenticated') is True if connected is True else None)
    return result


def discovery(node: dict) -> dict:
    if not isinstance(node,dict):
        raise ValueError('node must be a dictionary')
    ident,name,kind=(node.get(k) for k in ('id','name','kind'))
    if (not _identifier(ident) or ident in ('bridge','panel7','tuya','tuya_switch4')
            or not isinstance(name,str) or not 1 <= len(name) <= 80
            or any(ord(c)<32 for c in name)
            or not _identifier(kind) or kind in ('panel','panel7','tuya','switch')):
        raise ValueError('invalid or already managed node')
    device_id='argos_node_'+ident
    prefix='argos/nodes/'+ident
    device={'identifiers':[device_id],'name':name,'manufacturer':'ARGOS','model':kind}
    availability=[{'topic':topic,'payload_available':'ONLINE','payload_not_available':'OFFLINE'}
                  for topic in (prefix+'/availability',BRIDGE_AVAILABILITY_TOPIC)]
    result={}
    for key,label,binary in (('connected','Connectivity',True),('service_ready','Service ready',True),
                             ('role','Role',False),('uptime_seconds','Uptime',False)):
        component='binary_sensor' if binary else 'sensor'
        if kind == 'coral_accel' and key == 'service_ready':
            label = 'Signed status ready'
        config={'name':label,'unique_id':device_id+'_'+key,'device':dict(device),
                'state_topic':prefix+'/state','availability':[dict(a) for a in availability],
                'availability_mode':'all','expire_after':STATE_EXPIRY_SECONDS,'entity_category':'diagnostic'}
        valid = ('value_json.'+key+' is sameas true or value_json.'+key+' is sameas false') if binary else ('value_json.'+key+' is defined and value_json.'+key+' is not none')
        config['availability'].append({'topic':prefix+'/state',
            'payload_available':'ONLINE','payload_not_available':'OFFLINE',
            'value_template':"{{ 'ONLINE' if ("+valid+") else 'OFFLINE' }}"})
        if binary:
            config.update({'payload_on':'ON','payload_off':'OFF',
                'value_template':"{{ 'ON' if value_json."+key+" is sameas true else 'OFF' if value_json."+key+" is sameas false else 'None' }}"})
            if key=='connected':config['device_class']='connectivity'
        else:
            config['value_template']="{{ value_json."+key+" if value_json."+key+" is not none else 'None' }}"
            if key=='uptime_seconds':config.update({'device_class':'duration','unit_of_measurement':'s','state_class':'measurement'})
        if kind == 'coral_accel':
            config['json_attributes_topic'] = prefix+'/state'
            config['json_attributes_template'] = "{{ {'status_source': value_json.status_source | default(none), 'readiness_scope': value_json.readiness_scope | default(none), 'inference_verified': value_json.inference_verified | default(none), 'authenticated': value_json.authenticated | default(none)} | tojson }}"
        result[f'homeassistant/{component}/{device_id}/{key}/config']=config
    return result
