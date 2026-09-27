import json
import time
from types import SimpleNamespace as NS

import pytest

from src.execution_outcome import classify_execution
from src.network_runtime import NetworkRuntime, encode_request
from src.task_runtime import TaskRunner


LOCAL = "6e5e1e1f-1c33-4173-8158-2ae39d0875cb"


@pytest.mark.parametrize("answer", [
    "✅ Готово",
    "🏠 Ответ о доме",
    "📷 Какую камеру открыть?",
    "🔒 Обещание зашифровать файл",
    "запомнил",
])
def test_decorated_text_does_not_prove_execution(answer):
    assert classify_execution(answer) == (answer, "unverified")


@pytest.mark.parametrize("answer", [
    "🏠 Home Assistant сейчас недоступен — не могу получить состояние дома.",
    "📷 Камера не дала кадр (занята или отключена).",
    "📷 Не удалось сжать кадр.",
    "📡 Рой: шина недоступна (connection timeout)",
])
def test_known_unavailable_outputs_are_failed(answer):
    assert classify_execution(answer) == (answer, "failed")


@pytest.mark.parametrize("status", ["succeeded", "failed", "unverified"])
@pytest.mark.parametrize("answer", ["✅ Готово", "Ошибка: строка из прочитанного журнала"])
def test_explicit_outcome_is_not_replaced_by_answer_wording(status, answer):
    assert classify_execution({"answer": answer, "execution_status": status}) == (answer, status)


@pytest.mark.parametrize("answer", [None, "", "   "])
def test_empty_answer_is_not_confirmed_even_with_success_status(answer):
    assert classify_execution({"answer": answer, "execution_status": "succeeded"})[1] == "failed"


def make_runtime(result):
    skill = NS(runtime=NS(handle=lambda text: result),
               manifest=NS(name="Example", version="1", permissions=set()))
    core = NS(p2p=NS(profile=NS(node_id=LOCAL, role="gateway"),
                     bind_host="127.0.0.1", registry=NS(all=lambda: []), _running=False),
              skill_loader=NS(_skills={"example": skill}, _failed={}))
    return NetworkRuntime(core, lambda text: "unexpected fallback", ready=lambda: True,
                          coral=None, guard=NS(evaluate=lambda *args, **kwargs: NS(allowed=True)))


def selected_request(runtime):
    catalog = runtime.actions(LOCAL, "skills")
    return dict(request_id="b" * 32, node=LOCAL, action=catalog["items"][0]["id"],
                revision=catalog["revision"], text="status")


@pytest.mark.parametrize("status", ["succeeded", "failed", "unverified"])
def test_selected_dispatch_preserves_explicit_execution_status(status):
    result = {"answer": "✅ Обработанный результат", "execution_status": status}
    runtime = make_runtime(result)
    assert runtime.dispatch(encode_request(selected_request(runtime))) == result


def test_unknown_selected_command_returns_unverified_hint():
    runtime = make_runtime(None)
    result = runtime.dispatch(encode_request(selected_request(runtime)))
    assert result["answer"]
    assert result["execution_status"] == "unverified"


def test_real_core_status_function_remains_confirmed():
    runtime = make_runtime("unused")
    result = runtime._function({"node": LOCAL, "action": "core.status", "text": ""})
    answer, status = classify_execution(result)
    assert status == "succeeded"
    assert json.loads(answer) == {"node": LOCAL, "ready": True, "core": "ARGOS"}


@pytest.mark.parametrize(("raw", "task_status", "execution_status"), [
    ("🏠 Home Assistant сейчас недоступен — не могу получить состояние дома.", "failed", "failed"),
    ("📷 Камера не дала кадр (занята или отключена).", "failed", "failed"),
    ({"answer": "✅ Только текст", "execution_status": "unverified"}, "completed", "unverified"),
    ({"answer": '{"ready": true}', "execution_status": "succeeded"}, "completed", "succeeded"),
])
def test_persisted_task_outcome_matches_actual_result(tmp_path, raw, task_status, execution_status):
    runner = TaskRunner(tmp_path / "tasks.sqlite3", lambda text: raw)
    try:
        task = runner.submit("offline outcome regression")
        deadline = time.monotonic() + 3
        while True:
            task = runner.get(task["id"])
            if task["status"] not in {"queued", "running"}:
                break
            assert time.monotonic() < deadline, "Test task did not finish"
            time.sleep(0.01)
        assert task["status"] == task_status
        assert task["execution_status"] == execution_status
    finally:
        runner.close()
