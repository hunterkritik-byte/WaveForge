# Scenario presets

WaveForge includes reusable presets for common educational experiments. Each preset is deterministic and can be overridden from the command line.

## Baseline

```bash
python main.py --scenario baseline
```

A balanced configuration for demonstrations.

## Crowded

```bash
python main.py --scenario crowded
```

Uses more simulated Wi-Fi clients and a higher interference probability to make channel pressure more visible.

## Quiet

```bash
python main.py --scenario quiet
```

Uses low simulated interference and fewer clients for a clean baseline.

## Override a preset

Command-line options override the selected preset. For example:

```bash
python main.py --scenario crowded --block-probability 0.10 --clients 5
```

These scenarios are software-only. They do not access, transmit through, scan, or interfere with physical wireless hardware.
