"""Helpers for reproducible headless WaveForge experiments.

The experiment layer stays independent from the dashboard so CI, notebooks,
and scripts can collect per-step telemetry without opening a GUI.
"""
from __future__ import annotations

from statistics import mean
from typing import Any, Dict, List

from .simulator import Simulation


def run_experiment(simulation: Simulation, steps: int) -> List[Dict[str, float]]:
    """Run ``steps`` ticks and return one telemetry snapshot per tick."""
    if steps < 0:
        raise ValueError("steps must be non-negative")

    history: List[Dict[str, float]] = []
    for _ in range(steps):
        simulation.step()
        history.append(dict(simulation.telemetry()))
    return history


def summarize_history(history: List[Dict[str, float]]) -> Dict[str, float]:
    """Return aggregate statistics for a telemetry history."""
    if not history:
        return {
            "steps": 0.0,
            "final_delivery_rate": 0.0,
            "mean_delivery_rate": 0.0,
            "mean_latency_ms": 0.0,
            "mean_rssi_dbm": 0.0,
        }

    def values(key: str) -> List[float]:
        return [float(row[key]) for row in history if key in row]

    delivery = values("delivery_rate")
    latency = values("avg_latency_ms")
    rssi = values("avg_rssi_dbm")
    return {
        "steps": float(len(history)),
        "final_delivery_rate": delivery[-1] if delivery else 0.0,
        "mean_delivery_rate": mean(delivery) if delivery else 0.0,
        "mean_latency_ms": mean(latency) if latency else 0.0,
        "mean_rssi_dbm": mean(rssi) if rssi else 0.0,
    }


def compare_histories(
    baseline: List[Dict[str, float]], candidate: List[Dict[str, float]]
) -> Dict[str, float]:
    """Compare final cumulative telemetry between two runs."""
    if not baseline or not candidate:
        raise ValueError("both histories must contain at least one snapshot")

    keys = ("delivery_rate", "avg_latency_ms", "avg_rssi_dbm", "delivered", "dropped")
    return {
        f"delta_{key}": float(candidate[-1].get(key, 0.0)) - float(baseline[-1].get(key, 0.0))
        for key in keys
    }


def as_jsonable(history: List[Dict[str, float]]) -> List[Dict[str, Any]]:
    """Return a detached JSON-friendly copy of telemetry history."""
    return [dict(row) for row in history]
