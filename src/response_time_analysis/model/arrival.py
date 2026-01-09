from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from itertools import chain, count, dropwhile
from math import ceil
from typing import TypeAlias

from .time import EPSILON_TIME, Duration

JobCount: TypeAlias = int


@dataclass(frozen=True)
class Periodic:
    "A periodic task's period parameter."

    period: Duration

    def __post_init__(self) -> None:
        if self.period <= 0:
            raise ValueError("period must be positive")

    def __call__(self, delta: Duration) -> JobCount:
        r"Upper arrival curve $\alpha^+(\delta)$"
        return self.max_arrivals(delta)

    def max_arrivals(self, delta: Duration) -> JobCount:
        r"Upper arrival curve $\alpha^+(\delta)$"
        if delta <= 0:
            return 0
        else:
            return ceil(delta / self.period)

    def steps(self) -> Iterator[Duration]:
        """Iterator yielding values of delta such that
        max_arrivals(delta) != max_arrivals(delta + 1)"""

        return count(0, self.period)


@dataclass(frozen=True)
class PeriodicWithJitter:
    "A sporadic task's minimum inter-arrival parameter."

    period: Duration
    jitter: Duration

    def __post_init__(self) -> None:
        if self.period <= 0:
            raise ValueError("period must be positive")
        if self.jitter < 0:
            raise ValueError("jitter must be non-negative")

    def __call__(self, delta: Duration) -> JobCount:
        r"Upper arrival curve $\alpha^+(\delta)$"
        return self.max_arrivals(delta)

    def max_arrivals(self, delta: Duration) -> JobCount:
        r"Upper arrival curve $\alpha^+(\delta)$"
        if delta <= 0:
            return 0
        else:
            return ceil((delta + self.jitter) / self.period)

    def steps(self) -> Iterator[Duration]:
        """Iterator yielding values of delta such that
        max_arrivals(delta) != max_arrivals(delta + 1)"""

        raw_steps = count(-self.jitter, self.period)
        filtered = dropwhile(lambda delta: delta <= 0, raw_steps)
        return chain([0], filtered)


@dataclass(frozen=True)
class Sporadic:
    "A sporadic task's minimum inter-arrival parameter."

    mit: Duration

    def __post_init__(self) -> None:
        if self.mit <= 0:
            raise ValueError("minimum inter-arrival time must be positive")

    def __call__(self, delta: Duration) -> JobCount:
        r"Upper arrival curve $\alpha^+(\delta)$"
        return self.max_arrivals(delta)

    def max_arrivals(self, delta: Duration) -> JobCount:
        r"Upper arrival curve $\alpha^+(\delta)$"
        if delta <= 0:
            return 0
        else:
            return int(ceil(delta / self.mit))

    def steps(self) -> Iterator[Duration]:
        """Iterator yielding values of delta such that
        max_arrivals(delta) != max_arrivals(delta + 1)"""

        return count(0, self.mit)


@dataclass(frozen=True)
class MinimumSeparationVector:
    """Sporadic arrivals charaterized by an arbitrary arrival-curve prefix,
    expressed as a delta-min vector."""

    # delta-min vector:
    # dmin[0] is the minimum separation of two jobs,
    # dmin[1] is the minimum separation of three jobs,
    # and so on.
    dmin: list[Duration]

    def __post_init__(self) -> None:
        if len(self.dmin) == 0:
            raise ValueError("dmin must not be empty")
        if any(gap < 0 for gap in self.dmin):
            raise ValueError("dmin gaps must be non-negative")
        if any(b < a for a, b in zip(self.dmin, self.dmin[1:])):
            raise ValueError("dmin must be non-decreasing")

    def __call__(self, delta: Duration) -> JobCount:
        r"Upper arrival curve $\alpha^+(\delta)$"
        return self.max_arrivals(delta)

    @property
    def max_covered_delta(self) -> Duration:
        return self.dmin[-1]

    @property
    def max_covered_njobs(self) -> int:
        return len(self.dmin) + 1

    def extrapolate(self):
        n = self.max_covered_njobs + 1
        dmin_for_n = max(
            self.min_gap_between(i) + self.min_gap_between(n - i + 1)
            for i in range(2, self.max_covered_njobs // 2)
        )
        self.dmin.append(dmin_for_n)

    def min_gap_between(self, n: int) -> Duration:
        if n <= 1:
            return 0

        while self.max_covered_njobs < n:
            self.extrapolate()

        return self.dmin[n - 2]

    def max_arrivals(self, delta: Duration) -> JobCount:
        r"Upper arrival curve $\alpha^+(\delta)$"
        if delta <= 0:
            return 0

        while self.max_covered_delta < delta:
            self.extrapolate()

        for n in range(2, self.max_covered_njobs + 1):
            if delta <= self.min_gap_between(n):
                return n - 1

        assert False  # not reachable

    def steps(self) -> Iterator[Duration]:
        """Iterator yielding values of delta such that
        max_arrivals(delta) != max_arrivals(delta + 1)"""
        yield 0  # for one job
        last_yielded = 0
        for n in count(2):
            gap = self.min_gap_between(n)
            if gap != last_yielded:
                yield gap
                last_yielded = gap


@dataclass(frozen=True)
class ArrivalCurvePrefix:
    """Sporadic arrivals charaterized by an arbitrary arrival-curve prefix,
    expressed as a list of steps of the arrival curve up to a given horizon."""

    # Horizon of the given arrival-curve prefix.
    horizon: Duration
    # The steps of the eta-max curve up to the horizon.
    # A tuple (δ, c) ∈ ac_steps means
    # α(δ) = c and ∀ δ' < δ,  α(δ) < c.
    # The first step must be for δ=EPSILON_TIME.
    ac_steps: list[tuple[Duration, JobCount]]

    def __post_init__(self) -> None:
        if self.horizon <= 0:
            raise ValueError("horizon must be positive")
        if len(self.ac_steps) == 0:
            raise ValueError("ac_steps must not be empty")
        if self.ac_steps[0][0] != EPSILON_TIME:
            raise ValueError("first arrival-curve step must be at EPSILON_TIME")
        last_delta = 0
        last_jobs = 0
        for delta, jobs in self.ac_steps:
            if delta <= last_delta:
                raise ValueError("ac_steps must be strictly increasing in delta")
            if delta >= self.horizon:
                raise ValueError("ac_steps must lie within the given horizon")
            if jobs <= last_jobs:
                raise ValueError("ac_steps must be increasing in job count")
            last_delta = delta
            last_jobs = jobs

    def __call__(self, delta: Duration) -> JobCount:
        r"Upper arrival curve $\alpha^+(\delta)$"
        return self.max_arrivals(delta)

    def max_arrivals_within_horizon(self, delta: Duration) -> JobCount:
        if delta <= 0:
            return 0

        assert delta < self.horizon

        for i in range(1, len(self.ac_steps)):
            if self.ac_steps[i][0] > delta:
                return self.ac_steps[i - 1][1]

        return self.ac_steps[-1][1]

    def max_arrivals(self, delta: Duration) -> JobCount:
        r"Upper arrival curve $\alpha^+(\delta)$"
        if delta <= 0:
            return 0

        # This uses a "fast extrapolation" technique that avoids more costly
        # curve extrapolation as in the delta-min-based ArrivalCurve implementation.

        full_windows = delta // self.horizon
        offset = delta % self.horizon
        jobs_in_last_window = self.max_arrivals_within_horizon(offset)

        return full_windows * self.ac_steps[-1][1] + jobs_in_last_window

    def steps(self) -> Iterator[Duration]:
        """Iterator yielding values of delta such that
        max_arrivals(delta) != max_arrivals(delta + 1)"""
        for window in count(0):
            window_start = window * self.horizon
            for delta, _job_count in self.ac_steps:
                yield window_start + delta - EPSILON_TIME


ArrivalModel: TypeAlias = (
    Periodic
    | PeriodicWithJitter
    | Sporadic
    | MinimumSeparationVector
    | ArrivalCurvePrefix
)
