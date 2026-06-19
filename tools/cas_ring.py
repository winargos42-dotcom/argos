"""
Pure-Python wrapper around the C extension `cas_ring`.

If the compiled extension is unavailable, this module falls back to a
reference implementation using `collections.deque` so that callers still
compile and tests can run.
"""

from __future__ import annotations

import struct
import time
from dataclasses import dataclass
from typing import Optional

EVENT_RECORD_FMT = "<QHHIIIq"  # 32 bytes, little-endian
EVENT_RECORD_SIZE = struct.calcsize(EVENT_RECORD_FMT)
assert EVENT_RECORD_SIZE == 32


@dataclass(frozen=True)
class RingEvent:
    ts_ns: int
    ev_type: int
    addr: int
    val_before: int
    val_after: int
    delta_ns: int


class CasRingFallback:
    """Reference deque-based ring buffer used when C extension is absent."""

    _CAPACITY = 256

    def __init__(self) -> None:
        self._buf: list[RingEvent] = []

    def enqueue(self, ts_ns: int, ev_type: int, addr: int,
                val_before: int, val_after: int, delta_ns: int) -> None:
        if len(self._buf) >= self._CAPACITY:
            raise CasRingError("ring full")
        self._buf.append(RingEvent(ts_ns, ev_type, addr,
                                   val_before, val_after, delta_ns))

    def dequeue(self) -> Optional[RingEvent]:
        if not self._buf:
            return None
        return self._buf.pop(0)

    def capacity(self) -> int:
        return self._CAPACITY


# Try to import the compiled extension; otherwise use the fallback.
try:
    try:
        import cas_ring as _cr  # type: ignore[import]
    except Exception:
        _cr = None  # type: ignore[assignment]

    if _cr is not None:
        class CasRing:
            def __init__(self) -> None:
                self._ring = _cr.CasRing()

            def enqueue(self, ts_ns: int, ev_type: int, addr: int,
                        val_before: int, val_after: int, delta_ns: int) -> None:
                try:
                    self._ring.enqueue(ts_ns, ev_type, addr,
                                       val_before, val_after, delta_ns)
                except _cr.CasRingError as exc:
                    raise CasRingError("ring full") from exc

            def dequeue(self) -> Optional[RingEvent]:
                try:
                    raw = self._ring.dequeue()
                except _cr.CasRingError:
                    return None
                if raw is None:
                    return None
                return RingEvent(
                    ts_ns=raw[0],
                    ev_type=raw[1],
                    addr=raw[2],
                    val_before=raw[3],
                    val_after=raw[4],
                    delta_ns=raw[5],
                )

            def capacity(self) -> int:
                return int(self._ring.capacity())
    else:
        CasRing = CasRingFallback  # type: ignore[misc, assignment]

    class CasRingError(Exception):
        """Raised when the ring is full."""
        pass
except Exception:
    CasRing = CasRingFallback  # type: ignore[misc, assignment]

    class CasRingError(Exception):  # type: ignore[no-redef]
        """Raised when the ring is full."""
        pass


def pack_event(ev: RingEvent) -> bytes:
    return struct.pack(
        EVENT_RECORD_FMT,
        ev.ts_ns,
        ev.ev_type,
        0,  # reserved
        ev.addr,
        ev.val_before,
        ev.val_after,
        ev.delta_ns,
    )


def unpack_event(data: bytes) -> RingEvent:
    if len(data) != EVENT_RECORD_SIZE:
        raise ValueError(f"expected {EVENT_RECORD_SIZE} bytes, got {len(data)}")
    ts_ns, ev_type, _reserved, addr, val_before, val_after, delta_ns = struct.unpack(
        EVENT_RECORD_FMT, data
    )
    return RingEvent(ts_ns, ev_type, addr, val_before, val_after, delta_ns)


if __name__ == "__main__":
    ring = CasRing()
    print("capacity:", ring.capacity())
    ring.enqueue(
        ts_ns=time.perf_counter_ns(),
        ev_type=1,
        addr=0x1000,
        val_before=0,
        val_after=1,
        delta_ns=500,
    )
    ev = ring.dequeue()
    print("event:", ev)
    print("packed:", pack_event(ev).hex())
