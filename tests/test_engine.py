import random
import pytest
from src.engine import BluetoothNode, WiFiClientNode, WiFiRouterNode
from src.simulator import Simulation, SimulationConfig
from src.utils import attenuation, rssi_from_distance


def test_afh_excludes_blocked_channels():
    a = BluetoothNode("a", rng=random.Random(1)); b = BluetoothNode("b", rng=random.Random(1)); a.pair(b)
    a.blocked_channels = set(range(78))
    assert a.choose_channel() == 78


def test_afh_fails_when_all_channels_blocked():
    a = BluetoothNode("a", rng=random.Random(1)); a.blocked_channels = set(range(79))
    with pytest.raises(RuntimeError): a.choose_channel()


def test_wifi_routes_to_exact_ip():
    r = WiFiRouterNode("r"); c = WiFiClientNode("c", "10.0.0.8", "02:00:00:00:00:08"); r.register(c)
    packet = r.route("r", "10.0.0.8", 100)
    assert packet.destination_id == "c" and packet.target_ip == "10.0.0.8"


def test_physics_helpers():
    assert attenuation(2) == 0.25
    assert rssi_from_distance(1) == -30.0


def test_simulation_is_deterministic_and_reports_telemetry():
    config = SimulationConfig(seed=42, client_count=2)
    first = Simulation(config)
    second = Simulation(config)
    for _ in range(5):
        first.step()
        second.step()
    assert first.telemetry() == second.telemetry()
    assert first.tick == 5
    assert first.success + first.dropped == 5
    assert 0.0 <= first.packet_delivery_rate <= 100.0
    assert first.average_rssi < 0.0


def test_simulation_config_validates_runtime_controls():
    with pytest.raises(ValueError):
        SimulationConfig(fps=0)
    with pytest.raises(ValueError):
        SimulationConfig(channel_block_probability=1.1)
    with pytest.raises(ValueError):
        SimulationConfig(client_count=0)
