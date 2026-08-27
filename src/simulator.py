"""Matplotlib dashboard for the software-only radio simulation."""
from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from .engine import BluetoothNode, WiFiClientNode, WiFiRouterNode
from .utils import attenuation, rssi_from_distance


@dataclass(frozen=True)
class SimulationConfig:
    """Runtime controls for a deterministic educational simulation."""
    seed: int = 7
    fps: int = 30
    channel_block_probability: float = 0.06
    client_count: int = 3

    def __post_init__(self) -> None:
        if self.fps <= 0:
            raise ValueError("fps must be positive")
        if not 0.0 <= self.channel_block_probability <= 1.0:
            raise ValueError("channel_block_probability must be between 0 and 1")
        if self.client_count <= 0:
            raise ValueError("client_count must be positive")


class Simulation:
    """Own simulation state and telemetry; no physical radio access is performed."""

    def __init__(self, config: Optional[SimulationConfig] = None, seed: Optional[int] = None):
        self.config = config or SimulationConfig(seed=7 if seed is None else seed)
        if seed is not None:
            self.config = SimulationConfig(
                seed=seed,
                fps=self.config.fps,
                channel_block_probability=self.config.channel_block_probability,
                client_count=self.config.client_count,
            )
        self.rng = random.Random(self.config.seed)
        self.bt_a = BluetoothNode("BT-A", -1.5, 0, self.rng)
        self.bt_b = BluetoothNode("BT-B", 1.5, 0, self.rng)
        self.bt_a.pair(self.bt_b)
        self.router = WiFiRouterNode("ROUTER", 0, x=0, y=-2)
        self.clients = [
            WiFiClientNode(
                f"C{i}",
                f"192.168.1.{10+i}",
                f"02:00:00:00:00:{i:02x}",
                x=-2+i*2,
                y=-0.2,
            )
            for i in range(self.config.client_count)
        ]
        for client in self.clients:
            self.router.register(client)
        self.tick = 0
        self.success = 0
        self.dropped = 0
        self.latencies: List[float] = []
        self.rssi_samples: List[float] = []
        self.power: Dict[str, float] = {"Bluetooth": 0.0, "Wi-Fi": 0.0}

    @property
    def packet_delivery_rate(self) -> float:
        """Return delivered packets as a percentage of attempted packets."""
        attempts = self.success + self.dropped
        return 100.0 * self.success / attempts if attempts else 0.0

    @property
    def average_rssi(self) -> float:
        """Return the average simulated Bluetooth RSSI in dBm."""
        return sum(self.rssi_samples) / len(self.rssi_samples) if self.rssi_samples else 0.0

    def telemetry(self) -> Dict[str, float]:
        """Return a compact snapshot suitable for dashboards or tests."""
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0.0
        return {
            "tick": float(self.tick),
            "delivered": float(self.success),
            "dropped": float(self.dropped),
            "delivery_rate": self.packet_delivery_rate,
            "avg_latency_ms": avg_latency,
            "avg_rssi_dbm": self.average_rssi,
            "bluetooth_power": self.power["Bluetooth"],
            "wifi_power": self.power["Wi-Fi"],
        }

    def step(self) -> None:
        self.tick += 1
        self.bt_a.x += self.rng.uniform(-0.08, 0.08)
        self.bt_b.x += self.rng.uniform(-0.08, 0.08)
        blocked = {
            c for c in range(79)
            if self.rng.random() < self.config.channel_block_probability
        }
        self.bt_a.blocked_channels = blocked

        distance = max(abs(self.bt_a.x - self.bt_b.x), 0.1)
        signal_factor = attenuation(distance)
        self.rssi_samples.append(rssi_from_distance(distance))
        # At the default ~3-unit separation, the simplified model is still usable.
        delivered = signal_factor >= 0.08 and bool(79 - len(blocked))
        if delivered:
            self.success += 1
            self.latencies.append(2.0 + len(blocked) * 0.04 + (1.0 - signal_factor))
        else:
            self.dropped += 1

        self.power["Bluetooth"] += self.rng.uniform(2, 5)
        self.power["Wi-Fi"] += self.rng.uniform(50, 100)


def run(config: Optional[SimulationConfig] = None) -> None:
    """Run the dual-panel educational dashboard."""
    sim = Simulation(config)
    fig, (ax_bt, ax_wifi) = plt.subplots(1, 2, figsize=(13, 6))
    fig.suptitle("WaveForge — Software-Only Wireless Simulator")

    def update(_frame):
        sim.step()
        ax_bt.clear(); ax_wifi.clear()
        ax_bt.set_title("Bluetooth • Adaptive Frequency Hopping")
        ax_bt.set_xlim(-4, 4); ax_bt.set_ylim(-2, 2)
        ax_bt.scatter([sim.bt_a.x, sim.bt_b.x], [sim.bt_a.y, sim.bt_b.y], s=180)
        ax_bt.plot([sim.bt_a.x, sim.bt_b.x], [0, 0], linestyle="--")
        ax_bt.text(-3.8, 1.5, f"Clear channels: {79-len(sim.bt_a.blocked_channels)}/79")
        ax_bt.text(-3.8, 1.15, f"RSSI: {sim.average_rssi:.1f} dBm")
        ax_wifi.set_title("Wi-Fi • IP Routing")
        ax_wifi.set_xlim(-3, 3); ax_wifi.set_ylim(-3, 1)
        ax_wifi.scatter([sim.router.x], [sim.router.y], s=220, marker="s")
        for client in sim.clients:
            ax_wifi.scatter([client.x], [client.y], s=140)
            ax_wifi.plot([sim.router.x, client.x], [sim.router.y, client.y], linestyle=":")
            ax_wifi.text(client.x, client.y + .18, client.ip, ha="center", fontsize=8)
        metrics = sim.telemetry()
        fig.text(
            .5, .02,
            f"tick={sim.tick}  delivery={metrics['delivery_rate']:.1f}%  "
            f"avg latency={metrics['avg_latency_ms']:.2f} ms  "
            f"power BT={metrics['bluetooth_power']:.1f} / Wi-Fi={metrics['wifi_power']:.1f}",
            ha="center", fontsize=9,
        )

    fps = sim.config.fps
    FuncAnimation(fig, update, interval=1000 / fps, cache_frame_data=False)
    plt.tight_layout(rect=(0, .05, 1, 1))
    plt.show()


if __name__ == "__main__":
    run()
