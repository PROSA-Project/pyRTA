from collections.abc import Iterable
from itertools import takewhile

from response_time_analysis.analysis import edf
from response_time_analysis.iter import brute_force_steps
from response_time_analysis.model import (
    WCET,
    ArrivalCurvePrefix,
    Deadline,
    DemandBoundFunction,
    Duration,
    FullyNonPreemptive,
    MinimumSeparationVector,
    Periodic,
    PeriodicWithJitter,
    RequestBoundFunction,
    Sporadic,
    StepBound,
    Task,
    taskset,
    total,
)


def steps_up_to(bound: StepBound | Iterable[Duration], *, limit: int) -> list[int]:
    if isinstance(bound, StepBound):
        it = bound.steps()
    else:
        it = bound
    return list(takewhile(lambda delta: delta <= limit, it))


def test_periodic_steps_match_bruteforce() -> None:
    am = Periodic(period=5)
    limit = 27

    assert steps_up_to(am, limit=limit) == list(brute_force_steps(am, limit=limit))


def test_periodic_with_jitter_steps_match_bruteforce() -> None:
    am = PeriodicWithJitter(period=5, jitter=3)
    limit = 28

    assert steps_up_to(am, limit=limit) == list(brute_force_steps(am, limit=limit))


def test_sporadic_steps_match_bruteforce() -> None:
    am = Sporadic(mit=4)
    limit = 24

    assert steps_up_to(am, limit=limit) == list(brute_force_steps(am, limit=limit))


def test_arrival_curve_steps_match_bruteforce() -> None:
    am = MinimumSeparationVector(dmin=[2, 5, 9, 14, 20])
    limit = 75

    assert steps_up_to(am, limit=limit) == list(brute_force_steps(am, limit=limit))


def test_arrival_curve_prefix_steps_match_bruteforce() -> None:
    am = ArrivalCurvePrefix(horizon=200, ac_steps=[(1, 3), (21, 4), (31, 5), (51, 6)])
    limit = 500

    assert steps_up_to(am, limit=limit) == list(brute_force_steps(am, limit=limit))


def test_request_bound_function_steps_match_bruteforce() -> None:
    am = Periodic(period=4)
    rbf = RequestBoundFunction(WCET(3), am)
    limit = 33

    assert steps_up_to(rbf, limit=limit) == list(brute_force_steps(rbf, limit=limit))


def test_demand_bound_function_steps_match_bruteforce() -> None:
    am = Sporadic(mit=6)
    rbf = RequestBoundFunction(WCET(2), am)
    dbf = DemandBoundFunction(rbf, Deadline(5))
    limit = 33

    assert steps_up_to(dbf, limit=limit) == list(brute_force_steps(dbf, limit=limit))


def test_total_steps_merge_parts_like_bruteforce() -> None:
    am1 = Periodic(period=5)
    am2 = PeriodicWithJitter(period=7, jitter=2)
    combined = total(am1, am2)
    limit = 48

    assert steps_up_to(combined, limit=limit) == list(
        brute_force_steps(combined, limit=limit)
    )


def test_edf_blocking_bound_steps_match_bruteforce() -> None:
    tasks = taskset(
        Task(
            execution=FullyNonPreemptive(WCET(3)),
            arrivals=Periodic(1000),
            deadline=Deadline(900),
        ),
        Task(
            execution=FullyNonPreemptive(WCET(19)),
            arrivals=Periodic(100),
            deadline=Deadline(90),
        ),
        Task(
            execution=FullyNonPreemptive(WCET(20)),
            arrivals=Sporadic(33),
            deadline=Deadline(40),
        ),
        Task(
            execution=FullyNonPreemptive(WCET(2)),
            arrivals=PeriodicWithJitter(period=10, jitter=5),
            deadline=Deadline(15),
        ),
    )

    limit = 1500
    for t in tasks:
        assert steps_up_to(edf.blocking_bound_steps(tasks, t), limit=limit) == list(
            brute_force_steps(
                lambda offset: edf.blocking_bound(tasks, t, offset),
                limit=limit,
                yield_succ=True,
            )
        )
