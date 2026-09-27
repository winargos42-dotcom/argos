import json
from test_panel_regressions import browser,SOURCE,login
from playwright.sync_api import expect


def test_catalog_filter_offline_error_and_logout(browser):
 page=browser.new_page(viewport={'width':390,'height':844});errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
 data={'ok':True,'url':'http://127.0.0.1:8123','counts':{'total':3,'available':1,'unknown':1,'unavailable':1},'observed_at':1790000000,'domains':{'sensor':1,'light':2},'entities':[
 {'entity_id':'sensor.test','name':'<img src=x onerror=alert(1)>','domain':'sensor','state':'5','unit':'W','available':True},
 {'entity_id':'light.offline','name':'Offline light','domain':'light','state':'unavailable','available':False},
 {'entity_id':'light.unknown','name':'Unknown light','domain':'light','state':'unknown','available':False}]}
 def route(r):
  path=r.request.url.split('8080')[1].split('?')[0]
  if path=='/ui':return r.fulfill(status=200,content_type='text/html',body=SOURCE.read_text())
  body={'/api/status':{'ready':True},'/api/tasks':[],'/api/ha':data}[path]
  r.fulfill(status=200,content_type='application/json',body=json.dumps(body))
 page.route('http://127.0.0.1:8080/**',route);page.goto('http://127.0.0.1:8080/ui');login(page);page.locator('#homeTab').click()
 expect(page.locator('#haEntities article')).to_have_count(3)
 assert page.locator('#haEntities img').count()==0
 page.locator('#haDomain').select_option('light');expect(page.locator('#haEntities article')).to_have_count(2)
 page.locator('#haAvailability').select_option('unavailable');expect(page.locator('#haEntities article')).to_have_count(1)
 expect(page.locator('#haEntities .value')).to_have_text('Недоступно')
 page.locator('#haSearch').fill('not present');expect(page.locator('#haShown')).to_have_text('Совпадений не найдено.')
 assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
 data.clear();data.update({'ok':False,'online':'офлайн','entities':[]})
 page.locator('#haRefresh').click();expect(page.locator('#haDetails')).to_contain_text('Данные не получены')
 expect(page.locator('#haEntities article')).to_have_count(0);expect(page.locator('#haDashboard')).to_be_hidden()
 page.locator('#logout').click();assert page.locator('#haEntities').inner_text()==''
 assert not errors;page.close()
