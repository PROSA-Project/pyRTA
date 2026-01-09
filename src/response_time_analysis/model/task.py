from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from typing import overload

from .arrival import ArrivalModel
from .execution import CostModel, PreemptionModel
from .policy import (
    Deadline,
    Priority,
)
from .workload import DemandBoundFunction, RequestBoundFunction, Total, total


@dataclass(frozen=True)
class Task:
    arrivals: ArrivalModel
    execution: PreemptionModel
    deadline: Deadline | None = None
    priority: Priority | None = None

    @property
    def cost(self) -> CostModel:
        return self.execution.wcet

    @property
    def rbf(self) -> RequestBoundFunction:
        return RequestBoundFunction(self.cost, self.arrivals)

    @property
    def dbf(self) -> DemandBoundFunction | None:
        if self.deadline is not None:
            return DemandBoundFunction(self.rbf, self.deadline)
        else:
            return None


def deadline_parameter_missing():
    raise ValueError("deadline parameter missing")


def deadline_of(t: Task) -> Deadline:
    return t.deadline if t.deadline is not None else deadline_parameter_missing()


def priority_parameter_missing():
    raise ValueError("priority parameter missing")


def prio_of(t: Task) -> Priority:
    return t.priority if t.priority is not None else priority_parameter_missing()


@dataclass(frozen=True)
class TaskSet:
    tasks: tuple[Task, ...]

    @property
    def rbf(self) -> Total:
        return total(t.rbf for t in self.tasks)

    @property
    def max_arrivals(self) -> Total:
        return total(t.arrivals for t in self.tasks)

    @property
    def dbf(self) -> Total:
        return total(
            t.dbf if t.dbf is not None else deadline_parameter_missing()
            for t in self.tasks
        )

    def is_empty(self) -> bool:
        return len(self.tasks) == 0

    def __iter__(self) -> Iterator[Task]:
        return iter(self.tasks)

    def __len__(self) -> int:
        return len(self.tasks)

    def such_that(self, pred: Callable[[Task], bool]) -> TaskSet:
        return TaskSet(tuple(t for t in self.tasks if pred(t)))

    def with_priority_higher_than(self, prio_level: Priority | Task) -> TaskSet:
        if isinstance(prio_level, Task):
            prio_level = prio_of(prio_level)
        return self.such_that(lambda t: prio_of(t) > prio_level)

    def with_priority_higher_than_or_equal_to(
        self, prio_level: Priority | Task
    ) -> TaskSet:
        if isinstance(prio_level, Task):
            prio_level = prio_of(prio_level)
        return self.such_that(lambda t: prio_of(t) >= prio_level)

    def with_priority_higher_than_or_equal_to_excluding(
        self,
        excluded: Task,
        prio_level: Priority | None = None,
    ) -> TaskSet:
        if prio_level is None:
            prio_level = prio_of(excluded)
        return self.such_that(lambda t: prio_of(t) >= prio_level and t != excluded)

    def with_priority_lower_than(self, prio_level: Priority | Task) -> TaskSet:
        if isinstance(prio_level, Task):
            prio_level = prio_of(prio_level)
        return self.such_that(lambda t: prio_of(t) < prio_level)

    def with_priority_lower_than_iter(
        self, prio_level: Priority | Task
    ) -> Iterator[Task]:
        if isinstance(prio_level, Task):
            prio_level = prio_of(prio_level)
        return (t for t in self.tasks if prio_of(t) < prio_level)

    def with_deadline_at_most(self, reference: Deadline | Task) -> TaskSet:
        if isinstance(reference, Task):
            reference = deadline_of(reference)
        return self.such_that(lambda t: deadline_of(t) <= reference)

    def with_deadline_at_most_iter(self, reference: Deadline | Task) -> Iterator[Task]:
        if isinstance(reference, Task):
            reference = deadline_of(reference)
        return (t for t in self.tasks if deadline_of(t) <= reference)

    def with_deadline_greater_than(self, reference: Deadline | Task) -> TaskSet:
        if isinstance(reference, Task):
            reference = deadline_of(reference)
        return self.such_that(lambda t: deadline_of(t) > reference)

    def with_deadline_greater_than_iter(
        self, reference: Deadline | Task
    ) -> Iterator[Task]:
        if isinstance(reference, Task):
            reference = deadline_of(reference)
        return (t for t in self.tasks if deadline_of(t) > reference)

    def excluding(self, excluded: Task) -> TaskSet:
        return self.such_that(lambda t: t != excluded)

    def excluding_iter(self, excluded: Task) -> Iterator[Task]:
        return (t for t in self.tasks if t != excluded)


@overload
def taskset(*tasks: Task) -> TaskSet: ...


@overload
def taskset(tasks: Iterable[Task]) -> TaskSet: ...


def taskset(*args: object) -> TaskSet:  # pyright: ignore[reportInconsistentOverload]
    # runtime implementation
    if len(args) == 1 and isinstance(args[0], Iterable):
        return TaskSet(tuple(iter(args[0])))  # pyright: ignore[reportArgumentType]
    else:
        assert all(isinstance(t, Task) for t in args)
        return TaskSet(args)  # pyright: ignore[reportArgumentType]
