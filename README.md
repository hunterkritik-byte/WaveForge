# ⚡ WaveForge

**Software-only wireless network simulator for exploring Bluetooth Adaptive Frequency Hopping and Wi-Fi IP routing.**

WaveForge turns wireless concepts into an interactive simulation without radio hardware or physical network access. It models protocol behavior, interference, attenuation, routing, latency, and power as software-only abstractions. The original project concept contrasts Bluetooth 79-channel AFH with Wi-Fi hub-and-spoke routing.

## ✨ Features

### Bluetooth
- 79-channel Adaptive Frequency Hopping model
- Dynamic simulated interference zones
- Automatic exclusion of blocked channels
- Pairing enforcement
- Packet frequency metadata
- Distance/RSSI educational models

### Wi-Fi
- Central router + multiple clients
- IP/MAC routing table
- Deterministic destination lookup
- Packet metadata and topology visualization

### Simulation & telemetry
- Real-time Matplotlib dashboard
- 30 FPS animation target
- Moving Bluetooth nodes
- Wi-Fi hub-and-spoke topology
- Signal attenuation model
- Simulated environmental noise
- Packet-delivery and latency telemetry
- Comparative power-consumption telemetry

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
              │                           │
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

Run tests:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## 📁 Project layout

```text
WaveForge/
├── .github/workflows/python-app.yml
├── src/
│   ├── __init__.py
│   ├── engine.py
│   ├── simulator.py
│   └── utils.py
├── tests/test_engine.py
├── main.py
├── requirements.txt
├── requirements-dev.txt
├── LICENSE
└── README.md
```

## 📐 Modeling notes

The physics in WaveForge is intentionally educational rather than a standards-compliant RF propagation simulator. The attenuation helper uses a simplified inverse-power model, and the RSSI helper uses a log-distance approximation. Power values are simulation units rather than measurements from real hardware.

## 🛡️ Safety boundary

WaveForge is a **simulation-only** project. It does not access wireless interfaces, capture real frames, transmit packets, perform deauthentication, jam frequencies, scan nearby networks, or interfere with third-party systems. It is intended for education, visualization, algorithm development, and deterministic testing.

## 📜 License

MIT
