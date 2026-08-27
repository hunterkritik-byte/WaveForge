"""Telemetry history and CSV export for software-only simulations."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Union


class TelemetryRecorder:
    """Collect simulation snapshots and export them as portable CSV data."""

    def __init__(self) -> None:
        self.rows: List[Dict[str, float]] = []

    def record(self, snapshot: Dict[str, float]) -> None:
        """Append a copy of a telemetry snapshot."""
        self.rows.append(dict(snapshot))

    def export_csv(self, path: Union[str, Path]) -> Path:
        """Write recorded snapshots to *path* and return the resulting path."""
        if not self.rows:
            raise ValueError("cannot export empty telemetry history")
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = list(self.rows[0])
        with destination.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.rows)
        return destination

    def __len__(self) -> int:
        return len(self.rows)
