"""Hard per-run ceilings, checked before a call rather than after it.

Every specification states four ceilings and a deadline. The rule they share is
that a call which *would* breach is never made: checking afterwards means the
tokens are already spent and the ceiling was decoration. A breach ends the run
at ``failed`` and never at ``ok``.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from .errors import BudgetExceeded, LivenessExceeded

#: Per-million-token prices are deployment configuration, not something this
#: module may assume. A runner supplies them; without them the USD ceiling
#: cannot be enforced pre-call and :meth:`Budget.project` says so.
Prices = dict[str, tuple[float, float]]  # model -> (usd per 1M in, usd per 1M out)


@dataclass
class Budget:
    """Ceilings for one run, and what has been spent against them."""

    tokens_max: int
    tool_calls_max: int
    usd_cap: float
    liveness_seconds: int
    max_regenerations: int = 3
    prices: Prices = field(default_factory=dict)

    tokens_used: int = 0
    tool_calls_used: int = 0
    usd_spent: float = 0.0
    regenerations_used: int = 0

    _started: float = field(default_factory=time.monotonic, repr=False)

    # -- enforcement ------------------------------------------------------
    def check_liveness(self) -> None:
        """Raise if the run has outlived its deadline."""
        elapsed = time.monotonic() - self._started
        if elapsed > self.liveness_seconds:
            raise LivenessExceeded(
                f"liveness deadline exceeded: {elapsed:.0f}s of {self.liveness_seconds}s"
            )

    def project(self, *, model: str = "", tokens_in: int = 0, tokens_out: int = 0,
                tool_calls: int = 1) -> float:
        """Raise if the described call would breach any ceiling; return its cost.

        Cost is ``0.0`` when no price is known for the model. That is reported
        rather than guessed, because a fabricated price makes the USD ceiling
        meaningless in exactly the direction that costs money.
        """
        self.check_liveness()

        tokens = tokens_in + tokens_out
        if self.tokens_used + tokens > self.tokens_max:
            raise BudgetExceeded(
                f"tokens: {self.tokens_used + tokens} would exceed {self.tokens_max}",
                reason="budget_breach:tokens",
            )
        if self.tool_calls_used + tool_calls > self.tool_calls_max:
            raise BudgetExceeded(
                f"tool_calls: {self.tool_calls_used + tool_calls} would exceed "
                f"{self.tool_calls_max}",
                reason="budget_breach:tool_calls",
            )

        cost = self.estimate(model, tokens_in, tokens_out)
        if self.usd_spent + cost > self.usd_cap:
            raise BudgetExceeded(
                f"usd: {self.usd_spent + cost:.4f} would exceed {self.usd_cap:.2f}",
                reason="budget_breach:usd",
            )
        return cost

    def spend(self, *, model: str = "", tokens_in: int = 0, tokens_out: int = 0,
              tool_calls: int = 1) -> None:
        """Record a call that has happened. Call :meth:`project` first."""
        self.tokens_used += tokens_in + tokens_out
        self.tool_calls_used += tool_calls
        self.usd_spent += self.estimate(model, tokens_in, tokens_out)

    def regenerate(self) -> None:
        """Count one schema-regeneration attempt, raising past the cap."""
        self.regenerations_used += 1
        if self.regenerations_used > self.max_regenerations:
            raise BudgetExceeded(
                f"regenerations: {self.regenerations_used} would exceed "
                f"{self.max_regenerations}",
                reason="budget_breach:regenerations",
            )

    # -- reporting --------------------------------------------------------
    def estimate(self, model: str, tokens_in: int, tokens_out: int) -> float:
        """USD for a call, or ``0.0`` when the model has no configured price."""
        if model not in self.prices:
            return 0.0
        per_in, per_out = self.prices[model]
        return (tokens_in / 1_000_000) * per_in + (tokens_out / 1_000_000) * per_out

    @property
    def priced(self) -> bool:
        """Whether a USD ceiling can be enforced at all."""
        return bool(self.prices)

    @property
    def elapsed_seconds(self) -> float:
        return time.monotonic() - self._started

    def as_record(self) -> dict:
        """The ``budget`` block of a run record."""
        return {
            "tokens_max": self.tokens_max,
            "tokens_used": self.tokens_used,
            "tool_calls_max": self.tool_calls_max,
            "tool_calls_used": self.tool_calls_used,
            "usd_cap": round(self.usd_cap, 4),
            "usd_spent": round(self.usd_spent, 4),
        }
