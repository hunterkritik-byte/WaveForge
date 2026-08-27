# ⚡ WaveForge

**Software-only wireless network simulator for exploring Bluetooth Adaptive Frequency Hopping and Wi-Fi IP routing.**

WaveForge turns wireless concepts into an interactive simulation without radio hardware or physical network access. It models protocol behavior, interference, attenuation, routing, latency, delivery rate, RSSI, and power as software-only abstractions. The original project concept contrasts Bluetooth 79-channel AFH with Wi-Fi hub-and-spoke routing.

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
- Built-in `baseline`, `crowded`, and `quiet` scenario presets
- Moving Bluetooth nodes
- Wi-Fi hub-and-spoke topology
- Signal attenuation model
- Simulated environmental noise
- Packet-delivery and latency telemetry
- Average RSSI telemetry
- Comparative power-consumption telemetry
- Deterministic runs for reproducible experiments

### Developer experience
- Modular `src/` architecture
- Python 3.9+ compatible typing
- Type hints and docstrings
- Pytest regression suite
- GitHub Actions on Python 3.9–3.12
- No compiled binaries or physical-radio dependencies

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
                    Matplotlib Dashboard
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

The dashboard accepts reproducible runtime controls:

```bash
python main.py --seed 42 --fps 30 --block-probability 0.08 --clients 5
```

Or select a built-in scenario:

```bash
python main.py --scenario crowded
```

Scenario details are documented separately in [`docs/scenarios.md`](docs/scenarios.md).

- `--seed`: deterministic simulation seed
- `--fps`: dashboard update rate
- `--block-probability`: per-channel simulated interference probability from `0` to `1`
- `--clients`: number of simulated Wi-Fi clients
- `--scenario`: `baseline`, `crowded`, or `quiet`

Run tests:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## 📊 Telemetry API

The `Simulation` object exposes a lightweight `telemetry()` snapshot for experiments and tests:

```python
from src.simulator import Simulation

sim = Simulation()
for _ in range(10):
    sim.step()

print(sim.telemetry())
```

The snapshot includes delivery rate, delivered/dropped packets, average latency, average RSSI, and accumulated Bluetooth/Wi-Fi power units.

## 📁 Project layout

```text
WaveForge/
├── .github/workflows/python-app.yml
├── docs/
│   └── scenarios.md
├── src/
│   ├── __init__.py
│   ├── engine.py
│   ├── scenarios.py
│   ├── simulator.py
│   └── utils.py
├── tests/
│   ├── test_engine.py
│   └── test_scenarios.py
├── main.py
├── requirements.txt
├── requirements-dev.txt
├── LICENSE
└── README.md
```

## 📐 Modeling notes

The physics in WaveForge is intentionally educational rather than a standards-compliant RF propagation simulator. The attenuation helper uses a simplified inverse-power model, and the RSSI helper uses a log-distance approximation. Packet delivery uses the resulting signal factor and simulated channel availability. Power values are simulation units rather than measurements from real hardware.

## 🛡️ Safety boundary

WaveForge is a **simulation-only** project. It does not access wireless interfaces, capture real frames, transmit packets, perform deauthentication, jam frequencies, scan nearby networks, or interfere with third-party systems. It is intended for education, visualization, algorithm development, and deterministic testing.

## 📜 License

MIT
