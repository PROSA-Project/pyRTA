from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from .time import Duration, Work


@dataclass(frozen=True)
class IdealProcessor:
    speed: Work = 1

    def __post_init__(self) -> None:
        if self.speed <= 0:
            raise ValueError("processor speed must be positive")

    def supply_bound(self, delta: Duration) -> Work:
        if delta > 0:
            return self.speed * delta
        else:
            return 0

    def __call__(self, delta: Duration) -> Work:
        return self.supply_bound(delta)


@dataclass(frozen=True)
class RateDelayModel:
    period: Duration
    allocation: Work  # guaranteed resource amount per period
    delay: Duration  # inaccuracy of the supply

    def __post_init__(self) -> None:
        if self.period <= 0:
            raise ValueError("period must be positive")
        if self.allocation <= 0:
            raise ValueError("allocation must be positive")
        if self.delay < 0:
            raise ValueError("delay must be non-negative")

    def supply_bound(self, delta: Duration) -> Work:
        delta_shifted = delta - self.delay
        if delta_shifted > 0:
            return (delta_shifted * self.allocation) // self.period
        else:
            return 0

    def __call__(self, delta: Duration) -> Work:
        return self.supply_bound(delta)


SupplyModel: TypeAlias = IdealProcessor | RateDelayModel
