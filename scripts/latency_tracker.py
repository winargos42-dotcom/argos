"""LatencyTracker — атомарный замер задержек (рекомендован Claude TG)"""
from dataclasses import dataclass
from time import perf_counter
from typing import Optional
import traceback


@dataclass
class LatencyBreakdown:
    cycle_id: str
    provider_used: Optional[str]
    attempt_index: int
    latency_provider_request_ms: int
    latency_api_call_ms: int
    postprocess_ms: int
    outcome: str          # success|timeout|error|fallback
    fail_reason: Optional[str]
    retry_count: int

    def to_log_dict(self) -> dict:
        return {
            "cycle": self.cycle_id,
            "provider": self.provider_used,
            "attempt": self.attempt_index,
            "api_ms": self.latency_api_call_ms,
            "post_ms": self.postprocess_ms,
            "outcome": self.outcome,
            "fail": self.fail_reason,
            "retries": self.retry_count,
        }


class LatencyTracker:
    """
    Контракт (non-stream):
    - latency_api_call_ms: mark_start_http → mark_body_done
    - postprocess_ms: mark_body_done → mark_postprocess_done
    """
    def __init__(self, *, cycle_id: str, provider_used: Optional[str],
                 attempt_index: int = 0, retry_count: int = 0):
        self.cycle_id = cycle_id
        self.provider_used = provider_used
        self.attempt_index = attempt_index
        self.retry_count = retry_count
        self._t0: Optional[float] = None
        self._t_body: Optional[float] = None
        self._t_post: Optional[float] = None
        self._outcome = "success"
        self._fail_reason: Optional[str] = None

    def mark_start_http(self) -> None:
        self._t0 = perf_counter()

    def mark_body_done(self) -> None:
        self._t_body = perf_counter()

    def mark_postprocess_done(self) -> None:
        self._t_post = perf_counter()

    def mark_outcome(self, *, outcome: str, fail_reason: Optional[str] = None,
                     exc: Optional[BaseException] = None) -> None:
        self._outcome = outcome
        self._fail_reason = fail_reason
        if exc is not None and fail_reason is None:
            self._fail_reason = str(exc)[:100]

    def build(self) -> LatencyBreakdown:
        now = perf_counter()
        t0 = self._t0 or now
        t_body = self._t_body or now
        t_post = self._t_post or now
        return LatencyBreakdown(
            cycle_id=self.cycle_id,
            provider_used=self.provider_used,
            attempt_index=self.attempt_index,
            latency_provider_request_ms=0,
            latency_api_call_ms=int((t_body - t0) * 1000),
            postprocess_ms=int((t_post - t_body) * 1000),
            outcome=self._outcome,
            fail_reason=self._fail_reason,
            retry_count=self.retry_count,
        )
