from collections.abc import Iterator
from itertools import dropwhile

from response_time_analysis.iter import merge_sorted_unique
from response_time_analysis.model import (
    EPSILON_TIME,
    ArrivalCurvePrefix,
    Deadline,
    Duration,
    IdealProcessor,
    SupplyModel,
    Task,
    TaskSet,
    Work,
    deadline_of,
)

from . import Solution, solve, sparse_finite_search_space


def busy_window_bound_nps(all_tasks: TaskSet, task_under_analysis: Task) -> Duration:
    """A bound on the length of a busy interval that starts with priority inversion
    (w.r.t. a job of a given task under analysis) under the EDF scheduling policy."""

    def lp_interference(tsk_lp: Task) -> Work:
        return tsk_lp.execution.max_non_preemptive_segment - EPSILON_TIME

    def hep_interference(tsk_lp: Task) -> Work:
        dl_lp = deadline_of(tsk_lp).value
        return sum(
            tsk_hp.rbf(dl_lp - deadline_of(tsk_hp).value)
            for tsk_hp in all_tasks.with_deadline_at_most_iter(tsk_lp)
        )

    return max(
        (
            lp_interference(t) + hep_interference(t)
            for t in all_tasks.with_deadline_greater_than_iter(task_under_analysis)
        ),
        default=0,
    )


def busy_window_bound_rbf(
    all_tasks: TaskSet,
    supply: SupplyModel,
    horizon: Duration | None = None,
) -> Duration | None:
    return solve.inequality(lhs=all_tasks.rbf, rhs=supply, horizon=horizon)


def busy_window_bound(
    all_tasks: TaskSet,
    task_under_analysis: Task,
    supply: SupplyModel,
    horizon: Duration | None = None,
) -> Duration | None:
    "A bound on the length of the busy window of any job of the task under analysis."
    if isinstance(supply, IdealProcessor):
        # On an ideal uniprocessor without supply restrictions,
        # we can be less pessimistic about the blocking bound.
        return busy_window_bound_rbf(all_tasks, supply, horizon)
    else:
        bw_nps = busy_window_bound_nps(all_tasks, task_under_analysis)
        bw_rbf = busy_window_bound_rbf(all_tasks, supply, horizon)
        return max(bw_nps, bw_rbf) if bw_rbf is not None else None


# This is a good candidate for an LRU cache.
def blocking_bound(
    all_tasks: TaskSet, task_under_analysis: Task, offset: Duration
) -> Work:
    """A bound on the maximum priority-inversion blocking incurred by a job of the task
    under analysis if it arrives offset time units after the beginning of its busy window."""

    reference = Deadline(offset + deadline_of(task_under_analysis).value)

    return max(
        (
            t.execution.max_non_preemptive_segment - EPSILON_TIME
            for t in all_tasks.with_deadline_greater_than_iter(reference)
            if t.rbf(EPSILON_TIME) > 0
        ),
        default=0,
    )


def blocking_bound_steps(
    all_tasks: TaskSet, task_under_analysis: Task
) -> Iterator[Duration]:
    """
    Yields all positive offsets where the blocking bound changes its value:
        blocking_bound(all_tasks, task_under_analysis, offset)
        != blocking_bound(all_tasks, task_under_analysis, offset - 1)

    These are the boundary offsets o such that:
        o + D_u == D_k
    for some task k in all_tasks, where D_u is the deadline of the task under analysis.
    """
    reference = deadline_of(task_under_analysis)

    possible_offsets = (
        deadline_of(t).value - reference.value
        for t in all_tasks
        if t != task_under_analysis
    )

    return (
        offset
        for offset in sorted(possible_offsets)
        if offset > 0
        and (
            blocking_bound(all_tasks, task_under_analysis, offset - EPSILON_TIME)
            != blocking_bound(all_tasks, task_under_analysis, offset)
        )
    )


def points_of_interest(
    all_tasks: TaskSet,
    task_under_analysis: Task,
    supply: SupplyModel,
) -> Iterator[Duration]:
    "The points at which the per-offset response-time bound must be computed."

    def poi(to: Task) -> Iterator[Duration]:
        t_dl = deadline_of(task_under_analysis).value
        to_dl = deadline_of(to).value
        shifted = (pt - t_dl + to_dl for pt in to.rbf.steps())
        return dropwhile(lambda pt: pt < 0, shifted)

    if isinstance(supply, IdealProcessor):
        # On an ideal uniprocessor without supply restrictions,
        # we do not have not consider points at which the blocking
        # bound changes.
        return merge_sorted_unique(
            [task_under_analysis.rbf.steps()]
            + [poi(to) for to in all_tasks.excluding_iter(task_under_analysis)]
        )
    else:
        return merge_sorted_unique(
            [
                blocking_bound_steps(all_tasks, task_under_analysis),
                task_under_analysis.rbf.steps(),
            ]
            + [poi(to) for to in all_tasks.excluding_iter(task_under_analysis)]
        )


def search_space(
    all_tasks: TaskSet,
    task_under_analysis: Task,
    supply: SupplyModel,
    horizon: Duration | None = None,
    bw_bound: Duration | None = None,
) -> Iterator[Duration] | None:
    "The finite, sparse search space for EDF RTA."

    L = (
        busy_window_bound(all_tasks, task_under_analysis, supply, horizon)
        if bw_bound is None
        else bw_bound
    )

    return sparse_finite_search_space(
        points_of_interest(all_tasks, task_under_analysis, supply), L
    )


def poet_search_space(
    all_tasks: TaskSet,
    tua: Task,
    supply: SupplyModel,
    L: Duration,
) -> Iterator[Duration]:
    "The over-approximated search space used in POET's EDF RTA."

    # This search space is special-cased to ideal uniprocessors and does
    # not work with arbitrary supply restrictions.
    assert isinstance(supply, IdealProcessor)

    for tsko in all_tasks:
        tua_dl = deadline_of(tua).value
        tsko_dl = deadline_of(tsko).value
        # round to next horizon multiple
        # ((L + (task_deadline tsk - task_deadline tsko)) %/ h).+1.
        if isinstance(tsko.arrivals, ArrivalCurvePrefix):
            h = tsko.arrivals.horizon
            dl_diff = max(0, tua_dl - tsko_dl)
            upper_bound = ((L + dl_diff) // h + 1) * h
        else:
            upper_bound = L

        for pt in tsko.rbf.steps():
            if pt < upper_bound:
                if pt + 1 + tsko_dl >= tua_dl:
                    yield max(0, pt - tua_dl + tsko_dl)
            else:
                break


def rta(
    all_tasks: TaskSet,
    task_under_analysis: Task,
    supply: SupplyModel,
    horizon: Duration | None = None,
    # special case for POET's over-approximated search spaces -- works only for ArrivalCurvePrefix
    use_poet_search_space: bool = False,
) -> Solution:
    "Response-time analysis for uniprocessor earliest-deadline first (EDF) scheduling."

    assert not all_tasks.is_empty()

    # first, define the RTA inequality for a given offset
    def rta_for_offset(
        A: Duration,
    ) -> tuple[Duration, Duration | None, Duration | None]:
        bb = blocking_bound(all_tasks, task_under_analysis, A)

        other_tasks = all_tasks.excluding(task_under_analysis)

        hep_reference = A + EPSILON_TIME + deadline_of(task_under_analysis).value

        def hep_bound(delta: Duration) -> Work:
            return sum(
                t.rbf(min(hep_reference - deadline_of(t).value, delta))
                for t in other_tasks
            )

        tua_work = task_under_analysis.rbf(A + EPSILON_TIME) - (
            task_under_analysis.cost.value
            - task_under_analysis.execution.run_to_completion_threshold
        )

        F = solve.inequality(
            lhs=lambda F: bb + tua_work + hep_bound(F),
            rhs=supply,
            start=bb + tua_work,
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

    # second, try to obtain the search space of relevant offsets
    L = busy_window_bound(all_tasks, task_under_analysis, supply, horizon)
    if L is None:
        return Solution.no_search_space_found(all_tasks, task_under_analysis)

    if use_poet_search_space:
        sp = poet_search_space(all_tasks, task_under_analysis, supply, L)
    else:
        sp = search_space(all_tasks, task_under_analysis, supply, horizon, L)
    if sp is None:
        return Solution.no_search_space_found(all_tasks, task_under_analysis)

    # finally, analyze each element of the search space
    sp = tuple(rta_for_offset(A) for A in sp)

    return Solution.from_search_space(all_tasks, task_under_analysis, L, sp)
