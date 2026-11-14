#!/usr/bin/env python3
"""message_auth.py — HMAC-аутентификация сообщений канала VIBE <-> ARGOS X230.

Закрывает главное ограничение публичного транспорта (x0.at + ntfy): SHA256
подтверждает целостность, но не личность отправителя. Этот модуль добавляет
HMAC-SHA256 подпись конверта по каноническому JSON.

Ключ: переменная окружения ARGOS_LINK_SECRET (hex, 32+ байт). Ключ НИКОГДА
не пишется в файлы, логи и публичные каналы; передаётся только владельцем
в обе стороны вне публичного транспорта (чат с владельцем / консоль X230).
key_id = первые 8 hex-символов SHA256(ключа) — позволяет сторонам убедиться,
что используют один ключ, не раскрывая сам ключ.

Верификация: constant-time сравнение; конверт без auth, с чужим key_id или
неверной подписью отклоняется. Подписывается весь конверт КРОМЕ поля auth.

CLI:
    python message_auth.py --selftest
    python message_auth.py --sign file.json      # подписать на месте
    python message_auth.py --verify file.json    # проверить, rc 0/1
"""

import copy
import hashlib
import hmac
import json
import os
import re
import sys

ALG = "hmac-sha256"


def load_key() -> bytes:
    key = os.getenv("ARGOS_LINK_SECRET", "").strip()
    if not key:
        raise RuntimeError("ARGOS_LINK_SECRET is not set; refusing unsigned operation")
    if not re.fullmatch(r"[0-9a-fA-F]{64}", key):
        raise RuntimeError("ARGOS_LINK_SECRET must contain 32 random bytes as 64 hex characters")
    return key.encode("ascii")


def key_id(key: bytes) -> str:
    return hashlib.sha256(key).hexdigest()[:8]


def canonical_bytes(obj: dict) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def sign_envelope(env: dict, key: bytes, key_id_label: str | None = None) -> dict:
    signed = copy.deepcopy(env)
    signed.pop("auth", None)
    sig = hmac.new(key, canonical_bytes(signed), hashlib.sha256).hexdigest()
    signed["auth"] = {"alg": ALG, "key_id": key_id_label or key_id(key), "sig": sig}
    return signed


def verify_envelope(env: dict, key: bytes) -> tuple[bool, str]:
    auth = env.get("auth")
    if not isinstance(auth, dict):
        return False, "missing auth block"
    if auth.get("alg") != ALG:
        return False, f"unsupported alg: {auth.get('alg')}"
    if auth.get("key_id") != key_id(key):
        return False, "key_id mismatch (different key on peer)"
    body = copy.deepcopy(env)
    body.pop("auth", None)
    expected = hmac.new(key, canonical_bytes(body), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, str(auth.get("sig", ""))):
        return False, "signature mismatch"
    return True, "ok"


def self_test() -> bool:
    key = b"0123456789abcdef0123456789abcdef"
    env = {"msg_id": "test", "type": "selftest", "n": 1}
    s = sign_envelope(env, key)
    ok, _ = verify_envelope(s, key)
    tampered = copy.deepcopy(s)
    tampered["n"] = 2
    ok_t, _ = verify_envelope(tampered, key)
    forged = copy.deepcopy(s)
    forged["auth"]["sig"] = "0" * 64
    ok_f, _ = verify_envelope(forged, key)
    noauth, _ = verify_envelope({"msg_id": "x"}, key)
    foreign, _ = verify_envelope(s, b"abcdef0123456789abcdef0123456789")
    return ok and not ok_t and not ok_f and not noauth and not foreign


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "--selftest"
    if cmd == "--selftest":
        result = self_test()
        print("selftest:", "PASS" if result else "FAIL")
        return 0 if result else 1
    key = load_key()
    path = sys.argv[2]
    with open(path, encoding="utf-8") as f:
        env = json.load(f)
    if cmd == "--sign":
        env = sign_envelope(env, key)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(env, f, ensure_ascii=False, indent=2)
        print(f"signed with key_id={key_id(key)}")
        return 0
    if cmd == "--verify":
        ok, why = verify_envelope(env, key)
        print(f"{path}: {'AUTHENTIC' if ok else 'REJECTED'} ({why})")
        return 0 if ok else 1
    print(f"unknown command {cmd}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
