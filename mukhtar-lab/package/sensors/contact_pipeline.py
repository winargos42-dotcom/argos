from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Mapping

import numpy as np


@dataclass(slots=True)
class ContactSignal:
    active: bool = False
    normal_force: float = 0.0
    tangential_force: float = 0.0
    duration_s: float = 0.0
    position: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float32))
    normal: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float32))
    contact_count: int = 0
    # классификация последнего значимого контакта: floor / obstacle / none
    kind: str = "none"
    pair: tuple[str, str] = ()

    def copy(self) -> "ContactSignal":
        return ContactSignal(
            active=self.active,
            normal_force=self.normal_force,
            tangential_force=self.tangential_force,
            duration_s=self.duration_s,
            position=self.position.copy(),
            normal=self.normal.copy(),
            contact_count=self.contact_count,
            kind=self.kind,
            pair=self.pair,
        )


ForceReader = Callable[[object, object, int], np.ndarray]


class ContactPipeline:
    """Convert MuJoCo contacts into stable per-leg/per-part reflex signals.

    ``geom_map`` maps MuJoCo geom IDs to ``(leg_index, part_name)``.  Track
    foot and tibia separately, for example::

        {foot_geom_id: (0, "foot"), tibia_geom_id: (0, "tibia")}

    Durations are accumulated in physical seconds using the controller's
    actual ``dt``.  Leg-to-leg contacts are ignored by default so they do not
    masquerade as terrain contacts.
    """

    def __init__(
        self,
        *,
        model: object,
        geom_map: Mapping[int, tuple[int, str]],
        dt: float,
        force_reader: ForceReader | None = None,
        ignore_leg_leg: bool = True,
        kind_by_geom: Mapping[int, str] | None = None,
        name_reader: Callable[[int], str] | None = None,
    ) -> None:
        if dt <= 0.0 or not np.isfinite(dt):
            raise ValueError("dt must be finite and > 0")
        if not geom_map:
            raise ValueError("geom_map must not be empty")

        self.model = model
        self.geom_map = {int(k): (int(v[0]), str(v[1])) for k, v in geom_map.items()}
        self.dt = float(dt)
        self.ignore_leg_leg = bool(ignore_leg_leg)
        self.force_reader = force_reader or self._mujoco_force_reader
        self._kind_by_geom = ({int(k): str(v) for k, v in kind_by_geom.items()}
                              if kind_by_geom else {})
        self._name_reader = name_reader or (
            lambda gid: self._mujoco_name_reader(model, gid))

        self._keys = sorted(set(self.geom_map.values()))
        self._duration = {key: 0.0 for key in self._keys}
        # самоконтакты не выбрасываются — логируются отдельно (для safety)
        self.last_self_pairs: list[tuple[str, str]] = []
        self.self_total: int = 0

    @staticmethod
    def _mujoco_name_reader(model: object, gid: int) -> str:
        try:
            import mujoco
            name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, gid)
            return str(name) if name is not None else str(gid)
        except Exception:  # тестовый фейк-модель / не-MjModel
            return str(gid)

    @staticmethod
    def _mujoco_force_reader(model: object, data: object, contact_index: int) -> np.ndarray:
        try:
            import mujoco
        except ImportError as exc:  # pragma: no cover - depends on target runtime
            raise RuntimeError("MuJoCo is required when force_reader is not supplied") from exc

        wrench = np.zeros(6, dtype=np.float64)
        mujoco.mj_contactForce(model, data, contact_index, wrench)
        return wrench

    def reset(self) -> None:
        for key in self._duration:
            self._duration[key] = 0.0
        self.last_self_pairs = []
        self.self_total = 0

    def update(self, data: object) -> dict[int, dict[str, ContactSignal]]:
        accum: dict[tuple[int, str], ContactSignal] = {
            key: ContactSignal() for key in self._keys
        }
        self.last_self_pairs = []
        kind_rank = {"floor": 1, "obstacle": 2}

        ncon = int(getattr(data, "ncon"))
        for ci in range(ncon):
            contact = data.contact[ci]
            g1 = int(contact.geom1)
            g2 = int(contact.geom2)
            k1 = self.geom_map.get(g1)
            k2 = self.geom_map.get(g2)

            if k1 is None and k2 is None:
                continue
            if self.ignore_leg_leg and k1 is not None and k2 is not None:
                # самоконтакт: не в сигналы, но в отдельный лог
                n1 = self._name_reader(g1)
                n2 = self._name_reader(g2)
                self.last_self_pairs.append((n1, n2))
                self.self_total += 1
                continue

            targets = [key for key in (k1, k2) if key is not None]
            wrench = np.asarray(self.force_reader(self.model, data, ci), dtype=np.float64)
            if wrench.shape != (6,):
                raise ValueError("force_reader must return a 6-vector")

            normal_force = max(0.0, float(wrench[0]))
            tangential_force = float(np.hypot(wrench[1], wrench[2]))
            pos = np.asarray(contact.pos, dtype=np.float32).reshape(3)
            frame = np.asarray(contact.frame, dtype=np.float32).reshape(3, 3)
            normal = frame[0].copy()

            # классификация: kind партнёра (робот-части здесь уже отсечены)
            if k1 is not None:
                other_gid, other_key = g2, k2
            else:
                other_gid, other_key = g1, k1
            kind = self._kind_by_geom.get(other_gid, "obstacle")
            n1 = self._name_reader(g1)
            n2 = self._name_reader(g2)
            pair = (n1, n2)

            for key in targets:
                signal = accum[key]
                signal.active = True
                signal.normal_force += normal_force
                signal.tangential_force += tangential_force
                signal.contact_count += 1
                # приоритет kind: obstacle > floor (важнее для рефлексов)
                if kind_rank.get(kind, 0) >= kind_rank.get(signal.kind, 0):
                    signal.kind = kind
                    signal.pair = pair

                # Force-weighted position/normal is useful when multiple contact
                # points exist. Fall back to equal weighting for zero normal force.
                weight = normal_force if normal_force > 0.0 else 1.0
                if not hasattr(signal, "_weight_sum"):
                    # slots dataclass cannot accept temporary fields; accumulate
                    # by averaging incrementally instead.
                    pass
                n = float(signal.contact_count)
                signal.position += (pos - signal.position) / n
                signal.normal += (normal - signal.normal) / n

        for key, signal in accum.items():
            if signal.active:
                self._duration[key] += self.dt
                signal.duration_s = self._duration[key]
                norm = float(np.linalg.norm(signal.normal))
                if norm > 1e-8:
                    signal.normal /= norm
            else:
                self._duration[key] = 0.0
                signal.duration_s = 0.0

        result: dict[int, dict[str, ContactSignal]] = {}
        for (leg, part), signal in accum.items():
            result.setdefault(leg, {})[part] = signal.copy()
        return result
