"""Rendered session/provenance regressions; all routes are local test fixtures."""
import json
import os
import shutil
from pathlib import Path

import pytest
pytest.importorskip('playwright.sync_api')
from playwright.sync_api import expect, sync_playwright

SOURCE = Path(os.getenv('ARGOS_PANEL_HTML', 'src/interface/control_panel.html')).resolve()
CHROMIUM = os.getenv('ARGOS_CHROMIUM') or shutil.which('chromium')
pytestmark = pytest.mark.skipif(not SOURCE.is_file() or not CHROMIUM,
    reason='Requires compatible ARGOS control_panel.html and an existing Chromium executable')
MAP = {'origin': 'current_registry', 'source': 'runtime_discovery', 'text': 'CURRENT VERIFIED SYSTEM MAP: test node',
       'wing': 'technical', 'room': 'current_system'}


@pytest.fixture(scope='module')
def browser():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=CHROMIUM, headless=True,
                                    args=['--no-sandbox', '--disable-dev-shm-usage', '--no-proxy-server'])
        yield browser
        browser.close()


@pytest.fixture
def panel(browser):
    page = browser.new_page(viewport={'width': 1200, 'height': 900})
    page.clock.install()
    calls = []
    pending = []
    settings = {'hold_ha': False}

    def route(request):
        path = request.request.url.split('8080', 1)[1].split('?', 1)[0]
        if path == '/ui':
            request.fulfill(status=200, content_type='text/html', body=SOURCE.read_text())
            return
        auth = request.request.headers.get('authorization') == 'Bearer test-only-key'
        calls.append((path, auth))
        if not auth:
            request.fulfill(status=401, content_type='application/json', body='{"detail":"unauthorized"}')
            return
        if path == '/api/ha' and settings['hold_ha']:
            pending.append(request)
            return
        body = {'/api/status': {'ready': True, 'memory': {}}, '/api/tasks': [],
                '/api/memory/search': [MAP], '/api/ha': {'ok': True, 'url': 'http://127.0.0.1:8123'}}[path]
        request.fulfill(status=200, content_type='application/json', body=json.dumps(body))

    page.route('http://127.0.0.1:8080/**', route)
    page.goto('http://127.0.0.1:8080/ui', wait_until='domcontentloaded')
    yield page, calls, settings, pending
    page.close()


def login(page):
    page.locator('#accessKey').fill('test-only-key')
    page.locator('#loginForm button').click()
    expect(page.locator('#workspace')).to_be_visible()


def ha_ready(page):
    page.clock.run_for(15000)
    expect(page.locator('#haLink')).to_be_visible()


def test_current_discovery_map_has_current_provenance_and_no_fake_id(panel):
    page, _, _, _ = panel
    login(page)
    page.locator('#memoryTab').click()
    page.locator('#memoryQuery').fill('Coral')
    page.locator('#searchForm button').click()
    expect(page.locator('#memoryResults summary')).to_have_text('Текущая карта системы · Источник')
    assert 'undefined' not in page.locator('#memoryResults pre').inner_text()


def test_logged_out_panel_does_not_poll_authenticated_ha_api(panel):
    page, calls, _, _ = panel
    page.clock.run_for(15000)
    assert not any(path == '/api/ha' for path, _ in calls)


def test_logout_clears_verified_ha_link_immediately(panel):
    page, _, _, _ = panel
    login(page)
    ha_ready(page)
    page.locator('#logout').click()
    expect(page.locator('#haLink')).to_be_hidden(timeout=1000)
    assert page.locator('#haLink').get_attribute('href') is None


def test_ha_response_after_logout_cannot_reopen_link(panel):
    page, _, settings, pending = panel
    login(page)
    ha_ready(page)
    settings['hold_ha'] = True
    page.clock.run_for(15000)
    page.wait_for_timeout(30)
    assert pending
    page.locator('#logout').click()
    pending.pop().fulfill(status=200, content_type='application/json',
                          body=json.dumps({'ok': True, 'url': 'http://127.0.0.1:8123'}))
    page.wait_for_timeout(50)
    expect(page.locator('#haLink')).to_be_hidden(timeout=1000)


def test_old_ha_unauthorized_response_cannot_log_out_new_session(panel):
    page, _, settings, pending = panel
    login(page)
    ha_ready(page)
    settings['hold_ha'] = True
    page.clock.run_for(15000)
    page.wait_for_timeout(30)
    assert pending
    old_request = pending.pop()
    page.locator('#logout').click()
    settings['hold_ha'] = False
    login(page)
    old_request.fulfill(status=401, content_type='application/json', body='{"detail":"old session expired"}')
    page.wait_for_timeout(80)
    expect(page.locator('#workspace')).to_be_visible(timeout=1000)
    expect(page.locator('#login')).to_be_hidden(timeout=1000)


def test_current_session_unauthorized_response_still_logs_out(panel):
    page, _, settings, pending = panel
    login(page)
    ha_ready(page)
    settings['hold_ha'] = True
    page.clock.run_for(15000)
    page.wait_for_timeout(30)
    assert pending
    pending.pop().fulfill(status=401, content_type='application/json', body='{"detail":"session expired"}')
    expect(page.locator('#workspace')).to_be_hidden(timeout=1000)
    expect(page.locator('#login')).to_be_visible(timeout=1000)
