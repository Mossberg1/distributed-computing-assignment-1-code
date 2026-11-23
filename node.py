"""Assignment 1, Parts B/C/E.

Complete ONLY the TODO sections. 
The supplied network.py drives simulated communication.
"""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Iterable


class GossipNode:
    def __init__(self, node_id: str, send: Callable[[str, str, dict], None],
                 retry_interval: float = 0.5, batch_size: int = 16):
        self.node_id = node_id
        self.send = send  # callback: send(destination, 'gossip'|'ack', {'ids': [...]})
        self.retry_interval = retry_interval
        self.batch_size = batch_size
        self.neighbors: list[str] = []
        self.known: set[int] = set()
        self.pending: dict[str, set[int]] = defaultdict(set)
        self.sent_unacked: dict[str, set[int]] = defaultdict(set)
        self.last_sent: dict[str, float] = defaultdict(lambda: float("-inf"))
        self.counters: dict[str, int] = defaultdict(int)

    def learn(self, event_ids: Iterable[int]) -> set[int]:
        """TODO B1: merge unique IDs and queue only newly learned IDs.

        1. Convert event_ids to a set.
        2. Compute which IDs are not already in self.known.
        3. Update self.known.
        4. Add each new ID to self.pending[neighbor] for each neighbor.
        5. Update counters['new_ids'] and counters['duplicates'].
        6. Return the set of newly discovered IDs.
        """
        ids = set(event_ids)
        new = ids - self.known
        self.known |= new
        for neighbor in self.neighbors:
            self.pending[neighbor] |= new
        self.counters["new_ids"] += len(new)
        self.counters["duplicates"] += len(ids) - len(new)
        return new

    def broadcast(self, event_id: int) -> dict:
        """TODO B1: call learn([event_id]); return an immediate local ACK.

        Expected: {'type': 'broadcast_ok', 'event_id': event_id}
        """
        self.learn([event_id])
        return {"type": "broadcast_ok", "event_id": event_id}

    def read(self) -> list[int]:
        """TODO B1: return a sorted list from this node's known set."""
        return sorted(self.known)

    def receive_gossip(self, sender: str, event_ids: list[int]) -> None:
        """TODO B2: learn received IDs and acknowledge the sender.

        The sender already knows the IDs it passed us. Avoid echoing them
        needlessly back by removing event_ids from self.pending[sender].
        Also remove them from self.sent_unacked[sender] if present.
        Reply using self.send(sender, 'ack', {'ids': sorted(set(event_ids))}).
        Increment counters['gossip_received'].
        """
        ids = set(event_ids)
        self.learn(ids)
        self.pending[sender] -= ids
        self.sent_unacked[sender] -= ids
        self.send(sender, "ack", {"ids": sorted(ids)})
        self.counters["gossip_received"] += 1

    def receive_ack(self, sender: str, event_ids: list[int]) -> None:
        """TODO C: stop retrying IDs acknowledged by this peer.

        Remove event_ids from both self.pending[sender] and
        self.sent_unacked[sender]. Increment counters['acks_received'].
        Until Part C is implemented, the incoming ACK may be ignored.
        """
        return

    def tick(self, now: float) -> None:
        """Part B starter sends *new* gossip. TODO C adds retransmission.

        This timer runs in simulated time. A sent message may be lost.
        Only an ACK in receive_ack should clear a pending event.
        """
        for peer in self.neighbors:
            unsent = sorted(self.pending[peer] - self.sent_unacked[peer])[:self.batch_size]
            if unsent:
                self.send(peer, "gossip", {"ids": unsent})
                self.sent_unacked[peer].update(unsent)
                self.last_sent[peer] = now
                self.counters["gossip_sent"] += 1
                continue
            # TODO C: If self.pending[peer] is nonempty and retry_interval
            # elapsed since last_sent[peer], resend up to batch_size IDs.
            # Update last_sent and counters['retry_batches']. If the queue
            # is empty or the timeout did not expire, do nothing.
            pass

    def update_neighbors(self, new_neighbors: Iterable[str]) -> None:
        """Part B basic membership works. TODO E adds historical catch-up.

        For Part E, compare OLD and NEW neighbors, queue all known IDs for
        newly connected peers, reset their send timers, and remove obsolete
        peer queues. The simulator calls this whenever nodes join or leave.
        """
        old = set(self.neighbors)
        updated = set(new_neighbors) - {self.node_id}
        self.neighbors = sorted(updated)
        # TODO E: implement catch-up for newly connected/rejoined neighbors.
        # Hint: updated - old gives newly connected peers; old - updated
        # gives disconnected peers. The pending queues are per peer.

    def snapshot(self) -> dict:
        """Already provided — the visualizer uses node-local state."""
        return {"known": self.read(), "neighbors": list(self.neighbors),
                "pending": {p: sorted(ids) for p, ids in self.pending.items() if ids},
                "counters": dict(self.counters)}
