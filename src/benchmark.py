"""Headless benchmarking helpers for reproducible simulations."""
from __future__ import annotations

from typing import Dict

from .simulator import Simulation, SimulationConfig


def run_benchmark(steps: int, config: SimulationConfig = None) -> Dict[str, float]:
    """Run *steps* without opening the Matplotlib dashboard and return telemetry."""
    if steps <= 0:
        raise ValueError("steps must be positive")
    simulation = Simulation(config)
    for _ in range(steps):
        simulation.step()
    result = simulation.telemetry()
    result["steps"] = float(steps)
    return result
