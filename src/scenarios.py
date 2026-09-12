"""Portable scenario profiles for repeatable WaveForge experiments.

Scenario files are intentionally hardware-agnostic: they describe simulated
nodes, channel conditions, and run parameters without opening radio devices.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Scenario:
    """A validated, serializable simulation scenario."""

    name: str
    seed: int = 7
    steps: int = 100
    clients: int = 3
    block_probability: float = 0.06
    notes: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("scenario name must not be empty")
        if self.steps < 0:
            raise ValueError("steps must be >= 0")
        if self.clients <= 0:
            raise ValueError("clients must be positive")
        if not 0.0 <= self.block_probability <= 1.0:
            raise ValueError("block_probability must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["tags"] = list(self.tags)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Scenario":
        allowed = {"name", "seed", "steps", "clients", "block_probability", "notes", "tags"}
        unknown = set(data) - allowed
        if unknown:
            raise ValueError(f"unknown scenario fields: {', '.join(sorted(unknown))}")
        return cls(tags=tuple(data.get("tags", ())), **{k: v for k, v in data.items() if k != "tags"},)


PRESETS = {
    "baseline": Scenario(
        name="baseline", seed=7, steps=100, clients=3,
        block_probability=0.06, notes="Default Bluetooth/Wi-Fi teaching scenario", tags=("demo", "baseline"),
    ),
    "dense-interference": Scenario(
        name="dense-interference", seed=42, steps=250, clients=8,
        block_probability=0.22, notes="Stress test for channel contention", tags=("stress", "interference"),
    ),
    "low-power": Scenario(
        name="low-power", seed=1337, steps=250, clients=4,
        block_probability=0.10, notes="Repeatable low-interference efficiency study", tags=("power", "efficiency"),
    ),
}


def get_preset(name: str) -> Scenario:
    try:
        return PRESETS[name]
    except KeyError as exc:
        raise ValueError(f"unknown scenario preset: {name}") from exc


def load(path: str | Path) -> Scenario:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("scenario file must contain a JSON object")
    return Scenario.from_dict(payload)


def save(scenario: Scenario, path: str | Path) -> None:
    Path(path).write_text(json.dumps(scenario.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
