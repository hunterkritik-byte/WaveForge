# ⚡ WaveForge

**Software-only wireless network simulator for exploring Bluetooth Adaptive Frequency Hopping and Wi-Fi IP routing.**

WaveForge turns wireless concepts into an interactive simulation without radio hardware or physical network access. It models protocol behavior, interference, attenuation, routing, latency, delivery rate, RSSI, and power as software-only abstractions.

## ✨ Features

### Bluetooth
- 79-channel Adaptive Frequency Hopping model
- Dynamic simulated interference zones
- Automatic exclusion of blocked channels
- Pairing enforcement
- Packet frequency metadata
- Distance/RSSI educational models
- Simulated delivery decisions based on signal strength and channel availability

### Wi-Fi
- Central router + configurable clients
- IP/MAC routing table
- Deterministic destination lookup
- Packet metadata and topology visualization

### Simulation & telemetry
- Real-time Matplotlib dashboard
- Configurable update rate, seed, interference probability, and client count
- Moving Bluetooth nodes
- Wi-Fi hub-and-spoke topology
- Signal attenuation model
- Simulated environmental noise
- Packet-delivery and latency telemetry
- Average RSSI telemetry
- Comparative power-consumption telemetry
- Deterministic runs for reproducible experiments
- **Headless JSON telemetry mode for CI, notebooks, and regression experiments**
- **Per-step experiment history reports**
- **Aggregate experiment summaries and run-to-run comparison helpers**

### Developer experience
- Modular `src/` architecture
- Python 3.9+ compatible typing
- Type hints and docstrings
- Pytest regression suite
- GitHub Actions on Python 3.9–3.12
- No compiled binaries or physical-radio dependencies

## 🧪 Headless experiment mode

Run the simulation without opening a GUI and emit machine-readable telemetry:

```bash
python main.py --steps 100 --seed 42 --json
```

This makes WaveForge easier to use in automated tests and reproducible experiments. The output contains tick count, delivered/dropped packets, delivery rate, average latency, RSSI, and simulated power units.

### Experiment reports

Capture one telemetry snapshot per simulation step:

```bash
python main.py --steps 100 --seed 42 --report history
```

Get aggregate statistics for a run:

```bash
python main.py --steps 100 --seed 42 --report summary
```

The experiment helpers can also be used from Python:

```python
from src.experiments import compare_histories, run_experiment, summarize_history
from src.simulator import Simulation

baseline = run_experiment(Simulation(seed=42), 100)
candidate = run_experiment(Simulation(seed=43), 100)

print(summarize_history(candidate))
print(compare_histories(baseline, candidate))
```

## 🖥️ Architecture

```text
                         WAVEFORGE
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
       BLUETOOTH MODEL                WI-FI MODEL
              │                           │
       79-channel AFH              Router / IP table
              │                           │
      Interference map            Client destinations
              └─────────────┬─────────────┘
                            ▼
                    Simulation Engine
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
             Physics               Telemetry
                 │                     │
                 └──────────┬──────────┘
                            ▼
                 Dashboard / JSON output
                            │
                     Experiment Reports
```

## 🚀 Quick start

```bash
git clone https://github.com/hunterkritik-byte/WaveForge.git
cd WaveForge
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
python -m pip install -r requirements.txt
python main.py
```

### Configure a run

```bash
python main.py --seed 42 --fps 30 --block-probability 0.08 --clients 5
```

### Run a reproducible headless experiment

```bash
python main.py --seed 42 --steps 500 --json > telemetry.json
```

Run tests:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## 📊 Telemetry API

The `Simulation` object exposes a lightweight `telemetry()` snapshot for experiments and tests:

```python
from src.simulator import Simulation

sim = Simulation(seed=42)
for _ in range(10):
    sim.step()

print(sim.telemetry())
```

The snapshot includes delivery rate, delivered/dropped packets, average latency, average RSSI, and accumulated Bluetooth/Wi-Fi power units.

## 🛡️ Safety boundary

WaveForge is a **simulation-only** project. It does not access wireless interfaces, capture real frames, transmit packets, perform deauthentication, jam frequencies, scan nearby networks, or interfere with third-party systems. It is intended for education, visualization, algorithm development, and deterministic testing.

## 📜 License

MIT
