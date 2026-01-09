from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import TypeAlias, overload

from response_time_analysis.iter import merge_sorted_unique

from .arrival import ArrivalModel, JobCount
from .execution import CostModel
from .policy import (
    Deadline,
)
from .time import (
    EPSILON_TIME,
    Demand,
    Duration,
    Work,
)


@dataclass(frozen=True)
class RequestBoundFunction:
    "Upper bound on the total processor service required by a task, commonly called RBF."

    cm: CostModel
    am: ArrivalModel

    def rbf(self, delta: Duration) -> Work:
        r"""$RBF(\delta)$ -- the maximum cumulative cost of all jobs released
        in an interval of length $\delta$.
        """
        njobs = self.am.max_arrivals(delta)
        return self.cm.max_cost(njobs)

    def __call__(self, delta: Duration) -> Work:
        r"$RBF(\delta)$"
        return self.rbf(delta)

    def steps(self) -> Iterator[Duration]:
        """Iterator yielding values of delta such that
        rbf(delta) != rbf(delta + 1)"""

        return self.am.steps()


@dataclass(frozen=True)
class DemandBoundFunction:
    "Upper bound on the total processor demand required by a task, commonly called DBF."

    rbf: RequestBoundFunction
    deadline: Deadline

    def dbf(self, delta: Duration) -> Demand:
        shifted_delta = delta - (self.deadline.value - 1)
        return self.rbf(shifted_delta)

    def __call__(self, delta: Duration) -> Demand:
        r"$DBF(\delta)$"
        return self.dbf(delta)

    def steps(self) -> Iterator[Duration]:
        """Iterator yielding values of delta such that
        dbf(delta) != dbf(delta + 1)."""

        return (
            delta + (self.deadline.value - EPSILON_TIME) for delta in self.rbf.steps()
        )


@dataclass(frozen=True)
class Total:
    parts: tuple[StepBound, ...]

    def cumulative_bound(self, delta: Duration) -> Demand | Work | JobCount:
        return sum(p(delta) for p in self.parts)

    def __call__(self, delta: Duration) -> Demand | Work | JobCount:
        return self.cumulative_bound(delta)

    def steps(self) -> Iterator[Duration]:
        """Iterator yielding values of delta such that
        cumulative_bound(delta) != cumulative_bound(delta + 1)."""
        return merge_sorted_unique(p.steps() for p in self.parts)


@overload
def total(*bounds: StepBound) -> Total: ...


@overload
def total(bounds: Iterable[StepBound]) -> Total: ...


def total(*args: object) -> Total:  # pyright: ignore[reportInconsistentOverload]
    # runtime implementation
    if len(args) == 1 and isinstance(args[0], Iterable):
        return Total(tuple(iter(args[0])))  # pyright: ignore[reportArgumentType]
    else:
        assert all(isinstance(b, StepBound) for b in args)
        return Total(args)  # pyright: ignore[reportArgumentType]


StepBound: TypeAlias = ArrivalModel | RequestBoundFunction | DemandBoundFunction | Total
