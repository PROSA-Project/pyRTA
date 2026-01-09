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
