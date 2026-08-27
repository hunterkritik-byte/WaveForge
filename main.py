"""WaveForge command-line entry point."""
from __future__ import annotations

import argparse

from src.simulator import SimulationConfig, run


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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = SimulationConfig(
        seed=args.seed,
        fps=args.fps,
        channel_block_probability=args.block_probability,
        client_count=args.clients,
    )
    run(config)


if __name__ == "__main__":
    main()
