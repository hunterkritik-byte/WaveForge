# Simulation → Hardware Roadmap

WaveForge is intentionally being built in stages so physical hardware is introduced only after the software workflow is reproducible.

## Phase 1 — Simulation foundation

- [x] Bluetooth 79-channel AFH model
- [x] Wi-Fi routing/topology model
- [x] Interference, attenuation, RSSI, latency, delivery, and power abstractions
- [x] Deterministic seeds
- [x] Headless telemetry

## Phase 2 — Experiment infrastructure

- [x] Per-step history
- [x] Aggregate summaries
- [x] Scenario presets
- [x] Portable JSON scenarios
- [x] JSON/Markdown exports
- [ ] Versioned scenario schema
- [ ] Pluggable PHY/model interfaces

## Phase 3 — Prototype preparation

- [ ] Define reference hardware architecture
- [ ] Produce an initial BOM and approved alternatives
- [ ] Define enclosure and mechanical constraints
- [ ] Freeze simulation scenarios as acceptance tests
- [ ] Create a controlled measurement plan

## Phase 4 — Hardware validation

- [ ] Fabricate engineering prototypes
- [ ] Bring up the board in a controlled environment
- [ ] Capture measured RF/network/power data
- [ ] Import measurements into a comparison format
- [ ] Quantify simulation-vs-measurement deltas
- [ ] Iterate model parameters based on evidence

## Phase 5 — Manufacturing readiness

- [ ] Design-for-manufacture review
- [ ] Component lifecycle and sourcing review
- [ ] Assembly/test fixture definition
- [ ] Small-batch pilot
- [ ] Production test plan

## Partner opportunity

The highest-value support is not simply fabrication: engineering feedback during component selection, PCB review, bring-up, testing, and design-for-manufacture can reduce the gap between a research prototype and a manufacturable product.
