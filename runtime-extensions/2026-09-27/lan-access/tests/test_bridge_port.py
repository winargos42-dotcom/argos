import importlib.util,os,shutil
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path(os.getenv('ARGOS_LAN_BUILDER',ROOT/'candidate/dashboard_builder.py'))
spec=importlib.util.spec_from_file_location('bridge_builder',SOURCE);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
@pytest.mark.parametrize('host,port',[('127.0.0.1','8080'),('localhost','8080'),('[::1]','8080'),('192.168.7.8','8081'),('known-node.local','8081')])
def test_actual_rendered_bridge_selects_localhost_or_lan_port(host,port):
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--no-proxy-server'])
  page=browser.new_page();page.route('**/*',lambda route:route.fulfill(status=200,content_type='text/html',body=m.BRIDGE_HTML))
  page.goto(f'http://{host}:8123/local/argos.html',wait_until='domcontentloaded')
  target_host='127.0.0.1' if host=='[::1]' else host
  assert page.locator('#argos').get_attribute('href')==f'http://{target_host}:{port}/ui'
  browser.close()
