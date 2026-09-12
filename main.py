"""WaveForge command-line entry point."""
from __future__ import annotations

import argparse
import json

from src.experiments import run_experiment, summarize_history
from src.report import write_json, write_markdown
from src.scenarios import get_preset, load as load_scenario
from src.simulator import Simulation, SimulationConfig, run


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the WaveForge software-only wireless simulator")
    parser.add_argument("--seed", type=int, default=7, help="deterministic simulation seed")
    parser.add_argument("--fps", type=int, default=30, help="dashboard update rate")
    parser.add_argument("--block-probability", type=float, default=0.06, help="per-channel interference probability (0..1)")
    parser.add_argument("--clients", type=int, default=3, help="number of simulated Wi-Fi clients")
    parser.add_argument("--steps", type=int, default=0, help="run headless for N simulation steps")
    parser.add_argument("--scenario", choices=("baseline", "dense-interference", "low-power"), help="load a built-in repeatable scenario")
    parser.add_argument("--scenario-file", help="load a scenario from a JSON file")
    parser.add_argument("--export-json", metavar="PATH", help="write experiment samples and summary to JSON")
    parser.add_argument("--export-md", metavar="PATH", help="write a review-friendly Markdown experiment report")
    parser.add_argument("--json", action="store_true", help="print final telemetry as JSON; implies headless mode")
    parser.add_argument("--report", choices=("final", "history", "summary"), default="final", help="headless report to emit")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.scenario and args.scenario_file:
        raise SystemExit("use --scenario or --scenario-file, not both")

    scenario = load_scenario(args.scenario_file) if args.scenario_file else get_preset(args.scenario) if args.scenario else None
    seed = scenario.seed if scenario else args.seed
    clients = scenario.clients if scenario else args.clients
    block_probability = scenario.block_probability if scenario else args.block_probability
    steps = scenario.steps if scenario and args.steps == 0 else args.steps

    if steps < 0:
        raise SystemExit("--steps must be >= 0")

    config = SimulationConfig(seed=seed, fps=args.fps, channel_block_probability=block_probability, client_count=clients)
    headless = bool(args.json or steps or args.report != "final" or args.export_json or args.export_md or scenario)
    if headless:
        sim = Simulation(config)
        history = run_experiment(sim, steps)
        if args.export_json:
            write_json(history, args.export_json)
        if args.export_md:
            write_markdown(history, args.export_md, title=scenario.name if scenario else "WaveForge Experiment Report")
        if args.report == "history":
            print(json.dumps(history, indent=2, sort_keys=True))
        elif args.report == "summary":
            print(json.dumps(summarize_history(history), indent=2, sort_keys=True))
        elif args.json:
            print(json.dumps(sim.telemetry(), indent=2, sort_keys=True))
        elif not (args.export_json or args.export_md):
            print(json.dumps(sim.telemetry(), indent=2, sort_keys=True))
        return

    run(config)


if __name__ == "__main__":
    main()
