"""WaveForge command-line entry point."""
from __future__ import annotations

import argparse
import json

from src.experiments import run_experiment, summarize_history
from src.simulator import Simulation, SimulationConfig, run


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the WaveForge software-only wireless simulator")
    parser.add_argument("--seed", type=int, default=7, help="deterministic simulation seed")
    parser.add_argument("--fps", type=int, default=30, help="dashboard update rate")
    parser.add_argument(
        "--block-probability",
        type=float,
        default=0.06,
        help="per-channel interference probability (0..1)",
    )
    parser.add_argument("--clients", type=int, default=3, help="number of simulated Wi-Fi clients")
    parser.add_argument("--steps", type=int, default=0, help="run headless for N simulation steps")
    parser.add_argument("--json", action="store_true", help="print final telemetry as JSON; implies headless mode")
    parser.add_argument(
        "--report",
        choices=("final", "history", "summary"),
        default="final",
        help="headless report to emit; history and summary imply headless mode",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = SimulationConfig(
        seed=args.seed,
        fps=args.fps,
        channel_block_probability=args.block_probability,
        client_count=args.clients,
    )
    if args.steps < 0:
        raise SystemExit("--steps must be >= 0")

    headless = args.json or args.steps or args.report != "final"
    if headless:
        sim = Simulation(config)
        history = run_experiment(sim, args.steps)
        if args.report == "history":
            print(json.dumps(history, indent=2, sort_keys=True))
        elif args.report == "summary":
            print(json.dumps(summarize_history(history), indent=2, sort_keys=True))
        else:
            payload = sim.telemetry()
            print(json.dumps(payload, indent=2, sort_keys=True) if args.json else payload)
        return

    run(config)


if __name__ == "__main__":
    main()
