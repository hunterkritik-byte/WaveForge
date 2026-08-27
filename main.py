"""WaveForge command-line entry point."""
from __future__ import annotations

import argparse

from src.scenarios import SCENARIOS, get_scenario
from src.simulator import SimulationConfig, run


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the WaveForge software-only wireless simulator")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default=None, help="use a built-in scenario")
    parser.add_argument("--seed", type=int, default=None, help="deterministic simulation seed")
    parser.add_argument("--fps", type=int, default=None, help="dashboard update rate")
    parser.add_argument("--block-probability", type=float, default=None, help="per-channel interference probability (0..1)")
    parser.add_argument("--clients", type=int, default=None, help="number of simulated Wi-Fi clients")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.scenario:
        base = get_scenario(args.scenario)
    else:
        base = SimulationConfig()
    config = SimulationConfig(
        seed=base.seed if args.seed is None else args.seed,
        fps=base.fps if args.fps is None else args.fps,
        channel_block_probability=(
            base.channel_block_probability
            if args.block_probability is None else args.block_probability
        ),
        client_count=base.client_count if args.clients is None else args.clients,
    )
    run(config)


if __name__ == "__main__":
    main()
