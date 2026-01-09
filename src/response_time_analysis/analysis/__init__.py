from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from itertools import takewhile

from ..model import Duration, Task, TaskSet


@dataclass
class Solution:
    taskset: TaskSet
    task_under_analysis: Task
    busy_window_bound: Duration | None
    search_space: tuple[tuple[Duration, Duration | None, Duration | None], ...] | None
    response_time_bound: Duration | None

    @staticmethod
    def no_search_space_found(ts: TaskSet, tua: Task) -> Solution:
        return Solution(ts, tua, None, None, None)

    @staticmethod
    def from_search_space(
        ts: TaskSet,
        tua: Task,
        bw_bound: Duration,
        sp: tuple[tuple[Duration, Duration | None, Duration | None], ...],
    ) -> Solution:
        rtb = 0
        for _A, _F, R in sp:
            if R is None:
                rtb = None
                break
            else:
                rtb = max(rtb, R)

        return Solution(ts, tua, bw_bound, sp, rtb)

    def bound_found(self) -> bool:
        return self.response_time_bound is not None


def sparse_finite_search_space(
    offsets_of_interests: Iterator[Duration], upper_bound: Duration | None
) -> Iterator[Duration] | None:
    return (
        takewhile(lambda A: A < upper_bound, offsets_of_interests)
        if upper_bound is not None
        else None
    )
