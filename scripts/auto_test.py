#!/usr/bin/env python3
"""
ARGOS Auto-Test — проверяет сгенерённый код перед деплоем.
Ели pass → ставит .TESTED, fail → .FAIL + причина.
"""
import subprocess, os, re, json, sys, py_compile
from pathlib import Path
from datetime import datetime

TASK_DIR = Path("/tmp/metagpt_tasks")
REPORT_DIR = Path("/home/ava/Projects/argoss/data/mempalace")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def run_syntax_test(file_path):
    """py_compile + flake8 как у пользователя."""
    errors = []
    try:
        py_compile.compile(file_path, doraise=True)
    except py_compile.PyCompileError as e:
        errors.append(f"SYNTAX: {e}")
    try:
        result = subprocess.run(
            ["flake8", file_path, "--ignore=E501,W503"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0 and ("E9" in result.stdout or "F8" in result.stdout):
            errors.append(f"FLAKE8: {result.stdout[:300]}")
    except FileNotFoundError:
        pass
    return len(errors) == 0, errors

def test_file(py_file: Path) -> dict:
    result = {"file": str(py_file), "passed": True, "errors": [], "ts": datetime.now().isoformat()}
    ok, errs = run_syntax_test(str(py_file))
    if not ok:
        result["passed"] = False
        result["errors"] = errs
    return result

def run_all_tests(cmd_file=None):
    results = []
    files = [Path(cmd_file)] if cmd_file else sorted(TASK_DIR.glob("*.py"))
    for f in files:
        if f.suffix != ".py" or any(s in f.name for s in [".APPROVED",".TESTED",".FAIL"]):
            continue
        print(f"[AutoTest] Testing {f.name}...")
        res = test_file(f)
        results.append(res)
        if res["passed"]:
            tested = f.with_suffix(".py.TESTED")
            f.rename(tested)
            print(f"  ✅ PASS → {tested.name}")
        else:
            fail = f.with_suffix(".py.FAIL")
            fail.write_text(json.dumps(res, ensure_ascii=False, indent=2))
            f.unlink()
            print(f"  ❌ FAIL → {fail.name}: {res['errors'][0][:80]}")
    report = REPORT_DIR / "auto_test_report.json"
    report.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"[AutoTest] Report: {report}")
    return results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        results = run_all_tests(cmd_file=sys.argv[1])
        sys.exit(0 if all(r["passed"] for r in results) else 1)
    else:
        run_all_tests()
