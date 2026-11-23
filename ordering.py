"""Supplied Part F clock scenarios."""
from __future__ import annotations

import heapq

from logical_clock import LogicalClock


CLOCK_CASES = ["F1 — Independent events", "F2 — Causal chain", "F3 — Delayed messages"]


class ClockScenario:
    def __init__(self, title: str, clock_class=LogicalClock):
        self.title = title
        self.clocks = {n: clock_class(n) for n in ("N0", "N1", "N2")}
        self.queue = []
        self.serial = 0
        self.now = 0.0
        self.events: list[dict] = []
        self.snapshots: list[dict] = []
        self.message_counter = 0

    def schedule(self, time: float, action) -> None:
        self.serial += 1
        heapq.heappush(self.queue, (round(time, 3), self.serial, action))

    def record(self, typ: str, node: str, label: str, *, peer=None, message_id=None) -> None:
        self.events.append({"at": round(self.now, 2), "type": typ, "node": node,
                            "peer": peer, "label": label,
                            "clock": self.clocks[node].value, "message_id": message_id})
        self.snapshots.append({"at": round(self.now, 2), "clocks":
                               {n: c.value for n, c in self.clocks.items()},
                               "event_index": len(self.events) - 1})

    def local(self, node: str, label: str) -> None:
        self.clocks[node].local_event()
        self.record("local", node, label)

    def send(self, src: str, dest: str, label: str, delay: float) -> None:
        self.clocks[src].local_event()
        timestamp = self.clocks[src].value
        self.message_counter += 1
        message_id = self.message_counter
        self.record("send", src, label, peer=dest, message_id=message_id)

        def arrive():
            self.clocks[dest].receive_message(timestamp)
            self.record("receive", dest, label, peer=src, message_id=message_id)

        self.schedule(self.now + delay, arrive)

    def run(self) -> dict:
        while self.queue:
            self.now, _, action = heapq.heappop(self.queue)
            action()
        return {"name": self.title, "events": self.events,
                "timeline": self.snapshots,
                "final_clocks": {n: c.value for n, c in self.clocks.items()},
                "explanation": "Lamport order respects causality; smaller timestamps alone do not prove causality."}


def run_clock_case(name: str, clock_class=LogicalClock) -> dict:
    world = ClockScenario(name, clock_class)
    if name == "F1 — Independent events":
        world.schedule(0.5, lambda: world.local("N0", "Independent alert A"))
        world.schedule(0.7, lambda: world.local("N2", "Independent alert C"))
        world.schedule(1.0, lambda: world.local("N1", "Independent alert B"))
    elif name == "F2 — Causal chain":
        world.schedule(0.5, lambda: world.local("N0", "Alert A"))
        world.schedule(0.6, lambda: world.send("N0", "N1", "Notify A", 0.6))
        world.schedule(0.8, lambda: world.local("N2", "Independent alert C"))
        world.schedule(1.5, lambda: world.local("N1", "Alert B after receiving A"))
    elif name == "F3 — Delayed messages":
        world.schedule(0.2, lambda: world.local("N0", "Alert A"))
        world.schedule(0.3, lambda: world.send("N0", "N1", "Slow notification A", 1.5))
        world.schedule(0.5, lambda: world.local("N2", "Alert C"))
        world.schedule(0.6, lambda: world.send("N2", "N1", "Fast notification C", 0.2))
        world.schedule(1.2, lambda: world.local("N1", "Local event B"))
    else:
        raise ValueError(name)
    return world.run()
