import pytest

from src.experiments import compare_histories, run_experiment, summarize_history
from src.simulator import Simulation, SimulationConfig


def test_run_experiment_captures_each_tick():
    simulation = Simulation(SimulationConfig(seed=42))
    history = run_experiment(simulation, 5)

    assert len(history) == 5
    assert [row["tick"] for row in history] == [1.0, 2.0, 3.0, 4.0, 5.0]
    assert history[-1]["delivered"] + history[-1]["dropped"] == 5.0


def test_same_seed_produces_same_history():
    config = SimulationConfig(seed=42, channel_block_probability=0.2, client_count=2)
    left = run_experiment(Simulation(config), 10)
    right = run_experiment(Simulation(config), 10)

    assert left == right


def test_summary_and_comparison():
    baseline = run_experiment(Simulation(SimulationConfig(seed=1)), 4)
    candidate = run_experiment(Simulation(SimulationConfig(seed=2)), 4)

    summary = summarize_history(candidate)
    delta = compare_histories(baseline, candidate)

    assert summary["steps"] == 4.0
    assert 0.0 <= summary["final_delivery_rate"] <= 100.0
    assert set(delta) == {
        "delta_delivery_rate",
        "delta_avg_latency_ms",
        "delta_avg_rssi_dbm",
        "delta_delivered",
        "delta_dropped",
    }


def test_empty_and_invalid_inputs():
    assert summarize_history([])["steps"] == 0.0
    with pytest.raises(ValueError):
        run_experiment(Simulation(), -1)
    with pytest.raises(ValueError):
        compare_histories([], [{"tick": 1.0}])
