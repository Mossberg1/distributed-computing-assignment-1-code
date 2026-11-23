"""Part F. Complete both TODOs."""


class LogicalClock:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.value = 0

    def local_event(self) -> int:
        """TODO F1: increment this node's logical clock; return the value."""
        raise NotImplementedError("TODO F1: local Lamport event")

    def receive_message(self, received_clock: int) -> int:
        """TODO F2: use max(local value, received_clock) + 1; return value."""
        raise NotImplementedError("TODO F2: Lamport message receive")
