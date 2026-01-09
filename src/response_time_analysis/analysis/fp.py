from collections.abc import Iterator

from response_time_analysis.model import (
    EPSILON_TIME,
    ArrivalCurvePrefix,
    Duration,
    SupplyModel,
    Task,
    TaskSet,
    Work,
)

from . import Solution, solve, sparse_finite_search_space


def blocking_bound(all_tasks: TaskSet, task_under_analysis: Task) -> Work:
    "The maximum priority-inversion incurred by a job of the task under analysis."
    return max(
        (
            t.execution.max_non_preemptive_segment - EPSILON_TIME
            for t in all_tasks.with_priority_lower_than_iter(task_under_analysis)
        ),
        default=0,
    )


def busy_window_bound(
    all_tasks: TaskSet,
    task_under_analysis: Task,
    supply: SupplyModel,
    horizon: Duration | None = None,
    pi_blocking_bound: Work | None = None,
) -> Duration | None:
    "A bound on the length of the busy window of any job of the task under analysis."
    if pi_blocking_bound is None:
        pi_blocking_bound = blocking_bound(all_tasks, task_under_analysis)
    hep_trbf = all_tasks.with_priority_higher_than_or_equal_to(task_under_analysis).rbf
    return solve.inequality(
        lhs=lambda L: pi_blocking_bound + hep_trbf(L),
        rhs=supply,
        horizon=horizon,
    )


def points_of_interest(task_under_analysis: Task) -> Iterator[Duration]:
    "The points at which the per-offset response-time bound must be computed."
    return task_under_analysis.rbf.steps()


def search_space(
    all_tasks: TaskSet,
    task_under_analysis: Task,
    supply: SupplyModel,
    horizon: Duration | None = None,
    pi_blocking_bound: Work | None = None,
    bw_bound: Duration | None = None,
) -> Iterator[Duration] | None:
    "The finite, sparse search space for FP RTA."

    L = (
        busy_window_bound(
            all_tasks, task_under_analysis, supply, horizon, pi_blocking_bound
        )
        if bw_bound is None
        else bw_bound
    )

    # The search space consists of all points of interest less than L.
    return sparse_finite_search_space(points_of_interest(task_under_analysis), L)


def round_to_horizon(tsk: Task, L: Duration) -> Duration:
    """Support for POET's over-approximated search spaces:
    For tasks that use an ArrivalCurvePrefix, "round up" the given busy-window bound
    to the next integral multiple of the arrival-curve prefix's horizon.
    """
    if isinstance(tsk.arrivals, ArrivalCurvePrefix):
        return ((L // tsk.arrivals.horizon) + 1) * tsk.arrivals.horizon
    else:
        return L


def rta(
    all_tasks: TaskSet,
    task_under_analysis: Task,
    supply: SupplyModel,
    horizon: Duration | None = None,
    # special case for POET's over-approximated search spaces -- works only for ArrivalCurvePrefix
    use_poet_search_space: bool = False,
) -> Solution:
    "Response-time analysis for uniprocessor fixed-priority (FP) scheduling."

    assert not all_tasks.is_empty()

    # first, identify all other higher-or-equal-priority interfering tasks
    ohep_tasks = all_tasks.with_priority_higher_than_or_equal_to_excluding(
        task_under_analysis
    )

    # second, compute the blocking bound
    bb = blocking_bound(all_tasks, task_under_analysis)

    # third, define the RTA inequalities to be solved for a given offset
    def rta_for_offset(
        A: Duration,
    ) -> tuple[Duration, Duration | None, Duration | None]:
        tua_work = task_under_analysis.rbf(A + EPSILON_TIME) - (
            task_under_analysis.cost.value
            - task_under_analysis.execution.run_to_completion_threshold
        )

        F = solve.inequality(
            lhs=lambda F: bb + tua_work + ohep_tasks.rbf(F),
            rhs=supply,
            horizon=horizon,
        )
        if F is None:
            return (A, None, None)

        def needed_supply(_AR: Duration) -> Work:
            return supply(F) + (
                task_under_analysis.cost.value
                - task_under_analysis.execution.run_to_completion_threshold
            )

        AR = solve.inequality(
            lhs=needed_supply,
            rhs=lambda AR: supply(AR),
            start=needed_supply(A + F),
            horizon=horizon,
        )
        return (A, F, max(0, AR - A, F - A)) if AR is not None else (A, F, None)

    # fourth, try to obtain the search space of relevant offsets
    L = busy_window_bound(
        all_tasks,
        task_under_analysis,
        supply,
        horizon,
        pi_blocking_bound=bb,
    )
    if L is None:
        return Solution.no_search_space_found(all_tasks, task_under_analysis)
    sp_bound = (
        L if not use_poet_search_space else round_to_horizon(task_under_analysis, L)
    )
    sp = search_space(
        all_tasks,
        task_under_analysis,
        supply,
        horizon,
        bw_bound=sp_bound,
    )
    if sp is None:
        return Solution.no_search_space_found(all_tasks, task_under_analysis)

    # finally, analyze each element of the search space
    sp = tuple(rta_for_offset(A) for A in sp)

    return Solution.from_search_space(all_tasks, task_under_analysis, L, sp)
