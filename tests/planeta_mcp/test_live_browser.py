from integrations.planeta_mcp.live_browser import LiveBrowserRuntime


def test_live_browser_runtime_uses_loopback_only(tmp_path):
    runtime = LiveBrowserRuntime(data_dir=tmp_path)

    assert runtime.cdp_url == "http://127.0.0.1:9222"
    assert runtime.vnc_host == "127.0.0.1"
    assert runtime.vnc_port == 5900
    assert runtime.websockify_url == "tcp://127.0.0.1:5900"


def test_live_browser_commands_never_expose_control_ports(tmp_path):
    runtime = LiveBrowserRuntime(data_dir=tmp_path)

    assert runtime.xvfb_command() == [
        "Xvfb",
        ":99",
        "-screen",
        "0",
        "1365x768x24",
        "-nolisten",
        "tcp",
    ]
    assert "-localhost" in runtime.vnc_command()
    assert runtime.vnc_command()[runtime.vnc_command().index("-rfbport") + 1] == "5900"
    assert "--remote-debugging-address=127.0.0.1" in runtime.chromium_args()
    assert "--remote-debugging-port=9222" in runtime.chromium_args()


def test_live_browser_profile_is_inside_data_dir(tmp_path):
    runtime = LiveBrowserRuntime(data_dir=tmp_path)
    assert runtime.profile_dir == tmp_path / "browser-profile"
