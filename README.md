# ⚡ WaveForge

**Software-only wireless network simulator for exploring Bluetooth Adaptive Frequency Hopping, Wi-Fi routing, interference, telemetry, and reproducible hardware-validation workflows.**

WaveForge turns wireless concepts into an interactive simulation without radio hardware or physical network access. It provides a safe software layer for experimenting with protocol behavior before committing to prototype hardware.

> **Hardware roadmap:** WaveForge is designed to grow from a simulation and research tool into a repeatable pre-prototype validation platform. Hardware partners can use the project to evaluate scenarios, compare design assumptions, and define what should be measured on future prototypes.

## ✨ What it can do today

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
- Configurable seed, update rate, interference probability, and client count
- Moving Bluetooth nodes
- Wi-Fi hub-and-spoke topology
- Signal attenuation and environmental-noise models
- Packet delivery, latency, RSSI, and simulated power telemetry
- Deterministic runs for reproducible experiments
- Headless JSON telemetry for CI and notebooks
- Per-step experiment history
- Aggregate summaries and run-to-run comparisons
- **Portable scenario presets and JSON scenario files**
- **Exportable JSON and Markdown experiment reports**

### Developer experience
- Modular `src/` architecture
- Python 3.9+ compatible typing
- Type hints and docstrings
- Pytest regression suite
- GitHub Actions on Python 3.9–3.12
- No compiled binaries or physical-radio dependencies

## 🧪 Repeatable scenarios

Built-in profiles make demos and design reviews reproducible:

```bash
python main.py --scenario baseline
python main.py --scenario dense-interference
python main.py --scenario low-power
```

Or load a scenario owned by your team:

```bash
python main.py --scenario-file examples/sponsor-demo.json
```

A scenario records its seed, run length, client count, interference assumptions, notes, and tags. This gives researchers and future hardware teams a stable starting point for comparing revisions.

## 📊 Export a design-review report

Generate machine-readable results and a lightweight report without adding database or cloud dependencies:

```bash
python main.py --scenario dense-interference --export-json artifacts/run.json --export-md artifacts/run.md
```

The JSON export contains raw samples plus aggregate statistics. The Markdown export is suitable for attaching to a prototype/design review and records that the measurements came from the deterministic software-only model.

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

### Run the regression suite

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## 🧩 Example workflow for hardware teams

1. **Define** — describe the target topology and operating assumptions as a scenario.
2. **Simulate** — run baseline and stress profiles with fixed seeds.
3. **Compare** — export telemetry and review delivery, latency, RSSI, and power trends.
4. **Prototype** — translate the highest-value assumptions into a future PCB/enclosure test plan.
5. **Validate** — compare future measured hardware data against the software baseline.

WaveForge deliberately stops at the simulation boundary today. It does not claim that simulated RF results are a substitute for certified or laboratory measurements.

## 🗺️ Roadmap

- [x] Deterministic Bluetooth/Wi-Fi simulation
- [x] Headless telemetry and experiment history
- [x] Scenario presets and portable JSON profiles
- [x] JSON/Markdown experiment exports
- [ ] Pluggable PHY/model interfaces
- [ ] Hardware-measurement import format for prototype comparison
- [ ] Scenario schema versioning and migration tooling
- [ ] Optional dashboard for long-running experiment comparison
- [ ] Reference prototype specification and BOM once hardware resources are available

## 🤝 Hardware partnership / sponsorship

WaveForge is an open-source project and is currently focused on building a credible simulation and validation workflow before physical prototyping. Support from a hardware manufacturing or engineering partner could accelerate the next phase through **prototype PCB fabrication, component sourcing, enclosure development, assembly, testing, and engineering feedback**.

A partner would get a clear, reproducible software testbed and a public project that can document the transition from simulation assumptions to prototype validation. Any partnership should be agreed explicitly; the repository does not imply endorsement by any manufacturer.

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
                Scenarios / Reports / Dashboard
                            │
                       Future Hardware
                         Validation
```

## 🛡️ Safety boundary

WaveForge is a **simulation-only** project. It does not access wireless interfaces, capture real frames, transmit packets, perform deauthentication, jam frequencies, scan nearby networks, or interfere with third-party systems. It is intended for education, visualization, algorithm development, deterministic testing, and pre-prototype engineering analysis.

## 📜 License

MIT
