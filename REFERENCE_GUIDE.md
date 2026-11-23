# Short reference guide: concepts and code

## Independent nodes and simulated messages

Each `GossipNode` has its **own** Python object and `known` set. The simulation uses one Python process for simplicity, but does not share node event sets. The only way to spread an alert is through `self.send(destination, kind, payload)`. The supplied `Network` scheduler delays, drops, or delivers the message later. This is a **model**, not a real network or OS-process test.

## Gossip, duplicates, acknowledgements

For Part B, set union is sufficient for deduplication:

```text
new = received IDs − IDs already known locally
known ← known ∪ new
queue new IDs for each neighbor
```

Two sends may carry the same ID. A receiver stores the ID just once. The outgoing `broadcast_ok` confirms **local acceptance**, not delivery to every node.

For Part C, `pending[peer]` holds IDs still awaiting that peer's acknowledgement. An initial gossip send does not remove them. A received ACK removes the IDs. If an ACK or the gossip message is lost, send again after `retry_interval`.

Example message payloads *inside the simulator*:

```python
self.send("N1", "gossip", {"ids": [104, 205]})
self.send("N0", "ack", {"ids": [104, 205]})
```

These are **Python callback arguments**, not Maelstrom JSON/STDIN/STDOUT messages.

## Network partitions and eventual consistency

The ring topology connects neighboring nodes. During a 2–3 partition, cross-group messages are dropped. Nodes can still accept local events; the groups may temporarily disagree about event sets. With live nodes, restored connectivity, and retries, the sets should eventually converge. This is not a promise of persistence after every possible crash.

## Node joins and restarts

`update_neighbors(new_neighbors)` is invoked by the supplied simulator. A newly added neighbor may be missing alerts that arrived before it joined. Existing nodes should queue **all** known events for that new neighbor, not only recent events.

An offline node retains memory in the disconnect scenario. A restarted node receives a fresh `GossipNode` instance with an empty set. Other nodes must gossip previously known events again.

## Lamport logical clocks

Each node has its own scalar logical clock. Update rules:

```text
local event or send: L := L + 1
receive message with timestamp T: L := max(L, T) + 1
```

If event A causally precedes event B, then L(A) < L(B). **The reverse implication is not guaranteed:** a lower timestamp does not prove a causal relationship. Two independent nodes may both produce timestamp 1. A logical clock is not a consensus algorithm.

## Definitions used in Part D

| Metric | Meaning in this simulator |
| --- | --- |
| Convergence | Every currently online node knows every injected alert by the end |
| Convergence time | Simulated seconds from **last alert injection** to first full convergence after all faults have finished |
| Recovery time | Simulated seconds from last healing/join/restart (or last injection, whichever is later) to convergence |
| Messages attempted | Gossip messages plus ACK messages, including dropped attempts |
| Dropped messages | Attempts lost because of random loss, blocked links, or unavailable nodes |
| Retry batches | Gossip batches containing previously sent, still-unacknowledged IDs |
| Duplicates suppressed | IDs already present in a node's local set on receipt |

Use `seed=42` for the required baseline experiments so all students can compare results. Single-run outcomes need not generalize to every possible random network trace.
