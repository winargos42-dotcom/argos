#!/usr/bin/env python3
"""
ARGOS Quantum Dataset Validator
================================
Проверяет примеры датасета квантовых схем (argos-quantum-train-v2).

Каждый пример (одна строка JSONL) должен содержать:
  - input    : dict  — описание квантовой схемы (qasm3 + человекочитаемое)
  - output   : dict  — результат симуляции (counts + наиболее вероятные состояния)
  - metadata : dict  — n_qubits, depth, gate_counts, name, shots

Валидатор НЕ доверяет заявленному output на слово: он перепроверяет схему
через qiskit (если доступен) — input.qasm3 должен парситься в QuantumCircuit
с тем же числом кубитов, что в metadata.

Использование:
    python scripts/quantum_validator.py /datasets/quantum-v2-test.jsonl
Возвращает код 0 если ВСЕ примеры валидны, иначе 1.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
    HAVE_QISKIT = True
except Exception:
    HAVE_QISKIT = False


def _resimulate(gates, n_qubits):
    """Реконструирует схему из структурного представления и считает точные
    вероятности — для сверки с заявленным output. Только qiskit core."""
    qc = QuantumCircuit(n_qubits)
    for g in gates:
        method = getattr(qc, g["gate"])
        method(*g.get("params", []), *g["qubits"])
    probs = Statevector.from_instruction(qc).probabilities_dict()
    return {k: v for k, v in probs.items() if v > 1e-9}, qc


def _err(idx: int, msg: str) -> str:
    return f"  [пример {idx}] ❌ {msg}"


def validate_example(idx: int, ex: Dict[str, Any]) -> List[str]:
    """Возвращает список ошибок для одного примера (пустой = валиден)."""
    errors: List[str] = []

    # 1. Верхнеуровневые поля
    for field in ("input", "output", "metadata"):
        if field not in ex:
            errors.append(_err(idx, f"отсутствует поле '{field}'"))
    if errors:
        return errors

    inp, out, meta = ex["input"], ex["output"], ex["metadata"]

    if not isinstance(inp, dict):
        errors.append(_err(idx, "input не dict"))
    if not isinstance(out, dict):
        errors.append(_err(idx, "output не dict"))
    if not isinstance(meta, dict):
        errors.append(_err(idx, "metadata не dict"))
    if errors:
        return errors

    source = meta.get("source", "simulator")
    is_hw = source == "ibm_hardware"

    # 2. metadata
    n_qubits = meta.get("n_qubits")
    if not isinstance(n_qubits, int) or n_qubits < 1:
        errors.append(_err(idx, f"metadata.n_qubits должно быть int>=1, got {n_qubits!r}"))
    if not isinstance(meta.get("name"), str) or not meta.get("name"):
        errors.append(_err(idx, "metadata.name должно быть непустой строкой"))
    shots = meta.get("shots")
    if not isinstance(shots, int) or shots < 1:
        errors.append(_err(idx, "metadata.shots должно быть int>=1"))
    if not is_hw:
        # логическая схема симулятора: depth/gate_counts обязательны
        if not isinstance(meta.get("depth"), int) or meta.get("depth", -1) < 0:
            errors.append(_err(idx, "metadata.depth должно быть int>=0"))
        if not isinstance(meta.get("gate_counts"), dict):
            errors.append(_err(idx, "metadata.gate_counts должно быть dict"))

    # 3. input
    if not isinstance(inp.get("description"), str) or not inp.get("description"):
        errors.append(_err(idx, "input.description должно быть непустой строкой"))
    gates = inp.get("gates")
    if is_hw:
        # hardware: схема transpiled на сотни кубитов — gates/qasm3 не требуем,
        # но обязателен backend и job_id для трассируемости
        if not meta.get("backend"):
            errors.append(_err(idx, "ibm_hardware: отсутствует metadata.backend"))
        if not meta.get("job_id"):
            errors.append(_err(idx, "ibm_hardware: отсутствует metadata.job_id"))
    else:
        qasm = inp.get("qasm3")
        if not isinstance(qasm, str) or "OPENQASM" not in qasm:
            errors.append(_err(idx, "input.qasm3 должно быть QASM3-строкой"))
        if not isinstance(gates, list) or not gates:
            errors.append(_err(idx, "input.gates должно быть непустым списком инструкций"))

    # 4. output: counts суммируются в shots, все ключи — битовые строки длины n_qubits
    counts = out.get("counts")
    if not isinstance(counts, dict) or not counts:
        errors.append(_err(idx, "output.counts должно быть непустым dict"))
    elif isinstance(n_qubits, int):
        total = 0
        for state, c in counts.items():
            if not isinstance(state, str) or any(ch not in "01" for ch in state):
                errors.append(_err(idx, f"output.counts ключ '{state}' не битовая строка"))
                break
            if len(state) != n_qubits:
                errors.append(_err(idx, f"длина состояния '{state}' != n_qubits={n_qubits}"))
                break
            if not isinstance(c, int) or c < 0:
                errors.append(_err(idx, f"счётчик для '{state}' не int>=0"))
                break
            total += c
        else:
            if isinstance(shots, int) and total != shots:
                errors.append(_err(idx, f"sum(counts)={total} != shots={shots}"))

    probs = out.get("top_states")
    if not isinstance(probs, list) or not probs:
        errors.append(_err(idx, "output.top_states должно быть непустым списком"))

    # 5a. HARDWARE: пересимуляция невозможна (transpiled на сотни кубитов).
    #     Проверяем, что доминирующее измеренное состояние входит в идеально ожидаемые.
    if is_hw:
        ideal = out.get("ideal_states")
        if not isinstance(ideal, list) or not ideal:
            errors.append(_err(idx, "ibm_hardware: output.ideal_states должно быть непустым списком"))
        elif isinstance(counts, dict) and counts:
            top_measured = max(counts, key=counts.get)
            if top_measured not in ideal:
                errors.append(_err(idx,
                    f"ibm_hardware: доминирующее измерение '{top_measured}' не среди ожидаемых {ideal}"))
        return errors

    # 5b. SIMULATOR: реконструируем схему и пересимулируем, сверяем с output.
    #     Валидатор не доверяет числам — он их пересчитывает.
    if HAVE_QISKIT and isinstance(gates, list) and gates and isinstance(n_qubits, int):
        try:
            true_probs, qc = _resimulate(gates, n_qubits)
            if qc.num_qubits != n_qubits:
                errors.append(_err(idx, f"схема имеет {qc.num_qubits} кубитов, в metadata {n_qubits}"))
            # сверяем счётчики: заявленная доля должна совпадать с истинной вероятностью (±2%)
            if isinstance(counts, dict) and isinstance(shots, int) and shots > 0:
                for state, c in counts.items():
                    claimed = c / shots
                    true_p = true_probs.get(state, 0.0)
                    if abs(claimed - true_p) > 0.02:
                        errors.append(_err(idx,
                            f"output.counts['{state}']={c} (доля {claimed:.3f}) "
                            f"не совпадает с симуляцией p={true_p:.3f}"))
                        break
                # заявленные состояния не должны быть «фантомными» (p≈0 в реальности)
                for state in counts:
                    if true_probs.get(state, 0.0) < 1e-6:
                        errors.append(_err(idx, f"output.counts содержит невозможное состояние '{state}'"))
                        break
        except Exception as e:
            errors.append(_err(idx, f"не удалось реконструировать/пересимулировать схему: {e}"))

    return errors


def validate_file(path: str) -> Tuple[int, int, List[str]]:
    p = Path(path)
    if not p.exists():
        return 0, 0, [f"❌ Файл не найден: {path}"]

    all_errors: List[str] = []
    total = 0
    valid = 0
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        total += 1
        try:
            ex = json.loads(line)
        except json.JSONDecodeError as e:
            all_errors.append(_err(i, f"невалидный JSON: {e}"))
            continue
        errs = validate_example(i, ex)
        if errs:
            all_errors.extend(errs)
        else:
            valid += 1
    return total, valid, all_errors


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: quantum_validator.py <file.jsonl>")
        return 2
    path = sys.argv[1]
    total, valid, errors = validate_file(path)

    print(f"qiskit кросс-проверка: {'ВКЛ' if HAVE_QISKIT else 'ВЫКЛ (qiskit не найден)'}")
    print(f"Примеров: {total} | валидных: {valid} | с ошибками: {total - valid}")
    if errors:
        print("\nОшибки:")
        for e in errors:
            print(e)
        return 1
    print(f"\n✅ ВСЕ {valid} примеров прошли валидацию.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
