import pytest
from src.skills import budding


@pytest.mark.parametrize('missing', ['NO_MODEL', 'NO_ENTRYPOINT', 'NO_CONFIG', 'NO_PYTHON'])
def test_missing_inference_artifact_is_unavailable_without_invented_training(missing,monkeypatch):
    calls=[]
    def ssh(command):
        calls.append(command)
        return missing+'\nactive',''
    monkeypatch.setattr(budding,'_ssh',ssh)
    answer=budding.Budding()._snn_say('fixture','hello')
    assert len(calls)==1 and 'systemd-run' not in calls[0]
    assert 'недоступен' in answer
    assert '1000' not in answer and 'дообуч' not in answer and 'растёт' not in answer


def test_unknown_or_failed_preflight_never_starts_inference(monkeypatch):
    calls=[]
    def ssh(command): calls.append(command);return '', 'offline'
    monkeypatch.setattr(budding,'_ssh',ssh)
    answer=budding.Budding()._snn_say('fixture','hello')
    assert len(calls)==1 and 'недоступен' in answer


def test_complete_preflight_with_missing_service_is_explicit_unavailable(monkeypatch):
    calls=[]
    def ssh(command):
        calls.append(command)
        return 'MODEL_OK\nENTRYPOINT_OK\nCONFIG_OK\nPYTHON_OK\nNO_SERVICE',''
    monkeypatch.setattr(budding,'_ssh',ssh)
    answer=budding.Budding()._snn_say('fixture','hello')
    assert len(calls)==1 and 'недоступен' in answer and 'сервис' in answer


def test_files_alone_do_not_prove_checkpoint_entrypoint_compatibility(monkeypatch):
    calls=[]
    def ssh(command):
        calls.append(command)
        return 'MODEL_OK\nENTRYPOINT_OK\nCONFIG_OK\nPYTHON_OK\nactive',''
    monkeypatch.setattr(budding,'_ssh',ssh)
    answer=budding.Budding()._snn_say('fixture','hello')
    assert len(calls)==1 and 'совместимость' in answer and 'недоступен' in answer
