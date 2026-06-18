# ARGOS — OSINT-разведка интегрирована в MCP — 2026-06-04

## Источник
Hermes создал `~/.hermes/skills/osint-recon/osint_tools.py` на ноутбуке (475 строк).
Скопировано на Orion через `ssh argos-laptop` → `F:\debug\argoss\scripts\osint\`.

## Проверка реальности
- osint_tools.py 475 строк, компилируется на Orion ✓.
- 17 сервисов / 26 функций: shodan_search/host, censys_hosts, fofa_search, zoomeye_host,
  fullhunt_domain, urlscan_submit/result, hunter_domain_emails, crtsh, grepapp_search,
  securitytrails_domain/subdomains, intelx_search, hibp_check, leakix_search/host,
  dehashed_search, vulners_search/cve_summary, greynoise_context/quick, wigle_search,
  + комбо quick_recon, ip_recon.
- Тесты: crt.sh — реальный HTTP (502 у них временно); shodan без ключа → аккуратный
  stub {"status":"stub","env_keys_required":["SHODAN_API_KEY"]}. Структура рабочая.

## Интеграция в ARGOS MCP (src/mcp_api.py)
Добавлен tool `osint` (3 места, схема как headroom):
1. tools list — определение osint {service, query}.
2. обработчик — elif name == "osint" → self._osint(service, query).
3. метод `_osint(service, query)` — диспетчер: getattr(osint_tools, service)(query),
   возвращает JSON. Неизвестный service → список доступных.

Вызов: `osint(service="shodan_search", query="apache")` или
`osint(service="crtsh", query="example.com")`, `osint(service="quick_recon", query="1.2.3.4")`.

## Проверка
- py_compile src/mcp_api.py → ✓.
- _osint работает: публичные сервисы → HTTP, с ключами → stub.

## Для полной работы — API ключи в .env
SHODAN_API_KEY, CENSYS_API_ID/SECRET, FOFA_KEY, ZOOMEYE_KEY, FULLHUNT_KEY, URLSCAN_KEY,
HUNTER_KEY, SECURITYTRAILS_KEY, INTELX_KEY, HIBP_KEY, LEAKIX_KEY, DEHASHED_KEY,
VULNERS_KEY, GREYNOISE_KEY, WIGLE_KEY. Без ключа сервис возвращает stub (crt.sh/grep.app
работают без ключей). Список нужного ключа — в stub-ответе каждого сервиса.

## Статус
- [x] osint_tools.py проверен, скопирован на Orion (scripts/osint/)
- [x] tool `osint` интегрирован в ARGOS MCP (mcp_api.py), компилируется, работает
- [ ] API ключи в .env (по мере необходимости)
- [ ] появится в живом MCP после рестарта ARGOS
