"""Deterministic, software-only simulation helpers for WaveForge.

These helpers model telemetry and network behavior; they never touch wireless
interfaces or transmit real frames.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from math import hypot
from random import Random
from statistics import mean
from typing import Iterable


@dataclass
class Node:
    node_id: str
    x: float = 0.0
    y: float = 0.0
    battery: float = 100.0
    tx_power: float = 0.0
    enabled: bool = True
    tags: dict[str, str] = field(default_factory=dict)


@dataclass
class PacketTrace:
    packet_id: int
    src: str
    dst: str
    size: int
    created_at: float
    delivered: bool = False
    latency_ms: float = 0.0
    retries: int = 0
    dropped_reason: str | None = None


@dataclass
class ChannelState:
    channel: int
    utilization: float = 0.0
    interference: float = 0.0
    noise_floor: float = -95.0


class SimulationMetrics:
    def __init__(self):
        self.packets: list[PacketTrace] = []
        self.samples: list[dict] = []

    def record(self, packet: PacketTrace):
        self.packets.append(packet)

    def snapshot(self) -> dict:
        delivered = [p for p in self.packets if p.delivered]
        return {
            "packets": len(self.packets),
            "delivered": len(delivered),
            "delivery_ratio": len(delivered) / len(self.packets) if self.packets else 0.0,
            "mean_latency_ms": mean(p.latency_ms for p in delivered) if delivered else 0.0,
            "retries": sum(p.retries for p in self.packets),
            "drops": len(self.packets) - len(delivered),
        }


def distance(a: Node, b: Node) -> float:
    return hypot(a.x - b.x, a.y - b.y)


def rssi(tx_power: float, distance_m: float, path_loss: float = 2.0) -> float:
    if distance_m <= 0:
        return tx_power
    return tx_power - 10.0 * path_loss * __import__("math").log10(distance_m)


def move(node: Node, dx: float, dy: float, bounds: tuple[float, float] | None = None):
    node.x += dx
    node.y += dy
    if bounds:
        width, height = bounds
        node.x = min(max(node.x, 0.0), width)
        node.y = min(max(node.y, 0.0), height)


def consume_battery(node: Node, amount: float):
    node.battery = max(0.0, node.battery - max(0.0, amount))
    if node.battery == 0:
        node.enabled = False


def channel_score(channel: ChannelState) -> float:
    return max(0.0, min(1.0, 0.55 * channel.utilization + 0.45 * channel.interference))


def best_channel(channels: Iterable[ChannelState]) -> ChannelState | None:
    return min(channels, key=channel_score, default=None)


def deterministic_noise(seed: int, count: int = 10, low: float = -3.0, high: float = 3.0) -> list[float]:
    rng = Random(seed)
    return [rng.uniform(low, high) for _ in range(count)]


def jitter(value: float, seed: int, spread: float = 1.0) -> float:
    return value + Random(seed).uniform(-spread, spread)


def throughput_mbps(packet_bytes: int, latency_ms: float) -> float:
    if latency_ms <= 0:
        return 0.0
    return (packet_bytes * 8.0) / (latency_ms / 1000.0) / 1_000_000.0


def packet_loss(sent: int, delivered: int) -> float:
    return 0.0 if sent <= 0 else max(0.0, min(1.0, (sent - delivered) / sent))


def pdr(sent: int, delivered: int) -> float:
    return 0.0 if sent <= 0 else max(0.0, min(1.0, delivered / sent))


def airtime_ms(size_bytes: int, rate_mbps: float) -> float:
    return 0.0 if rate_mbps <= 0 else (size_bytes * 8.0) / rate_mbps / 1000.0


def energy_per_packet(tx_power: float, airtime: float) -> float:
    return max(0.0, tx_power) * max(0.0, airtime)


def fairness(values: Iterable[float]) -> float:
    vals = [max(0.0, v) for v in values]
    total = sum(vals)
    if not vals or total == 0:
        return 0.0
    return total * total / (len(vals) * sum(v * v for v in vals))


def moving_average(values: Iterable[float], window: int = 3) -> list[float]:
    vals = list(values)
    if window <= 0:
        raise ValueError("window must be positive")
    return [mean(vals[max(0, i - window + 1): i + 1]) for i in range(len(vals))]


def exponential_smoothing(values: Iterable[float], alpha: float = 0.5) -> list[float]:
    if not 0 < alpha <= 1:
        raise ValueError("alpha must be in (0, 1]")
    result = []
    for value in values:
        result.append(value if not result else alpha * value + (1 - alpha) * result[-1])
    return result


def normalize_signal(value: float, floor: float = -100.0, ceiling: float = -20.0) -> float:
    if ceiling <= floor:
        raise ValueError("ceiling must be greater than floor")
    return max(0.0, min(1.0, (value - floor) / (ceiling - floor)))


def availability(enabled_nodes: Iterable[Node]) -> float:
    nodes = list(enabled_nodes)
    return sum(n.enabled and n.battery > 0 for n in nodes) / len(nodes) if nodes else 0.0


def topology_edges(nodes: Iterable[Node], radius: float) -> list[tuple[str, str]]:
    items = list(nodes)
    return [(a.node_id, b.node_id) for i, a in enumerate(items) for b in items[i + 1:] if distance(a, b) <= radius]


def seed_nodes(count: int, seed: int = 1, width: float = 100.0, height: float = 100.0) -> list[Node]:
    rng = Random(seed)
    return [Node(f"node-{i}", rng.uniform(0, width), rng.uniform(0, height), tags={"role": "client"}) for i in range(count)]


def percentile(values: Iterable[float], p: float = 0.95) -> float:
    vals = sorted(values)
    if not vals:
        return 0.0
    if not 0 <= p <= 1:
        raise ValueError("p must be between 0 and 1")
    return vals[min(len(vals) - 1, int(p * (len(vals) - 1)))]


def histogram(values: Iterable[float], bins: int = 10) -> list[int]:
    vals = list(values)
    if bins <= 0:
        raise ValueError("bins must be positive")
    if not vals:
        return [0] * bins
    lo, hi = min(vals), max(vals)
    if lo == hi:
        result = [0] * bins
        result[0] = len(vals)
        return result
    width = (hi - lo) / bins
    result = [0] * bins
    for value in vals:
        idx = min(bins - 1, int((value - lo) / width))
        result[idx] += 1
    return result


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def weighted_score(values: dict[str, float], weights: dict[str, float]) -> float:
    total_weight = sum(weights.get(k, 0.0) for k in values)
    return 0.0 if total_weight == 0 else sum(values[k] * weights.get(k, 0.0) for k in values) / total_weight


def confidence(observations: int, expected: int) -> float:
    if expected <= 0:
        return 0.0
    return clamp(observations / expected, 0.0, 1.0)


def queue_delay(queue_depth: int, service_rate_pps: float) -> float:
    return 0.0 if service_rate_pps <= 0 else queue_depth / service_rate_pps * 1000.0


def collision_probability(utilization: float) -> float:
    return clamp(utilization, 0.0, 1.0) ** 2


def retry_budget(success_probability: float, max_retries: int = 4) -> int:
    p = clamp(success_probability, 0.0, 1.0)
    return 0 if p >= 1 else max(0, min(max_retries, int((1 - p) * max_retries)))


def normalize_mac(mac: str) -> str:
    return mac.replace(":", "").replace("-", "").lower()


def normalize_channel(channel: int) -> int:
    if channel < 1:
        raise ValueError("channel must be positive")
    return channel


def packet_size_distribution(seed: int, count: int = 20) -> list[int]:
    rng = Random(seed)
    return [rng.randint(64, 1500) for _ in range(count)]


def latency_budget(base_ms: float, queue_ms: float, jitter_ms: float = 0.0) -> float:
    return max(0.0, base_ms + queue_ms + jitter_ms)


def utilization(bytes_sent: int, capacity_bytes: int) -> float:
    return 0.0 if capacity_bytes <= 0 else clamp(bytes_sent / capacity_bytes, 0.0, 1.0)


def link_quality(rssi_value: float, noise_floor: float) -> float:
    return clamp((rssi_value - noise_floor) / 50.0, 0.0, 1.0)


def snr_db(rssi_value: float, noise_floor: float) -> float:
    return rssi_value - noise_floor


def fading_factor(seed: int, spread: float = 1.0) -> float:
    return Random(seed).gauss(0.0, spread)


def path_loss(distance_m: float, exponent: float = 2.0, reference_loss: float = 40.0) -> float:
    if distance_m <= 0 or exponent <= 0:
        raise ValueError("distance and exponent must be positive")
    return reference_loss + 10.0 * exponent * __import__("math").log10(distance_m)


def received_power(tx_dbm: float, loss_db: float) -> float:
    return tx_dbm - max(0.0, loss_db)


def channel_capacity(rate_mbps: float, utilization_fraction: float) -> float:
    return max(0.0, rate_mbps * (1.0 - clamp(utilization_fraction, 0.0, 1.0)))


def sla_ok(latency_ms: float, packet_loss_fraction: float, max_latency_ms: float, max_loss: float) -> bool:
    return latency_ms <= max_latency_ms and packet_loss_fraction <= max_loss


def summarize_channels(channels: Iterable[ChannelState]) -> dict:
    items = list(channels)
    return {
        "count": len(items),
        "best": best_channel(items).channel if items else None,
        "mean_utilization": mean(c.utilization for c in items) if items else 0.0,
        "mean_interference": mean(c.interference for c in items) if items else 0.0,
    }


def deterministic_run_id(seed: int) -> str:
    return f"run-{seed:08x}"


def seed_event_times(seed: int, count: int, interval: float = 1.0) -> list[float]:
    rng = Random(seed)
    return [i * interval + rng.random() * interval * 0.1 for i in range(count)]


def confidence_interval(values: Iterable[float]) -> tuple[float, float]:
    vals = list(values)
    if not vals:
        return 0.0, 0.0
    m = mean(vals)
    if len(vals) == 1:
        return m, m
    variance = sum((v - m) ** 2 for v in vals) / (len(vals) - 1)
    margin = 1.96 * (variance / len(vals)) ** 0.5
    return m - margin, m + margin


def compare_runs(a: dict, b: dict) -> dict:
    keys = sorted(set(a) | set(b))
    return {k: b.get(k, 0) - a.get(k, 0) for k in keys if isinstance(a.get(k, 0), (int, float)) and isinstance(b.get(k, 0), (int, float))}
