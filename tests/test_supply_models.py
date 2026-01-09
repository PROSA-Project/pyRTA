import pytest

from response_time_analysis.model import IdealProcessor, RateDelayModel


def test_ideal_processor_supply_bound_and_call() -> None:
    supply = IdealProcessor()

    assert supply.supply_bound(-5) == 0
    assert supply.supply_bound(0) == 0
    assert supply.supply_bound(4) == 4
    assert supply(2) == 2


def test_ideal_processor_rejects_non_positive_speed() -> None:
    with pytest.raises(ValueError):
        _ = IdealProcessor(speed=0)

    with pytest.raises(ValueError):
        _ = IdealProcessor(speed=-1)


def test_rate_delay_supply_bound_respects_delay_and_period() -> None:
    supply = RateDelayModel(period=10, allocation=7, delay=2)

    assert supply.supply_bound(0) == 0
    assert supply.supply_bound(2) == 0
    assert supply.supply_bound(3) == 0
    assert supply.supply_bound(4) == 1
    assert supply.supply_bound(10) == 5
    assert supply.supply_bound(11) == 6
    assert supply(22) == 14


def test_rate_delay_model_validates_parameters() -> None:
    with pytest.raises(ValueError):
        _ = RateDelayModel(period=0, allocation=1, delay=0)

    with pytest.raises(ValueError):
        _ = RateDelayModel(period=1, allocation=0, delay=0)

    with pytest.raises(ValueError):
        _ = RateDelayModel(period=1, allocation=1, delay=-1)
