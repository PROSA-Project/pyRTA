from collections.abc import Iterator
from math import floor
from random import choice, getstate, randint, random, seed, setstate, uniform

from response_time_analysis.analysis import edf, fifo, fp
from response_time_analysis.model import (
    WCET,
    ArrivalCurvePrefix,
    Deadline,
    Duration,
    FullyPreemptive,
    IdealProcessor,
    MinimumSeparationVector,
    Periodic,
    PeriodicWithJitter,
    Priority,
    RateDelayModel,
    Sporadic,
    Task,
    TaskSet,
    taskset,
)

SEEDS = (
    hash("Liu"),
    hash("Layland"),
    hash("Stankovic"),
    hash("Sha"),
    hash("Mok"),
    hash("Burns"),
    hash("Baruah"),
    hash("Anderson"),
    hash("Buttazzo"),
    hash("Rajkumar"),
)
TASK_SETS_PER_SEED = 5
TOTAL_TASK_SETS = len(SEEDS) * TASK_SETS_PER_SEED
TARGET_UTILIZATION = 0.7
ROUND_PERIODS = [10, 25, 50, 100, 250, 500, 1000]

PERIODIC = 0.4
ROUND_PERIOD = 0.5
SPORADIC = 0.2
JITTER = 0.7
DELTA_MIN = 0.1


def maybe(threshold: float) -> bool:
    return random() <= threshold


def draw_period() -> int:
    if maybe(ROUND_PERIOD):
        return choice(ROUND_PERIODS)
    else:
        return randint(10, 1000)


def draw_task(util: float) -> Task:
    if maybe(PERIODIC):
        if maybe(JITTER):
            am = PeriodicWithJitter(period=draw_period(), jitter=randint(1, 1000))
            h = am.period
            n = 1
        else:
            am = Periodic(draw_period())
            h = am.period
            n = 1
    elif maybe(SPORADIC):
        am = Sporadic(randint(10, 1000))
        h = am.mit
        n = 1
    elif maybe(DELTA_MIN):
        gap: Duration = randint(3, 25)
        dmin: list[Duration] = []
        for _ in range(randint(5, 20)):
            dmin.append(gap)
            gap += randint(25, 50)
        am = MinimumSeparationVector(dmin)
        n = am.max_covered_njobs
        h = am.max_covered_delta
    else:
        steps = [(1, 1)]
        gap = randint(3, 20)
        for _ in range(randint(2, 20)):
            last = steps[-1]
            steps.append((last[0] + gap, last[1] + 1))
            gap += randint(0, 10)
        h = steps[-1][0] + randint(50, 100)
        n = steps[-1][1]
        am = ArrivalCurvePrefix(horizon=h, ac_steps=steps)
    wcet = WCET(max(1, int(floor(h * util / n))))
    return Task(
        execution=FullyPreemptive(wcet),
        arrivals=am,
        priority=Priority(randint(0, 100)),
        deadline=Deadline(int(h * uniform(0.5, 1.5))),
    )


def draw_task_set(target: float) -> TaskSet:
    n = randint(2, 10)
    utils = [uniform(0.1, 0.5) for _ in range(n)]
    scale = target / sum(utils)
    return taskset(draw_task(u * scale) for u in utils)


def iter_random_task_sets(
    target_utilization: float = TARGET_UTILIZATION,
) -> Iterator[TaskSet]:
    """Yield a deterministic set of randomly generated task sets."""
    state = getstate()
    try:
        for seed_value in SEEDS:
            seed(seed_value)
            for _ in range(TASK_SETS_PER_SEED):
                yield draw_task_set(target_utilization)
    finally:
        setstate(state)


THREE_YEARS_IN_NANOSECONDS = 10**17


def test_fp_rta_for_random_workloads() -> None:
    supply = IdealProcessor()
    total_sets = 0

    for ts in iter_random_task_sets():
        total_sets += 1
        for task in ts:
            solution = fp.rta(ts, task, supply, horizon=THREE_YEARS_IN_NANOSECONDS)
            assert solution.bound_found()

    assert total_sets == TOTAL_TASK_SETS


def test_edf_rta_for_random_workloads() -> None:
    supply = IdealProcessor()
    total_sets = 0

    for ts in iter_random_task_sets():
        total_sets += 1
        for task in ts:
            solution = edf.rta(ts, task, supply, horizon=THREE_YEARS_IN_NANOSECONDS)
            assert solution.bound_found()

    assert total_sets == TOTAL_TASK_SETS


def test_fifo_rta_for_random_workloads() -> None:
    supply = IdealProcessor()
    total_sets = 0

    for ts in iter_random_task_sets():
        total_sets += 1
        solution = fifo.rta(ts, supply, horizon=THREE_YEARS_IN_NANOSECONDS)
        assert solution.bound_found()

    assert total_sets == TOTAL_TASK_SETS


def test_fp_rta_for_random_workloads_rate_delay() -> None:
    supply = RateDelayModel(period=100, allocation=90, delay=50)
    total_sets = 0

    for ts in iter_random_task_sets():
        total_sets += 1
        for task in ts:
            solution = fp.rta(ts, task, supply, horizon=THREE_YEARS_IN_NANOSECONDS)
            assert solution.bound_found()

    assert total_sets == TOTAL_TASK_SETS


def test_fifo_rta_for_random_workloads_rate_delay() -> None:
    supply = RateDelayModel(period=100, allocation=90, delay=50)
    total_sets = 0

    for ts in iter_random_task_sets():
        total_sets += 1
        solution = fifo.rta(ts, supply, horizon=THREE_YEARS_IN_NANOSECONDS)
        assert solution.bound_found()

    assert total_sets == TOTAL_TASK_SETS
