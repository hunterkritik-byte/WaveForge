# Headless benchmark mode

WaveForge can run a deterministic simulation without opening the Matplotlib dashboard. This is useful for automated experiments, CI checks, and comparing parameter sets.

```python
from src.benchmark import run_benchmark

metrics = run_benchmark(steps=100)
print(metrics["delivery_rate"])
```

The returned dictionary contains the same core telemetry exposed by `Simulation.telemetry()`, plus the number of executed steps.

The benchmark remains software-only and never accesses physical wireless hardware.
