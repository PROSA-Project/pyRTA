from response_time_analysis import edf, fifo, fp
from response_time_analysis.model import (
    WCET,
    Deadline,
    FullyPreemptive,
    IdealProcessor,
    Periodic,
    Priority,
    Task,
    taskset,
)


def test_readme() -> None:
    # Two periodic tasks with implicit deadlines; higher priority has the larger numeric value as in Linux
    tsk1 = Task(Periodic(period=5), FullyPreemptive(WCET(1)), Deadline(5), Priority(2))
    tsk2 = Task(Periodic(period=10), FullyPreemptive(WCET(6)), Deadline(9), Priority(1))

    supply = IdealProcessor()

    tasks = taskset(tsk1, tsk2)

    # RTA assuming uniprocessor fixed-priority scheduling.
    solution = fp.rta(tasks, tsk2, supply)
    assert solution.bound_found()
    assert solution.response_time_bound == 8

    # RTA assuming uniprocessor earliest-deadline first scheduling.
    solution = edf.rta(tasks, tsk2, supply)
    assert solution.bound_found()
    assert solution.response_time_bound == 7

    # RTA assuming uniprocessor FIFO scheduling.
    solution = fifo.rta(tasks, supply)
    assert solution.bound_found()
    assert solution.response_time_bound == 7

    # Use the horizon parameter to prevent the RTA from diverging.
    tsk3 = Task(Periodic(period=9), FullyPreemptive(WCET(3)), Deadline(20), Priority(3))
    overload = taskset(tsk1, tsk2, tsk3)
    solution = fifo.rta(overload, supply, horizon=1000)
    assert solution.bound_found() is False
    assert solution.search_space is None
    assert solution.response_time_bound is None
