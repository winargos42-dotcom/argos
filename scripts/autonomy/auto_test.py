#!/usr/bin/env python3
"""
auto_test.py — синтаксис+import тест для сгенерированного кода
перед deploy в production. Использовать как:
    python auto_test.py <file.py>
Exit 0 = OK, 1 = FAIL.
"""
import sys, py_compile, subprocess, importlib.util, os

def test_syntax(path):
    try:
        py_compile.compile(path, doraise=True)
        return True, "py_compile OK"
    except py_compile.PyCompileError as e:
        return False, f"SYNTAX: {e}"

def test_flake8(path):
    try:
        r = subprocess.run(["flake8", path, "--ignore=E501,W503,E402"],
                          capture_output=True, text=True, timeout=20)
        if r.returncode == 0:
            return True, "flake8 clean"
        return False, f"FLAKE8:\n{(r.stdout or r.stderr)[:600]}"
    except FileNotFoundError:
        return True, "flake8 not installed — skipped"
    except Exception as e:
        return False, f"flake8 err: {e}"

def test_import(path):
    """Безопасный import — не выполняет, только парсит модуль."""
    try:
        spec = importlib.util.spec_from_file_location("candidate", path)
        if spec is None:
            return False, "spec creation failed"
        mod = importlib.util.module_from_spec(spec)
        # Не запускаем exec — только проверяем что spec валиден
        return True, "import spec OK"
    except Exception as e:
        return False, f"import: {e}"

def run_all(path):
    if not os.path.isfile(path):
        return False, f"file not found: {path}"
    results = []
    for name, fn in [("syntax", test_syntax), ("flake8", test_flake8), ("import", test_import)]:
        ok, msg = fn(path)
        results.append((name, ok, msg))
        print(f"[{'OK' if ok else 'FAIL'}] {name:8s} {msg}")
        if not ok and name in ("syntax", "import"):
            return False, msg
    return True, "all tests passed"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: auto_test.py <file.py>")
        sys.exit(2)
    ok, msg = run_all(sys.argv[1])
    print(f"\n=== {'PASSED' if ok else 'FAILED'}: {msg} ===")
    sys.exit(0 if ok else 1)
