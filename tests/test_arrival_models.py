from itertools import islice

from response_time_analysis.model import (
    ArrivalCurvePrefix,
    MinimumSeparationVector,
    Periodic,
    PeriodicWithJitter,
    Sporadic,
)


def test_periodic_arrivals_counts() -> None:
    am = Periodic(period=5)

    assert am.max_arrivals(-1) == 0
    assert am.max_arrivals(0) == 0
    assert am.max_arrivals(1) == 1
    assert am.max_arrivals(5) == 1
    assert am.max_arrivals(6) == 2
    assert am.max_arrivals(15) == 3
    assert am.max_arrivals(16) == 4


def test_periodic_with_jitter_arrivals_counts() -> None:
    am = PeriodicWithJitter(period=5, jitter=2)

    assert am.max_arrivals(0) == 0
    assert am.max_arrivals(1) == 1
    assert am.max_arrivals(3) == 1
    assert am.max_arrivals(4) == 2
    assert am.max_arrivals(5) == 2
    assert am.max_arrivals(9) == 3


def test_sporadic_arrivals_counts() -> None:
    am = Sporadic(mit=4)

    assert am.max_arrivals(0) == 0
    assert am.max_arrivals(1) == 1
    assert am.max_arrivals(4) == 1
    assert am.max_arrivals(5) == 2
    assert am.max_arrivals(12) == 3
    assert am.max_arrivals(13) == 4


def test_minimum_separation_vector_counts_with_extrapolation() -> None:
    am = MinimumSeparationVector(dmin=[2, 5, 9, 14, 20, 26])

    assert am.max_arrivals(0) == 0
    assert am.max_arrivals(2) == 1
    assert am.max_arrivals(3) == 2
    assert am.max_arrivals(9) == 3
    assert am.max_arrivals(10) == 4
    assert am.max_arrivals(20) == 5
    assert am.max_arrivals(25) == 6
    assert am.max_arrivals(26) == 6
    assert am.max_arrivals(27) == 7
    assert am.max_arrivals(30) == 8


def test_arrival_curve_prefix_counts_across_windows() -> None:
    ac_steps = [
        (1, 1),
        (21, 2),
        (51, 3),
        (91, 4),
    ]
    am = ArrivalCurvePrefix(horizon=100, ac_steps=ac_steps)

    assert am.max_arrivals(0) == 0
    assert am.max_arrivals(1) == 1
    assert am.max_arrivals(20) == 1
    assert am.max_arrivals(21) == 2
    assert am.max_arrivals(50) == 2
    assert am.max_arrivals(51) == 3
    assert am.max_arrivals(90) == 3
    assert am.max_arrivals(91) == 4
    assert am.max_arrivals(100) == 4
    assert am.max_arrivals(101) == 5
    assert am.max_arrivals(120) == 5
    assert am.max_arrivals(121) == 6
    assert am.max_arrivals(150) == 6
    assert am.max_arrivals(151) == 7
    assert am.max_arrivals(190) == 7
    assert am.max_arrivals(191) == 8
    assert am.max_arrivals(200) == 8
    assert am.max_arrivals(201) == 9


def test_periodic_as_arrival_curve_prefix_equivalence() -> None:
    am = Periodic(period=5)

    prefix = am.as_arrival_curve_prefix()

    assert prefix.horizon == 5
    assert prefix.ac_steps == [(1, 1)]
    for delta in range(26):
        assert prefix.max_arrivals(delta) == am.max_arrivals(delta)


def test_periodic_delta_min_equivalence() -> None:
    am = Periodic(period=5)

    am_dmin = MinimumSeparationVector([5])

    for delta in range(26):
        assert am_dmin(delta) == am(delta)

    for s_dmin, s in islice(zip(am_dmin.steps(), am.steps()), 10):
        assert s_dmin == s


def test_sporadic_as_arrival_curve_prefix_equivalence() -> None:
    am = Sporadic(mit=4)

    prefix = am.as_arrival_curve_prefix()

    assert prefix.horizon == 4
    assert prefix.ac_steps == [(1, 1)]
    for delta in range(26):
        assert prefix.max_arrivals(delta) == am.max_arrivals(delta)


def test_periodic_with_jitter_as_arrival_curve_prefix_default_horizon() -> None:
    am = PeriodicWithJitter(period=5, jitter=2)

    prefix = am.as_arrival_curve_prefix()

    assert prefix.horizon == 50
    assert prefix.ac_steps == [
        (1, 1),
        (4, 2),
        (9, 3),
        (14, 4),
        (19, 5),
        (24, 6),
        (29, 7),
        (34, 8),
        (39, 9),
        (44, 10),
        (49, 11),
    ]
    for delta in range(51):
        assert prefix.max_arrivals(delta) == am.max_arrivals(delta)


def test_minimum_separation_vector_as_arrival_curve_prefix() -> None:
    am = MinimumSeparationVector(dmin=[2, 5, 9, 14, 20, 26])

    prefix = am.as_arrival_curve_prefix()

    assert prefix.horizon == 26
    assert prefix.ac_steps == [
        (1, 1),
        (3, 2),
        (6, 3),
        (10, 4),
        (15, 5),
        (21, 6),
    ]
    for delta in range(26):
        assert prefix.max_arrivals(delta) == am.max_arrivals(delta)


def test_arrival_curve_prefix_as_arrival_curve_prefix_noop() -> None:
    ac = ArrivalCurvePrefix(horizon=100, ac_steps=[(1, 1)])

    assert ac.as_arrival_curve_prefix(50) is ac
