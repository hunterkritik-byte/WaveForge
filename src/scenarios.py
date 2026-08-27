"""Reusable scenario presets for the software-only simulator."""
from __future__ import annotations

from typing import Dict

from .simulator import SimulationConfig


SCENARIOS: Dict[str, SimulationConfig] = {
    "baseline": SimulationConfig(seed=7, fps=30, channel_block_probability=0.06, client_count=3),
    "crowded": SimulationConfig(seed=19, fps=30, channel_block_probability=0.18, client_count=8),
    "quiet": SimulationConfig(seed=3, fps=20, channel_block_probability=0.01, client_count=2),
}


def get_scenario(name: str) -> SimulationConfig:
    """Return a named immutable scenario configuration."""
    try:
        return SCENARIOS[name]
    except KeyError as exc:
        available = ", ".join(sorted(SCENARIOS))
        raise ValueError(f"unknown scenario {name!r}; choose from: {available}") from exc
