"""Core software-only wireless network models."""
from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
import random
from typing import Any


class BaseNode(ABC):
    """Base node with identity, position and lifecycle state."""
    def __init__(self, node_id: str, x: float = 0.0, y: float = 0.0):
        self.node_id, self.x, self.y, self.active = node_id, x, y, True

    @property
    def position(self) -> tuple[float, float]:
        return self.x, self.y


@dataclass
class DataPacket:
    """Packet metadata shared by both simulations."""
    source_id: str
    destination_id: str
    payload_size: int
    current_frequency: int | None = None
    target_ip: str | None = None
    packet_id: int = 0


class BluetoothNode(BaseNode):
    """Bluetooth node using a simulated 79-channel AFH map."""
    channels = tuple(range(79))

    def __init__(self, node_id: str, x: float = 0.0, y: float = 0.0, rng: random.Random | None = None):
        super().__init__(node_id, x, y)
        self.paired: set[str] = set()
        self.blocked_channels: set[int] = set()
        self.rng = rng or random.Random()

    def pair(self, other: "BluetoothNode") -> None:
        self.paired.add(other.node_id)
        other.paired.add(self.node_id)

    def choose_channel(self) -> int:
        """Return a clear channel; fail explicitly if all channels are blocked."""
        available = [c for c in self.channels if c not in self.blocked_channels]
        if not available:
            raise RuntimeError("AFH has no clear channels")
        return self.rng.choice(available)

    def transmit(self, destination: "BluetoothNode", payload_size: int, packet_id: int = 0) -> DataPacket:
        if destination.node_id not in self.paired:
            raise ValueError("destination is not paired")
        return DataPacket(self.node_id, destination.node_id, payload_size, current_frequency=self.choose_channel(), packet_id=packet_id)


class WiFiRouterNode(BaseNode):
    """Central Wi-Fi router with deterministic IP/MAC-to-client lookup."""
    def __init__(self, node_id: str, ip: str = "192.168.1.1", **kwargs: Any):
        super().__init__(node_id, **kwargs)
        self.ip = ip
        self.routing_table: dict[str, WiFiClientNode] = {}

    def register(self, client: "WiFiClientNode") -> None:
        self.routing_table[client.ip] = client
        self.routing_table[client.mac] = client

    def route(self, source_id: str, target_ip: str, payload_size: int, packet_id: int = 0) -> DataPacket:
        client = self.routing_table.get(target_ip)
        if client is None:
            raise KeyError(f"unknown destination IP: {target_ip}")
        return DataPacket(source_id, client.node_id, payload_size, target_ip=target_ip, packet_id=packet_id)


class WiFiClientNode(BaseNode):
    """Wi-Fi endpoint represented by an IP and MAC address."""
    def __init__(self, node_id: str, ip: str, mac: str, **kwargs: Any):
        super().__init__(node_id, **kwargs)
        self.ip, self.mac = ip, mac
