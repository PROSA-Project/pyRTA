from collections.abc import Iterable
from itertools import takewhile
from math import ceil

from response_time_analysis.analysis import (
    Solution,
    edf,
    fifo,
    fp,
    sparse_finite_search_space,
)
from response_time_analysis.analysis.solve import inequality
from response_time_analysis.model import (
    WCET,
    Deadline,
    Duration,
    FullyNonPreemptive,
    FullyPreemptive,
    IdealProcessor,
    Periodic,
    Priority,
    RateDelayModel,
    Task,
    taskset,
)


def steps_up_to(iterable: Iterable[Duration], limit: Duration) -> list[Duration]:
    return list(takewhile(lambda delta: delta < limit, iterable))


def test_solution_helpers_compute_response_time_bound() -> None:
    task = Task(
        arrivals=Periodic(5),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(5),
        priority=Priority(1),
    )
    ts = taskset(task)

    none_solution = Solution.no_search_space_found(ts, task)
    assert none_solution.busy_window_bound is None
    assert none_solution.search_space is None
    assert none_solution.response_time_bound is None
    assert not none_solution.bound_found()

    sp_with_bound = ((0, 1, 2), (3, 4, 5))
    solution = Solution.from_search_space(ts, task, 10, sp_with_bound)
    assert solution.bound_found()
    assert solution.response_time_bound == 5
    assert solution.busy_window_bound == 10

    sp_without_bound = ((0, 1, 2), (4, 6, None), (7, 8, 9))
    no_bound_solution = Solution.from_search_space(ts, task, 10, sp_without_bound)
    assert not no_bound_solution.bound_found()
    assert no_bound_solution.response_time_bound is None
    assert no_bound_solution.busy_window_bound == 10


def test_sparse_finite_search_space_limits_offsets() -> None:
    offsets = iter([0, 2, 4, 6])
    upper_bound = 5

    assert list(sparse_finite_search_space(offsets, upper_bound) or []) == [0, 2, 4]
    assert sparse_finite_search_space(iter([]), None) is None


def test_inequality_converges_and_respects_horizon() -> None:
    assert inequality(lhs=lambda x: x, rhs=lambda x: x + 1) == 1
    assert (
        inequality(
            lhs=lambda x: ceil(x / 10) * 5, rhs=lambda x: max(0, x - 50), horizon=40
        )
        is None
    )


def test_fifo_analysis_simple() -> None:
    supply = IdealProcessor()
    task = Task(arrivals=Periodic(3), execution=FullyPreemptive(WCET(1)))
    ts = taskset(task)

    assert fifo.busy_window_bound(ts, supply) == 1
    assert steps_up_to(fifo.points_of_interest(ts), limit=10)[:3] == [0, 3, 6]
    assert list(fifo.search_space(ts, supply) or []) == [0]

    solution = fifo.rta(ts, supply)
    assert solution.bound_found()
    assert solution.response_time_bound == 1


def test_fp_analysis_with_blocking_and_response_time_simple() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Periodic(4),
        execution=FullyPreemptive(WCET(1)),
        priority=Priority(10),
    )
    lp = Task(
        arrivals=Periodic(10),
        execution=FullyNonPreemptive(WCET(3)),
        priority=Priority(1),
    )
    ts = taskset(tua, lp)

    assert fp.blocking_bound(ts, tua) == 2
    assert fp.busy_window_bound(ts, tua, supply, pi_blocking_bound=2) == 3
    assert list(fp.search_space(ts, tua, supply) or []) == [0]

    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()
    assert solution.response_time_bound == 3


def test_edf_analysis_offsets_and_response_time_simple() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Periodic(5),
        execution=FullyPreemptive(WCET(2)),
        deadline=Deadline(10),
    )
    lp = Task(
        arrivals=Periodic(20),
        execution=FullyNonPreemptive(WCET(4)),
        deadline=Deadline(12),
    )
    ts = taskset(tua, lp)

    assert edf.busy_window_bound_nps(ts, tua) == 5
    assert edf.busy_window_bound_rbf(ts, supply) == 8
    assert edf.busy_window_bound(ts, tua, supply) == 8
    assert list(edf.blocking_bound_steps(ts, tua)) == [2]

    poi = steps_up_to(edf.points_of_interest(ts, tua, supply), limit=15)
    assert poi[:4] == [0, 2, 5, 10]

    search = edf.search_space(ts, tua, supply)
    assert list(search or []) == [0, 2, 5]

    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()
    assert solution.response_time_bound == 5


def test_fifo_analysis_rate_delay() -> None:
    supply = RateDelayModel(period=100, allocation=90, delay=25)
    task = Task(arrivals=Periodic(3), execution=FullyPreemptive(WCET(1)))
    ts = taskset(task)

    assert fifo.busy_window_bound(ts, supply) == 41
    assert list(fifo.search_space(ts, supply) or []) == list(range(0, 40, 3))

    solution = fifo.rta(ts, supply)
    assert solution.bound_found()
    assert solution.response_time_bound == 27
