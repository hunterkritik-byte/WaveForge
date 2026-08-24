from src.features import ChannelState, Node, PacketTrace, SimulationMetrics, availability, best_channel, distance, fairness, link_quality, moving_average, packet_loss, pdr, rssi, seed_nodes, snr_db, topology_edges, throughput_mbps


def test_geometry_and_rssi():
    a, b = Node("a", 0, 0), Node("b", 3, 4)
    assert distance(a, b) == 5
    assert rssi(-10, 10) < -10


def test_channels_and_topology():
    channels = [ChannelState(1, .8, .2), ChannelState(6, .1, .1)]
    assert best_channel(channels).channel == 6
    assert topology_edges([Node("a", 0, 0), Node("b", 1, 0)], 2) == [("a", "b")]


def test_metrics():
    metrics = SimulationMetrics()
    metrics.record(PacketTrace(1, "a", "b", 1000, 0, True, 5))
    assert metrics.snapshot()["delivery_ratio"] == 1.0
    assert packet_loss(10, 8) == .2
    assert pdr(10, 8) == .8
    assert throughput_mbps(1000, 10) > 0


def test_signal_helpers():
    assert 0 <= link_quality(-50, -90) <= 1
    assert snr_db(-50, -90) == 40
    assert len(moving_average([1, 2, 3])) == 3


def test_seed_and_fairness():
    assert seed_nodes(3, seed=7) == seed_nodes(3, seed=7)
    assert fairness([1, 1, 1]) == 1.0
    assert availability(seed_nodes(3)) == 1.0
