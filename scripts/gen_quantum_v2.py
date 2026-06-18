#!/usr/bin/env python3
"""
ARGOS Quantum Dataset Generator v2
===================================
Генерирует примеры для argos-quantum-train-v2: реальные квантовые схемы,
симулированные через qiskit. output — ФАКТ симуляции, а не выдумка.

Формат примера (JSONL):
  {
    "input":  {"qasm3": "<OPENQASM 3.0 ...>", "description": "..."},
    "output": {"counts": {"00": 512, "11": 512}, "top_states": [...], "statevector_norm": 1.0},
    "metadata": {"n_qubits": 2, "depth": 2, "gate_counts": {...}, "name": "bell_phi_plus", "shots": 1024}
  }

Запуск:
    python scripts/gen_quantum_v2.py --n 10 --out /datasets/quantum-v2-test.jsonl
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

from qiskit import QuantumCircuit
from qiskit.qasm3 import dumps as qasm3_dumps
from qiskit.quantum_info import Statevector

QUANTUM_SEED = 3233339492  # IBM genesis seed


# ── Конструкторы схем (без измерений; measure добавляется при симуляции) ──
def bell() -> Tuple[QuantumCircuit, str]:
    qc = QuantumCircuit(2, name="bell_phi_plus")
    qc.h(0); qc.cx(0, 1)
    return qc, "Состояние Белла Φ+: запутанная пара, ожидаются только |00⟩ и |11⟩ по 50%."


def ghz(n: int = 3) -> Tuple[QuantumCircuit, str]:
    qc = QuantumCircuit(n, name=f"ghz_{n}q")
    qc.h(0)
    for i in range(n - 1):
        qc.cx(i, i + 1)
    return qc, f"GHZ-состояние на {n} кубитах: максимальная запутанность, только |0...0⟩ и |1...1⟩."


def uniform_superposition(n: int = 2) -> Tuple[QuantumCircuit, str]:
    qc = QuantumCircuit(n, name=f"hadamard_uniform_{n}q")
    for i in range(n):
        qc.h(i)
    return qc, f"Равномерная суперпозиция: {n} гейтов Адамара, все 2^{n} состояний равновероятны."


def qft(n: int = 3) -> Tuple[QuantumCircuit, str]:
    qc = QuantumCircuit(n, name=f"qft_{n}q")
    for j in range(n):
        qc.h(j)
        for k in range(j + 1, n):
            qc.cp(math.pi / float(2 ** (k - j)), k, j)
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    return qc, f"Квантовое преобразование Фурье на {n} кубитах (входное состояние |0...0⟩)."


def deutsch_balanced() -> Tuple[QuantumCircuit, str]:
    # Алгоритм Дойча для сбалансированной функции f(x)=x → должен дать |1> на первом кубите
    qc = QuantumCircuit(2, name="deutsch_balanced")
    qc.x(1); qc.h(0); qc.h(1)
    qc.cx(0, 1)            # оракул f(x)=x
    qc.h(0)
    return qc, "Алгоритм Дойча, сбалансированная f(x)=x: первый кубит должен измериться в |1⟩."


def grover_2q() -> Tuple[QuantumCircuit, str]:
    # Гровер на 2 кубита, помеченное состояние |11>
    qc = QuantumCircuit(2, name="grover_2q_mark11")
    qc.h(0); qc.h(1)
    qc.cz(0, 1)                       # оракул помечает |11>
    qc.h(0); qc.h(1)                  # диффузор
    qc.x(0); qc.x(1)
    qc.cz(0, 1)
    qc.x(0); qc.x(1)
    qc.h(0); qc.h(1)
    return qc, "Алгоритм Гровера на 2 кубита, цель |11⟩: одна итерация даёт ~100% на |11⟩."


def phase_kickback() -> Tuple[QuantumCircuit, str]:
    qc = QuantumCircuit(2, name="phase_kickback")
    qc.x(1); qc.h(0); qc.h(1)
    qc.cx(0, 1)
    qc.h(0)
    return qc, "Демонстрация phase kickback через CNOT в базисе Адамара."


def w_state_3q() -> Tuple[QuantumCircuit, str]:
    # W-состояние на 3 кубита: (|100>+|010>+|001>)/sqrt(3)
    qc = QuantumCircuit(3, name="w_state_3q")
    theta = 2 * math.acos(1 / math.sqrt(3))
    qc.ry(theta, 0)
    qc.ch(0, 1)
    qc.cx(1, 2)
    qc.cx(0, 1)
    qc.x(0)
    return qc, "W-состояние на 3 кубита: ровно один кубит в |1⟩, три равновероятных исхода."


def bell_psi_minus() -> Tuple[QuantumCircuit, str]:
    qc = QuantumCircuit(2, name="bell_psi_minus")
    qc.x(0); qc.h(0); qc.cx(0, 1); qc.z(0)
    return qc, "Состояние Белла Ψ-: антикоррелированная пара, только |01⟩ и |10⟩."


def entangled_chain_4q() -> Tuple[QuantumCircuit, str]:
    qc = QuantumCircuit(4, name="entangled_chain_4q")
    qc.h(0)
    qc.cx(0, 1); qc.cx(1, 2); qc.cx(2, 3)
    return qc, "Цепочка запутывания на 4 кубита (линейный GHZ): только |0000⟩ и |1111⟩."


BUILDERS = [
    bell, ghz, uniform_superposition, qft, deutsch_balanced,
    grover_2q, phase_kickback, w_state_3q, bell_psi_minus, entangled_chain_4q,
]


def simulate(qc: QuantumCircuit, shots: int) -> Dict:
    """Реальная симуляция: точные вероятности из Statevector + сэмплирование counts."""
    sv = Statevector.from_instruction(qc)
    probs = sv.probabilities_dict()  # ключи — битовые строки длины n_qubits
    # qiskit отдаёт ключи в порядке q_{n-1}...q_0; нормализуем чистку малых хвостов
    probs = {k: v for k, v in probs.items() if v > 1e-9}

    # детерминированный сэмплинг counts по вероятностям (округление с коррекцией суммы)
    raw = {k: v * shots for k, v in probs.items()}
    counts = {k: int(round(v)) for k, v in raw.items()}
    diff = shots - sum(counts.values())
    if counts and diff != 0:
        # корректируем самый вероятный исход, чтобы сумма == shots
        top = max(counts, key=lambda k: probs[k])
        counts[top] += diff
    counts = {k: v for k, v in counts.items() if v > 0}

    top_states = sorted(
        ({"state": k, "probability": round(p, 6)} for k, p in probs.items()),
        key=lambda d: d["probability"], reverse=True,
    )[:8]

    return {
        "counts": counts,
        "top_states": top_states,
        "statevector_norm": round(float(sum(probs.values())), 6),
    }


def extract_gates(qc: QuantumCircuit) -> List[Dict]:
    """Структурное представление схемы — позволяет валидатору реконструировать её
    без внешних QASM-парсеров (qiskit core достаточно)."""
    gates: List[Dict] = []
    for instr in qc.data:
        op = instr.operation
        qubits = [qc.find_bit(q).index for q in instr.qubits]
        gates.append({
            "gate": op.name,
            "qubits": qubits,
            "params": [float(p) for p in op.params],
        })
    return gates


def build_example(builder, shots: int) -> Dict:
    qc, desc = builder()
    sim = simulate(qc, shots)
    gate_counts = {k: int(v) for k, v in qc.count_ops().items()}
    return {
        "input": {
            "qasm3": qasm3_dumps(qc),
            "gates": extract_gates(qc),
            "description": desc,
        },
        "output": sim,
        "metadata": {
            "n_qubits": qc.num_qubits,
            "depth": qc.depth(),
            "gate_counts": gate_counts,
            "name": qc.name,
            "shots": shots,
            "seed": QUANTUM_SEED,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--shots", type=int, default=1024)
    ap.add_argument("--out", default="/datasets/quantum-v2-test.jsonl")
    args = ap.parse_args()

    builders = (BUILDERS * ((args.n // len(BUILDERS)) + 1))[: args.n]
    examples = [build_example(b, args.shots) for b in builders]

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    print(f"✅ Сгенерировано {len(examples)} примеров → {out}")
    for ex in examples:
        m = ex["metadata"]
        top = ex["output"]["top_states"][0]
        print(f"  {m['name']:22} qubits={m['n_qubits']} depth={m['depth']} "
              f"top=|{top['state']}⟩ p={top['probability']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
