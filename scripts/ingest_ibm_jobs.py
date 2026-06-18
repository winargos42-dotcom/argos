#!/usr/bin/env python3
"""
ARGOS — импорт реальных IBM Quantum job'ов в датасет argos-quantum-train-v2.
============================================================================
Декодирует job-*-info.json / job-*-result.json (формат qiskit_ibm_runtime),
извлекает измеренные counts с КВАНТОВОГО ЖЕЛЕЗА (backend ibm_fez) и
дописывает их в JSONL как примеры с source="ibm_hardware".

В отличие от симулятора, output здесь — реальные измерения с шумом NISQ,
поэтому пересимуляция невозможна (схема transpiled на 156 кубитов).

Запуск:
    python scripts/ingest_ibm_jobs.py --src "<dir>" --out /datasets/quantum-v2-test.jsonl --append
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import warnings
from pathlib import Path
from typing import Dict, List

warnings.filterwarnings("ignore")
from qiskit_ibm_runtime.utils import RuntimeDecoder


def classify(counts: Dict[str, int]) -> Dict:
    """Эвристика по наблюдаемым counts: каких состояний ожидать идеально."""
    n = len(next(iter(counts)))
    total = sum(counts.values())
    fracs = {k: v / total for k, v in counts.items()}
    if n == 1:
        return {"kind": "superposition_1q",
                "ideal_states": ["0", "1"],
                "desc": "Суперпозиция одного кубита на ibm_fez: ожидается ~50/50 |0⟩ и |1⟩."}
    # 2 кубита: коррелированы ли (00/11 доминируют) → состояние Белла
    corr = fracs.get("00", 0) + fracs.get("11", 0)
    if corr > 0.8:
        return {"kind": "bell_entangled",
                "ideal_states": ["00", "11"],
                "desc": "Состояние Белла на ibm_fez: запутанная пара, |00⟩ и |11⟩ доминируют; "
                        "|01⟩/|10⟩ — шум NISQ-железа."}
    return {"kind": "generic",
            "ideal_states": list(counts.keys()),
            "desc": f"Результат {n}-кубитной схемы на ibm_fez."}


def extract_counts(res) -> Dict[str, int]:
    pr = res.pub_results[0] if hasattr(res, "pub_results") else res[0]
    data = pr.data
    # имя поля измерений: разные версии qiskit отдают по-разному
    if hasattr(data, "field_names") and data.field_names:
        fname = data.field_names[0]
    else:
        fname = next(iter(vars(data)))
    ba = getattr(data, fname) if hasattr(data, fname) else data[fname]
    return {k: int(v) for k, v in ba.get_counts().items()}


def build_example(info: Dict, counts: Dict[str, int], qc=None) -> Dict:
    n_qubits = len(next(iter(counts)))
    total = sum(counts.values())
    cls = classify(counts)
    transpiled = {}
    if qc is not None:
        transpiled = {
            "transpiled_qubits": qc.num_qubits,
            "transpiled_depth": qc.depth(),
            "transpiled_gate_counts": {k: int(v) for k, v in qc.count_ops().items()},
        }
    top_states = sorted(
        ({"state": k, "probability": round(v / total, 6)} for k, v in counts.items()),
        key=lambda d: d["probability"], reverse=True,
    )
    return {
        "input": {
            "description": cls["desc"],
            "backend": info.get("backend"),
            "circuit_kind": cls["kind"],
        },
        "output": {
            "counts": counts,
            "top_states": top_states,
            "ideal_states": cls["ideal_states"],
        },
        "metadata": {
            "n_qubits": n_qubits,
            "name": f"{cls['kind']}_{info['id'][:8]}",
            "shots": total,
            "source": "ibm_hardware",
            "backend": info.get("backend"),
            "job_id": info.get("id"),
            "created": info.get("created"),
            "cost": info.get("cost"),
            **transpiled,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="директория с job-*-info/result.json")
    ap.add_argument("--out", default="/datasets/quantum-v2-test.jsonl")
    ap.add_argument("--append", action="store_true")
    args = ap.parse_args()

    examples: List[Dict] = []
    for info_path in sorted(glob.glob(os.path.join(args.src, "job-*-info.json"))):
        res_path = info_path.replace("-info.json", "-result.json")
        if not os.path.exists(res_path):
            print(f"  ⚠️ нет result для {info_path}")
            continue
        with open(info_path) as f:
            info = json.load(f, cls=RuntimeDecoder)
        with open(res_path) as f:
            res = json.load(f, cls=RuntimeDecoder)
        counts = extract_counts(res)
        qc = info.get("params", {}).get("pubs", [[None]])[0][0]
        ex = build_example(info, counts, qc)
        examples.append(ex)
        m = ex["metadata"]
        print(f"  + {m['name']:28} backend={m['backend']} qubits={m['n_qubits']} "
              f"shots={m['shots']} counts={counts}")

    out = Path(args.out)
    mode = "a" if args.append else "w"
    with out.open(mode, encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    print(f"\n✅ {'Добавлено' if args.append else 'Записано'} {len(examples)} hardware-примеров → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
