"""Bounded exponential backoff, with the figures the standard pins.

Four attempts at 1s, 2s, 4s and 8s with jitter of plus or minus twenty per
cent, and a sixty-second ceiling on any single request. Retries count against
the run's budgets, so a call that retries into a ceiling stops there rather
than spending past it.
"""

from __future__ import annotations

import random
import time
from typing import Callable, Iterable, TypeVar

from .budget import Budget
from .errors import CoreError, RetriesExhausted

T = TypeVar("T")

MAX_ATTEMPTS = 4
BASE_DELAYS = (1.0, 2.0, 4.0, 8.0)
JITTER = 0.20
REQUEST_TIMEOUT_SECONDS = 60


def backoff_delays(rng: random.Random | None = None) -> list[float]:
    """The delays between attempts, jittered. One shorter than the attempts."""
    rand = rng or random
    return [
        d * (1 + rand.uniform(-JITTER, JITTER))
        for d in BASE_DELAYS[: MAX_ATTEMPTS - 1]
    ]


def call_with_retry(
    fn: Callable[[], T],
    *,
    retry_on: Iterable[type[BaseException]] = (TimeoutError, ConnectionError),
    budget: Budget | None = None,
    sleep: Callable[[float], None] = time.sleep,
    rng: random.Random | None = None,
    on_attempt: Callable[[int, BaseException | None], None] | None = None,
) -> T:
    """Call ``fn``, retrying transient failures up to :data:`MAX_ATTEMPTS`.

    A :class:`~employees.core.errors.CoreError` is never retried: a budget
    breach or a blast-radius violation is a decision, not a transient fault,
    and retrying it would spend the very budget that stopped the run.
    """
    retryable = tuple(retry_on)
    delays = backoff_delays(rng)
    last: BaseException | None = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        if budget is not None:
            budget.check_liveness()
        try:
            if on_attempt:
                on_attempt(attempt, None)
            return fn()
        except CoreError:
            raise
        except retryable as exc:
            last = exc
            if on_attempt:
                on_attempt(attempt, exc)
            if attempt == MAX_ATTEMPTS:
                break
            sleep(delays[attempt - 1])

    raise RetriesExhausted(
        f"{MAX_ATTEMPTS} attempts exhausted; last failure: {type(last).__name__}: {last}"
    )
