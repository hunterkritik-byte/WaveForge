import pytest

from src.scenarios import get_scenario
from src.simulator import Simulation


def test_named_scenarios_are_reproducible():
    config = get_scenario("crowded")
    first = Simulation(config)
    second = Simulation(config)
    for _ in range(4):
        first.step()
        second.step()
    assert first.telemetry() == second.telemetry()
    assert len(first.clients) == 8


def test_unknown_scenario_has_actionable_error():
    with pytest.raises(ValueError, match="baseline"):
        get_scenario("missing")
