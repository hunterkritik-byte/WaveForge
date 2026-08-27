import pytest

from src.benchmark import run_benchmark
from src.simulator import SimulationConfig


def test_benchmark_is_headless_and_deterministic():
    config = SimulationConfig(seed=11)
    first = run_benchmark(10, config)
    second = run_benchmark(10, config)
    assert first == second
    assert first["steps"] == 10.0
    assert first["tick"] == 10.0


def test_benchmark_rejects_non_positive_steps():
    with pytest.raises(ValueError):
        run_benchmark(0)
