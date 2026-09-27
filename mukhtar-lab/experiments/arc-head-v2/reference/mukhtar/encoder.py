"""arc3/mukhtar/encoder.py — вход игрового адаптера «мухи».

feature_vector(features) — плоский числовой вектор фиксированной длины.
Вход адаптера НИКОГДА не сырой кадр 64×64, только объектные признаки
(perception.extract_features) + предыдущее действие + прогресс.
"""
import sys
from pathlib import Path

sys.path.insert(0, '/home/argos-data/improve')
sys.path.insert(0, '/home/argos-data/improve/arc3')

from arc3.perception import feature_vector as _fv  # noqa: E402

VEC_LEN = 5 + 8 + 5 + 12 + 128 + 1 + 1


def feature_vector(features):
    v = _fv(features)
    v = v[:VEC_LEN] + [0.0] * (VEC_LEN - len(v))
    return v
