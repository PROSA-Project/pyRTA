from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from .arrival import JobCount
from .time import EPSILON_TIME, Work


@dataclass(frozen=True, eq=True, order=True)
class WCET:
    "A real-time task's worst-case execution-time parameter."

    value: Work

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError("wcet must be positive")

    def __call__(self, njobs: JobCount) -> Work:
        return self.max_cost(njobs)

    def max_cost(self, njobs: JobCount) -> Work:
        r"Cumulative maximum cost of $n$ consecutive jobs (or invocations)"
        if njobs <= 0:
            return 0
        else:
            return njobs * self.value


CostModel: TypeAlias = WCET


@dataclass
class FullyPreemptive:
    "The classic preemption model in which a task's jobs can be preempted at any time"

    wcet: WCET

    @property
    def max_non_preemptive_segment(self) -> Work:
        "The maximum amount of work that a job must carry out while it remains non-preemptive."
        return EPSILON_TIME

    @property
    def run_to_completion_threshold(self) -> Work:
        "The maximum amount of work a job must receive before non-preemptively running to completion."
        return self.wcet.value


@dataclass
class FullyNonPreemptive:
    "A preemption model with run-to-completion semantics: once started, a job cannot be preempted."

    wcet: WCET

    @property
    def max_non_preemptive_segment(self) -> Work:
        "The maximum amount of work that a job must carry out while it remains non-preemptive."
        return self.wcet.value

    @property
    def run_to_completion_threshold(self) -> Work:
        "The maximum amount of work a job must receive before non-preemptively running to completion."
        return EPSILON_TIME


@dataclass
class FloatingNonPreemptive:
    "A preemption model in which a task's jobs can contain non-preemptive segments at unknown times"

    wcet: WCET
    max_nps: Work

    def __post_init__(self) -> None:
        if self.max_nps <= 0:
            raise ValueError("max_nps must be positive")
        if self.max_nps > self.wcet.value:
            raise ValueError("max_nps cannot exceed wcet")

    @property
    def max_non_preemptive_segment(self) -> Work:
        "The maximum amount of work that a job must carry out while it remains non-preemptive."
        return self.max_nps

    @property
    def run_to_completion_threshold(self) -> Work:
        "The maximum amount of work a job must receive before non-preemptively running to completion."
        return self.wcet.value


@dataclass
class LimitedPreemptive:
    """A preemption model in which a task's jobs consist of a sequence of non-preemptive
    segments with known preemption points."""

    wcet: WCET
    max_nps: Work
    last_nps: Work

    def __post_init__(self) -> None:
        if self.max_nps <= 0:
            raise ValueError("max_nps must be positive")
        if self.last_nps <= 0:
            raise ValueError("last_nps must be positive")
        if self.max_nps > self.wcet.value:
            raise ValueError("max_nps cannot exceed wcet")
        if self.last_nps > self.wcet.value:
            raise ValueError("last_nps cannot exceed wcet")
        if self.last_nps > self.max_nps:
            raise ValueError("last_nps cannot exceed max_nps")

    @property
    def max_non_preemptive_segment(self) -> Work:
        "The maximum amount of work that a job must carry out while it remains non-preemptive."
        return self.max_nps

    @property
    def run_to_completion_threshold(self) -> Work:
        "The maximum amount of work a job must receive before non-preemptively running to completion."
        return self.wcet.value - (self.last_nps - EPSILON_TIME)


PreemptionModel: TypeAlias = (
    FullyPreemptive | FullyNonPreemptive | FloatingNonPreemptive | LimitedPreemptive
)
