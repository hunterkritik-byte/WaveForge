# Benchmark CLI

Run a headless benchmark directly from the command line:

```bash
python main.py --benchmark 100
```

The command prints a JSON telemetry snapshot instead of opening the graphical dashboard. Use the normal simulation options alongside it to compare scenarios, for example:

```bash
python main.py --benchmark 500 --scenario crowded
```

This feature is intended for reproducible experiments and CI-friendly measurements. It remains software-only.
