"""Matplotlib dashboard for the software-only radio simulation."""
from __future__ import annotations

import random
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from .engine import BluetoothNode, WiFiClientNode, WiFiRouterNode
from .utils import attenuation, rssi_from_distance


class Simulation:
    """Own simulation state and telemetry; no physical radio access is performed."""
    def __init__(self, seed: int = 7):
        self.rng = random.Random(seed)
        self.bt_a = BluetoothNode("BT-A", -1.5, 0, self.rng)
        self.bt_b = BluetoothNode("BT-B", 1.5, 0, self.rng)
        self.bt_a.pair(self.bt_b)
        self.router = WiFiRouterNode("ROUTER", 0, x=0, y=-2)
        self.clients = [WiFiClientNode(f"C{i}", f"192.168.1.{10+i}", f"02:00:00:00:00:{i:02x}", x=-2+i*2, y=-0.2) for i in range(3)]
        for c in self.clients: self.router.register(c)
        self.tick = 0
        self.success, self.latencies, self.power = 0, [], {"Bluetooth": 0.0, "Wi-Fi": 0.0}

    def step(self) -> None:
        self.tick += 1
        self.bt_a.x += self.rng.uniform(-0.08, 0.08)
        self.bt_b.x += self.rng.uniform(-0.08, 0.08)
        blocked = {c for c in range(79) if self.rng.random() < 0.06}
        self.bt_a.blocked_channels = blocked
        self.success += 1
        self.latencies.append(2.0 + len(blocked) * 0.04)
        self.power["Bluetooth"] += self.rng.uniform(2, 5)
        self.power["Wi-Fi"] += self.rng.uniform(50, 100)


def run() -> None:
    """Run a ~30 FPS dual-panel educational dashboard."""
    sim = Simulation()
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
        ax_wifi.set_title("Wi-Fi • IP Routing")
        ax_wifi.set_xlim(-3, 3); ax_wifi.set_ylim(-3, 1)
        ax_wifi.scatter([sim.router.x], [sim.router.y], s=220, marker="s")
        for c in sim.clients:
            ax_wifi.scatter([c.x], [c.y], s=140)
            ax_wifi.plot([sim.router.x, c.x], [sim.router.y, c.y], linestyle=":")
            ax_wifi.text(c.x, c.y + .18, c.ip, ha="center", fontsize=8)
        avg = sum(sim.latencies) / len(sim.latencies)
        fig.text(.5, .02, f"tick={sim.tick}  success={sim.success}  avg latency={avg:.2f} ms  power BT={sim.power['Bluetooth']:.1f} / Wi-Fi={sim.power['Wi-Fi']:.1f}", ha="center", fontsize=9)

    FuncAnimation(fig, update, interval=1000/30, cache_frame_data=False)
    plt.tight_layout(rect=(0, .05, 1, 1))
    plt.show()


if __name__ == "__main__":
    run()
