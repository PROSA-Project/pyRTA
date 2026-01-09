from response_time_analysis.analysis import edf, fifo, fp
from response_time_analysis.model import (
    WCET,
    ArrivalCurvePrefix,
    Deadline,
    FloatingNonPreemptive,
    FullyNonPreemptive,
    FullyPreemptive,
    IdealProcessor,
    LimitedPreemptive,
    MinimumSeparationVector,
    Periodic,
    PeriodicWithJitter,
    Priority,
    RateDelayModel,
    Sporadic,
    Task,
    taskset,
)


def background_tasks() -> tuple[Task, ...]:
    return (
        Task(
            arrivals=Periodic(11),
            execution=FullyPreemptive(WCET(1)),
            deadline=Deadline(18),
            priority=Priority(8),
        ),
        Task(
            arrivals=Periodic(16),
            execution=FullyNonPreemptive(WCET(2)),
            deadline=Deadline(30),
            priority=Priority(2),
        ),
    )


def test_periodic_fully_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Periodic(7),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_periodic_fully_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Periodic(7),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_periodic_fully_preemptive_ideal_earliest_deadline_first() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Periodic(7),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_periodic_fully_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Periodic(7),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_fully_preemptive_rate_delay_fixed_priority() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Periodic(7),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_fully_preemptive_rate_delay_earliest_deadline_first() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Periodic(7),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_fully_non_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Periodic(7),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_periodic_fully_non_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Periodic(7),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_periodic_fully_non_preemptive_ideal_earliest_deadline_first() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Periodic(7),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_periodic_fully_non_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Periodic(7),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_fully_non_preemptive_rate_delay_fixed_priority() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Periodic(7),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_fully_non_preemptive_rate_delay_earliest_deadline_first() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Periodic(7),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_floating_non_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Periodic(7),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_periodic_floating_non_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Periodic(7),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_periodic_floating_non_preemptive_ideal_earliest_deadline_first() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Periodic(7),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_periodic_floating_non_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Periodic(7),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_floating_non_preemptive_rate_delay_fixed_priority() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Periodic(7),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_floating_non_preemptive_rate_delay_earliest_deadline_first() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Periodic(7),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_limited_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Periodic(7),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_periodic_limited_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Periodic(7),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_periodic_limited_preemptive_ideal_earliest_deadline_first() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Periodic(7),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_periodic_limited_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Periodic(7),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_limited_preemptive_rate_delay_fixed_priority() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Periodic(7),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_limited_preemptive_rate_delay_earliest_deadline_first() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Periodic(7),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_with_jitter_fully_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_periodic_with_jitter_fully_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_periodic_with_jitter_fully_preemptive_ideal_earliest_deadline_first() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_periodic_with_jitter_fully_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_with_jitter_fully_preemptive_rate_delay_fixed_priority() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_with_jitter_fully_preemptive_rate_delay_earliest_deadline_first() -> (
    None
):
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_with_jitter_fully_non_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_periodic_with_jitter_fully_non_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_periodic_with_jitter_fully_non_preemptive_ideal_earliest_deadline_first() -> (
    None
):
    supply = IdealProcessor()
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_periodic_with_jitter_fully_non_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_with_jitter_fully_non_preemptive_rate_delay_fixed_priority() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_with_jitter_fully_non_preemptive_rate_delay_earliest_deadline_first() -> (
    None
):
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_with_jitter_floating_non_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_periodic_with_jitter_floating_non_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_periodic_with_jitter_floating_non_preemptive_ideal_earliest_deadline_first() -> (
    None
):
    supply = IdealProcessor()
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_periodic_with_jitter_floating_non_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_with_jitter_floating_non_preemptive_rate_delay_fixed_priority() -> (
    None
):
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_with_jitter_floating_non_preemptive_rate_delay_earliest_deadline_first() -> (
    None
):
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_with_jitter_limited_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_periodic_with_jitter_limited_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_periodic_with_jitter_limited_preemptive_ideal_earliest_deadline_first() -> (
    None
):
    supply = IdealProcessor()
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_periodic_with_jitter_limited_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_with_jitter_limited_preemptive_rate_delay_fixed_priority() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_periodic_with_jitter_limited_preemptive_rate_delay_earliest_deadline_first() -> (
    None
):
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=PeriodicWithJitter(7, 1),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_sporadic_fully_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Sporadic(8),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_sporadic_fully_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Sporadic(8),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_sporadic_fully_preemptive_ideal_earliest_deadline_first() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Sporadic(8),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_sporadic_fully_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Sporadic(8),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_sporadic_fully_preemptive_rate_delay_fixed_priority() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Sporadic(8),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_sporadic_fully_preemptive_rate_delay_earliest_deadline_first() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Sporadic(8),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_sporadic_fully_non_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Sporadic(8),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_sporadic_fully_non_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Sporadic(8),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_sporadic_fully_non_preemptive_ideal_earliest_deadline_first() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Sporadic(8),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_sporadic_fully_non_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Sporadic(8),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_sporadic_fully_non_preemptive_rate_delay_fixed_priority() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Sporadic(8),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_sporadic_fully_non_preemptive_rate_delay_earliest_deadline_first() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Sporadic(8),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_sporadic_floating_non_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Sporadic(8),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_sporadic_floating_non_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Sporadic(8),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_sporadic_floating_non_preemptive_ideal_earliest_deadline_first() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Sporadic(8),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_sporadic_floating_non_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Sporadic(8),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_sporadic_floating_non_preemptive_rate_delay_fixed_priority() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Sporadic(8),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_sporadic_floating_non_preemptive_rate_delay_earliest_deadline_first() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Sporadic(8),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_sporadic_limited_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Sporadic(8),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_sporadic_limited_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Sporadic(8),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_sporadic_limited_preemptive_ideal_earliest_deadline_first() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=Sporadic(8),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_sporadic_limited_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Sporadic(8),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_sporadic_limited_preemptive_rate_delay_fixed_priority() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Sporadic(8),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_sporadic_limited_preemptive_rate_delay_earliest_deadline_first() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=Sporadic(8),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_min_separation_vector_fully_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_min_separation_vector_fully_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_min_separation_vector_fully_preemptive_ideal_earliest_deadline_first() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_min_separation_vector_fully_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_min_separation_vector_fully_preemptive_rate_delay_fixed_priority() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_min_separation_vector_fully_preemptive_rate_delay_earliest_deadline_first() -> (
    None
):
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_min_separation_vector_fully_non_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_min_separation_vector_fully_non_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_min_separation_vector_fully_non_preemptive_ideal_earliest_deadline_first() -> (
    None
):
    supply = IdealProcessor()
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_min_separation_vector_fully_non_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_min_separation_vector_fully_non_preemptive_rate_delay_fixed_priority() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_min_separation_vector_fully_non_preemptive_rate_delay_earliest_deadline_first() -> (
    None
):
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_min_separation_vector_floating_non_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_min_separation_vector_floating_non_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_min_separation_vector_floating_non_preemptive_ideal_earliest_deadline_first() -> (
    None
):
    supply = IdealProcessor()
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_min_separation_vector_floating_non_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_min_separation_vector_floating_non_preemptive_rate_delay_fixed_priority() -> (
    None
):
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_min_separation_vector_floating_non_preemptive_rate_delay_earliest_deadline_first() -> (
    None
):
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_min_separation_vector_limited_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_min_separation_vector_limited_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_min_separation_vector_limited_preemptive_ideal_earliest_deadline_first() -> (
    None
):
    supply = IdealProcessor()
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_min_separation_vector_limited_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_min_separation_vector_limited_preemptive_rate_delay_fixed_priority() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_min_separation_vector_limited_preemptive_rate_delay_earliest_deadline_first() -> (
    None
):
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=MinimumSeparationVector([5, 11, 17, 23, 29]),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_arrival_curve_prefix_fully_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_arrival_curve_prefix_fully_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_arrival_curve_prefix_fully_preemptive_ideal_earliest_deadline_first() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_arrival_curve_prefix_fully_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_arrival_curve_prefix_fully_preemptive_rate_delay_fixed_priority() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_arrival_curve_prefix_fully_preemptive_rate_delay_earliest_deadline_first() -> (
    None
):
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=FullyPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_arrival_curve_prefix_fully_non_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_arrival_curve_prefix_fully_non_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_arrival_curve_prefix_fully_non_preemptive_ideal_earliest_deadline_first() -> (
    None
):
    supply = IdealProcessor()
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_arrival_curve_prefix_fully_non_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_arrival_curve_prefix_fully_non_preemptive_rate_delay_fixed_priority() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_arrival_curve_prefix_fully_non_preemptive_rate_delay_earliest_deadline_first() -> (
    None
):
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=FullyNonPreemptive(WCET(1)),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_arrival_curve_prefix_floating_non_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_arrival_curve_prefix_floating_non_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_arrival_curve_prefix_floating_non_preemptive_ideal_earliest_deadline_first() -> (
    None
):
    supply = IdealProcessor()
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_arrival_curve_prefix_floating_non_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_arrival_curve_prefix_floating_non_preemptive_rate_delay_fixed_priority() -> (
    None
):
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_arrival_curve_prefix_floating_non_preemptive_rate_delay_earliest_deadline_first() -> (
    None
):
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=FloatingNonPreemptive(WCET(2), max_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_arrival_curve_prefix_limited_preemptive_ideal_fifo() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply)
    assert solution.bound_found()


def test_arrival_curve_prefix_limited_preemptive_ideal_fixed_priority() -> None:
    supply = IdealProcessor()
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply)
    assert solution.bound_found()


def test_arrival_curve_prefix_limited_preemptive_ideal_earliest_deadline_first() -> (
    None
):
    supply = IdealProcessor()
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply)
    assert solution.bound_found()


def test_arrival_curve_prefix_limited_preemptive_rate_delay_fifo() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fifo.rta(ts, supply, horizon=1)
    assert not solution.bound_found()


def test_arrival_curve_prefix_limited_preemptive_rate_delay_fixed_priority() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = fp.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()


def test_arrival_curve_prefix_limited_preemptive_rate_delay_earliest_deadline_first() -> (
    None
):
    supply = RateDelayModel(period=10, allocation=7, delay=2)
    tua = Task(
        arrivals=ArrivalCurvePrefix(horizon=6, ac_steps=[(1, 1), (3, 2)]),
        execution=LimitedPreemptive(WCET(2), max_nps=1, last_nps=1),
        deadline=Deadline(15),
        priority=Priority(5),
    )
    ts = taskset((tua,) + background_tasks())
    solution = edf.rta(ts, tua, supply, horizon=1)
    assert not solution.bound_found()
