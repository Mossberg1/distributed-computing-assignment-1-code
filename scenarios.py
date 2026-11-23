"""Supplied reproducible simulation cases (seed 42; times in seconds)."""
from __future__ import annotations

from network import Network
from node import GossipNode


CASE_NAMES = [
    "B — Healthy gossip",
    "C — 20% message loss",
    "C — Partition and healing",
    "E — Late node join",
    "E — Disconnect and rejoin",
    "E — Crash and restart",
]


def create_case(case_name: str, *, count: int = 5,
                node_class: type[GossipNode] = GossipNode) -> tuple[Network, float]:
    names = [f"N{i}" for i in range(count)]
    loss = 0.20 if "20%" in case_name else 0.0
    start = set(names)
    if case_name == "E — Late node join":
        start.remove("N4")
    sim = Network(names, loss_rate=loss, seed=42, latency=0.1,
                  initially_online=start, node_class=node_class)
    sim.case_name = case_name
    duration = 10.0

    if case_name == "B — Healthy gossip":
        events = [(0.4, "N0", 104), (0.9, "N2", 205), (1.4, "N4", 306)]
    elif case_name in ("C — 20% message loss", "C — Partition and healing"):
        events = [(0.4, "N0", 104), (1.0, "N2", 205), (2.0, "N0", 306),
                  (2.2, "N3", 407), (3.2, "N1", 508), (4.0, "N4", 609)]
        if case_name == "C — Partition and healing":
            sim.schedule(1.5, "Partition: N0,N1 separated from N2,N3,N4",
                         lambda: sim.partition({"N0", "N1"}, True))
            sim.schedule(5.0, "Heal partition", lambda: sim.partition({"N0", "N1"}, False))
    elif case_name == "E — Late node join":
        events = [(0.4, "N0", 104), (1.0, "N2", 205), (1.4, "N3", 306),
                  (4.2, "N4", 407)]
        sim.schedule(3.0, "N4 joins", lambda: sim.set_online("N4", True))
    elif case_name == "E — Disconnect and rejoin":
        events = [(0.4, "N0", 104), (1.0, "N2", 205),
                  (2.0, "N0", 306), (2.5, "N4", 407)]
        sim.schedule(1.6, "N2 disconnects", lambda: sim.set_online("N2", False))
        sim.schedule(4.0, "N2 reconnects", lambda: sim.set_online("N2", True))
    elif case_name == "E — Crash and restart":
        events = [(0.4, "N0", 104), (1.0, "N2", 205), (1.2, "N3", 306),
                  (2.4, "N4", 407)]
        sim.schedule(1.7, "N3 crashes", lambda: sim.set_online("N3", False))
        sim.schedule(4.0, "N3 restarts with empty memory",
                     lambda: sim.set_online("N3", True, reset=True))
    else:
        raise ValueError(f"Unknown scenario: {case_name}")

    for at, origin, event_id in events:
        sim.schedule(at, f"Inject {event_id} at {origin}",
                     lambda n=origin, e=event_id: sim.inject(n, e))
    return sim, duration


def create_scale_case(count: int, *, loss_rate: float = 0.0,
                      partition: bool = False,
                      node_class: type[GossipNode] = GossipNode) -> tuple[Network, float]:
    names = [f"N{i}" for i in range(count)]
    sim = Network(names, loss_rate=loss_rate, seed=42, latency=0.1,
                  node_class=node_class)
    for i, event in enumerate([104, 205, 306, 407, 508, 609]):
        at = round(0.4 + 0.5 * i, 2)
        origin = names[(2 * i) % count]
        sim.schedule(at, f"Inject {event} at {origin}",
                     lambda n=origin, e=event: sim.inject(n, e))
    if partition:
        sim.schedule(1.5, "Partition", lambda: sim.partition({"N0", "N1"}, True))
        sim.schedule(5.0, "Heal", lambda: sim.partition({"N0", "N1"}, False))
    return sim, 10.0
