---
argos_import: project_file
source_path: data/telegram his/files/Новый текстовый документ (3).txt
source_abs: F:\debug\argoss\data\telegram his\files\Новый текстовый документ (3).txt
source_ext: .txt
source_sha256: ea12295cfbf2317cce195b7f41aad332609a60881b3328525a41eae9ba359b28
text_sha256: a38794b7140b7a707ec96389bc23cf64a396abc950efe2f3f6d92b6928f4f940
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-08 13:16:46
---

# Новый текстовый документ (3).txt

- Source: `data/telegram his/files/Новый текстовый документ (3).txt`
- Extract: `text`
- SHA256: `ea12295cfbf2317cce195b7f41aad332609a60881b3328525a41eae9ba359b28`

## Content

PS F:\debug\argoss> cd F:\debug\argoss
>> cat src/core.py | findstr /n "def set_ai_mode\|ai_mode_label\|_ai_generate\|ollama\|openai\|gemini\|gigachat"
93:def _read_secret_env(name: str) -> str:
100:def _env_disabled(name: str) -> bool:
118:    def __init__(self, max_calls: int, window_seconds: int):
124:    def allow(self) -> bool:
136:    def __init__(self, text: str = ""):
142:    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
160:    def _resolve_model_name(self, requested: str) -> str:
199:    def generate_content(self, contents):
229:    def _neutralize_broken_proxy_env() -> None:
286:    def __init__(self):
466:    def _init_constitution(self):
482:    def _init_memory(self):
503:    def _init_cloud_object_storage(self):
512:    def _init_scheduler(self):
521:    def _init_homeostasis(self):
531:    def _init_curiosity(self):
541:    def _init_alerts(self):
550:    def _init_vision(self):
558:    def _init_skills(self):
597:    def _init_dags(self):
604:    def _init_marketplace(self):
611:    def _init_iot(self):
651:    def _init_industrial(self):
660:    def _init_platform_admin(self):
669:    def _init_smart_systems(self):
679:    def _init_modules(self):
688:    def _init_home_assistant(self):
696:    def _init_tool_calling(self):
742:    def _init_external_services(self):
785:    def _ask_watsonx(self, system: str, user: str):
798:    def _startup_auto_update(self):
808:        def _do_update():
858:    def _init_powershell_bridge(self):
899:        def _start_bridge():
931:    def _init_git_ops(self):
939:    def _init_otg(self):
948:    def _init_grist(self):
960:    def _init_own_model(self):
969:    def _init_argoss_evolver(self):
981:    def _init_opi(self):
991:    def _init_integrator(self):
1005:    def _init_web_explorer(self):
1018:    def _init_awa_core(self):
1036:    def _init_sustain(self):
1050:    def _init_health_monitor(self):
1065:    def _init_ai_failover(self):
1215:    def _looks_like_awareness_scan_request(self, text: str) -> bool:
1237:    def _extract_direct_url(self, text: str) -> str | None:
1256:    def _looks_like_bulk_text_dump(self, text: str) -> bool:
1294:    def _analyze_bulk_text_dump(self, text: str) -> str:
1384:    def _scan_project_inventory(self, root: str | Path | None = None) -> dict:
1440:    def _system_awareness_report(self, admin=None) -> str:
1491:    def _classify_input(self, text: str) -> str:
1510:    def _safe_dump_response(self, text: str) -> str:
1526:    def _direct_dispatch(self, text: str, admin) -> str | None:
1570:    def process(self, user_text: str, admin=None, flasher=None) -> dict:
1576:    def _on_alert(self, msg: str):
1580:    def _remember_dialog_turn(self, user_text: str, answer: str, state: str):
1592:    def before_patch_file(self, patch_id: str, file_path: str):
1598:    def after_patch_success(self, patch_id: str):
1602:    def after_patch_failure(self, patch_id: str):
1610:    def handle_agent_step(self, step_text: str, execute_fn):
1619:    def start_p2p(self) -> str:
1625:    def start_dashboard(self, admin, flasher, port: int = 8080) -> str:
1642:    def start_wake_word(self, admin, flasher) -> str:
1653:    def _init_voice(self):
1669:    def say(self, text: str):
1672:        def _speak():
1681:    def listen(self) -> str:
1704:    def _transcribe_with_whisper(self, audio_data) -> str:
1728:    def transcribe_audio_path(self, audio_path: str) -> str:
1747:    def voice_services_report(self) -> str:
1763:    def _normalize_ai_mode(self, mode: str) -> str:
1793:    def set_ai_mode(self, mode: str) -> str:
1797:    def _clear_persona_profile(self) -> None:
1801:    def _apply_chatgpt_link_profile(self, text: str) -> str | None:
1849:    def ai_mode_label(self) -> str:
1863:    def _setup_ai(self):
1901:    def _gemini_rate_limit_text(self) -> str:
1905:    def _is_host_reachable(host: str, port: int = 443, timeout: float = 2.0) -> bool:
1918:    def _has_gigachat_config(self) -> bool:
1929:    def _has_yandexgpt_config(self) -> bool:
1934:    def _has_kimi_config(self) -> bool:
1938:    def _has_watsonx_config(self) -> bool:
1941:    def _is_provider_temporarily_disabled(self, provider_name: str) -> bool:
1951:    def _disable_provider_temporarily(self, provider_name: str, reason: str) -> None:
1969:    def _get_gigachat_token(self) -> str | None:
2040:    def _ask_gemini(self, context: str, user_text: str) -> str | None:
2062:    def _ask_gigachat(self, context: str, user_text: str) -> str | None:
2118:    def _ask_yandexgpt(self, context: str, user_text: str) -> str | None:
2178:    def _ask_kimi(self, context: str, user_text: str) -> str | None:
2210:    def _ask_kimi_with_tools(self, context: str, user_text: str) -> str | None:
2242:    def _ask_openai_compat(self, context: str, user_text: str,
2264:        env_keys, base_url, default_model = cfg[provider_name]
2282:            model = os.getenv(f"{provider_name.upper()}_MODEL", default_model).strip() or default_model
2325:    def _ask_grok(self, context: str, user_text: str) -> str | None:
2329:    def _ask_openai(self, context: str, user_text: str) -> str | None:
2339:    def _ensure_ollama_running(self) -> bool:
2459:    def _ensure_ollama_model(self, model: str) -> bool:
2505:    def _ask_ollama_reflex(self, context: str, user_text: str) -> str | None:
2567:    def _ask_ollama_vega(self, user_text: str) -> str | None:
2615:    def _is_micro_query(self, text: str) -> bool:
2626:    def _is_simple_query(self, text: str) -> bool:
2637:    def _ask_ollama(self, context: str, user_text: str, model_override: str | None = None) -> str | None:
2681:    def _ask_ollama_inner(self, context: str, user_text: str, model_override: str | None = None) -> str | None:
2763:    def _auto_providers(self) -> list[tuple[str, callable\]\]:
2766:        def _any_key(*names: str) -> bool:
2796:    def _ask_auto_consensus(self, context: str, user_text: str) -> tuple[str | None, str | None]:
2856:    def process_logic(self, user_text: str, admin, flasher) -> dict:
3214:    def _is_tool_command(self, text: str) -> bool:
3242:    def _validate_ai_answer(self, answer: str, user_text: str) -> str:
3380:    def dispatch_skill(self, text: str, t: str = "") -> str | None:
3384:    def _dispatch_skill(self, text: str, t: str = "") -> str | None:
3457:    def dispatchskill(self, text: str, t: str | None = None) -> str | None:
3461:    def _skills_list(self) -> str:
3464:    def _run_skill(self, skill_name: str, class_name: str | None,
3611:    def _import_skill(self, skill_name: str, class_name: str = ""):
3660:                            def __init__(self_w): pass
3661:                            def __call__(self_w, *a, **kw): return fn(*a, **kw)
3663:                            def report(self_w):   return fn()
3664:                            def scan(self_w):     return fn()
3665:                            def generate_digest(self_w): return fn()
3666:                            def list_skills(self_w):     return fn()
3678:    def _builtin_net_scan(self) -> str:
3701:        def ping_host(ip):
3770:    def _builtin_crypto_report(self) -> str:
3800:    def _skills_diagnostic(self) -> str:
3908:    def _self_update(self) -> str:
3969:    def _offline_answer(self, user_text: str) -> str:
4050:    async def process_logic_async(self, user_text: str, admin=None, flasher=None) -> dict:
4061:    def execute_intent(self, text: str, admin, flasher) -> str | None:
5861:                f"  ??????????: {s.default_channel or '??? ?????????? SLACK_DEFAULT_CHANNEL'}"
6313:                "defender ????????????", "windows defender",
6314:                "defender ??????????????????????", "defender scan",
6804:    def _operator_incident(self, admin) -> str:
6814:    def _operator_diagnostics(self, admin) -> str:
6830:    def _operator_recovery(self) -> str:
6837:    def _ai_modes_diagnostic(self) -> str:
6910:        def _chk(mod):
6970:    def _help(self) -> str:
7113:    def _argoscore_functions(self) -> str:
7179:    def _iot_protocols_help(self) -> str:
7209:    def _rs_ttl_help(self) -> str:
7230:    def _low_level_drivers_report(self) -> str:
7231:        def _module_ok(name: str) -> bool:
7238:        def _threading_line() -> str:
7243:        def _power_line() -> str:
7254:        def _video_line() -> str:
7261:                def _trusted_binary(path: str | None) -> str | None:
7275:                def _sanitize_gpu_name(text: str, max_length: int = 120) -> str:
7330:    def _start_smart_create_wizard(self) -> str:
7350:    def _continue_smart_create_wizard(self, text: str) -> str:
7373:            if value.lower() in ("????????", "auto", "default"):
7400:            if value.lower() not in ("????????", "auto", "default"):
PS F:\debug\argoss>

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
