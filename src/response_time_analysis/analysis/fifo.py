from collections.abc import Iterator

from response_time_analysis.analysis import Solution, solve, sparse_finite_search_space
from response_time_analysis.model import (
    EPSILON_TIME,
    Duration,
    SupplyModel,
    TaskSet,
)


def busy_window_bound(
    all_tasks: TaskSet,
    supply: SupplyModel,
    horizon: Duration | None = None,
) -> Duration | None:
    "A bound on the length of the busy window of any job of the task under analysis."
    trbf = all_tasks.rbf
    return solve.inequality(lhs=trbf, rhs=supply, horizon=horizon)


def points_of_interest(all_tasks: TaskSet) -> Iterator[Duration]:
    "The points at which the per-offset response-time bound must be computed."
    return all_tasks.rbf.steps()


def search_space(
    all_tasks: TaskSet,
    supply: SupplyModel,
    horizon: Duration | None = None,
    bw_bound: Duration | None = None,
) -> Iterator[Duration] | None:
    "The finite, sparse search space for FIFO RTA."

    L = busy_window_bound(all_tasks, supply, horizon) if bw_bound is None else bw_bound

    return sparse_finite_search_space(points_of_interest(all_tasks), L)


def rta(
    all_tasks: TaskSet,
    supply: SupplyModel,
    horizon: Duration | None = None,
) -> Solution:
    "Response-time analysis for uniprocessor first-in-first-out (FIFO) scheduling."

    assert not all_tasks.is_empty()

    # first, define the RTA inequality for a given offset
    def rta_for_offset(
        A: Duration,
    ) -> tuple[Duration, Duration | None, Duration | None]:
        all_work = all_tasks.rbf(A + EPSILON_TIME)
        F = solve.inequality(
            lhs=lambda _F: all_work,
            rhs=supply,
            horizon=horizon,
        )
        return (A, F, F - A) if F is not None else (A, None, None)

    # second, try to obtain the search space of relevant offsets
    L = busy_window_bound(all_tasks, supply, horizon)
    sp = search_space(all_tasks, supply, horizon, L)
    if sp is None or L is None:
        return Solution.no_search_space_found(all_tasks, all_tasks.tasks[0])

    # finally, analyze each element of the search space
    sp = tuple(rta_for_offset(A) for A in sp)

    return Solution.from_search_space(all_tasks, all_tasks.tasks[0], L, sp)
