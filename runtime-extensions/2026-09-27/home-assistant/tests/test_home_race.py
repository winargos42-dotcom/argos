import json
from test_panel_regressions import browser,panel,login,ha_ready
from playwright.sync_api import expect


def test_older_ha_success_cannot_restore_entities_after_newer_offline(panel):
    page,_,settings,pending=panel
    login(page);ha_ready(page)
    settings['hold_ha']=True
    page.locator('#homeTab').click()
    page.wait_for_timeout(30)
    assert len(pending)==1
    page.clock.run_for(15000)
    page.wait_for_timeout(30)
    assert len(pending)==2
    older,newer=pending[:]
    newer.fulfill(status=200,content_type='application/json',body=json.dumps({'ok':False,'online':'офлайн','entities':[]}))
    expect(page.locator('#haDetails')).to_contain_text('Данные не получены')
    older.fulfill(status=200,content_type='application/json',body=json.dumps({'ok':True,'url':'http://127.0.0.1:8123','observed_at':1000,'counts':{'total':1,'available':1},'domains':{'sensor':1},'entities':[{'entity_id':'sensor.fixture','domain':'sensor','name':'Old response','state':'5','unit':'W','available':True}]}))
    page.wait_for_timeout(100)
    expect(page.locator('#haEntities article')).to_have_count(0,timeout=500)
    expect(page.locator('#haDashboard')).to_be_hidden(timeout=500)


def test_older_ha_error_cannot_erase_newer_success(panel):
    page,_,settings,pending=panel
    login(page);ha_ready(page)
    settings['hold_ha']=True
    page.locator('#homeTab').click();page.wait_for_timeout(30)
    page.clock.run_for(15000);page.wait_for_timeout(30)
    assert len(pending)==2
    older,newer=pending[:]
    newer.fulfill(status=200,content_type='application/json',body=json.dumps({'ok':True,'url':'http://127.0.0.1:8123','observed_at':2000,'counts':{'total':1,'available':1},'domains':{'sensor':1},'entities':[{'entity_id':'sensor.fixture','domain':'sensor','name':'New response','state':'6','unit':'W','available':True}]}))
    expect(page.locator('#haEntities article')).to_have_count(1)
    older.fulfill(status=500,content_type='application/json',body=json.dumps({'detail':'old upstream failure'}))
    page.wait_for_timeout(100)
    expect(page.locator('#haEntities article')).to_have_count(1,timeout=500)
    expect(page.locator('#haEntities .value')).to_have_text('6 W')
    expect(page.locator('#haDashboard')).to_be_visible(timeout=500)
