import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('builder',Path(__file__).resolve().parents[1]/'dashboard_builder.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def test_native_rows_only_existing_entities_without_controls():
 states=[{'entity_id':'sensor.test_power','attributes':{'device_class':'power'}},{'entity_id':'switch.test'},{'entity_id':'binary_sensor.argos_test'},{'entity_id':'climate.test'}]
 conf=m.build(states);rows=[r for c in conf['views'][0]['cards'] if c['type']=='entities' for r in c['entities']]
 assert {r['entity'] for r in rows}=={x['entity_id'] for x in states}
 for row in rows:
  assert row['type']=='simple-entity'
  assert row['tap_action']==row['hold_action']==row['double_tap_action']=={'action':'none'}
 assert all(not c.get('show_header_toggle') for c in conf['views'][0]['cards'])
