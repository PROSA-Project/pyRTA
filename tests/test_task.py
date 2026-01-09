import pytest

from response_time_analysis.model import (
    WCET,
    FullyPreemptive,
    Periodic,
    Task,
    deadline_of,
    prio_of,
)


def test_deadline_missing_raises_value_error() -> None:
    task = Task(arrivals=Periodic(10), execution=FullyPreemptive(WCET(1)))

    with pytest.raises(ValueError, match="deadline parameter missing"):
        _ = deadline_of(task)


def test_priority_missing_raises_value_error() -> None:
    task = Task(arrivals=Periodic(10), execution=FullyPreemptive(WCET(1)))

    with pytest.raises(ValueError, match="priority parameter missing"):
        _ = prio_of(task)
