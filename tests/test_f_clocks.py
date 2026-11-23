import unittest

from logical_clock import LogicalClock
from ordering import run_clock_case


class PartFTests(unittest.TestCase):
    def test_lamport_rules(self):
        c = LogicalClock("N0")
        self.assertEqual(c.local_event(), 1)
        self.assertEqual(c.local_event(), 2)
        self.assertEqual(c.receive_message(8), 9)
        self.assertEqual(c.receive_message(1), 10)

    def test_causal_chain(self):
        trace = run_clock_case("F2 — Causal chain")["events"]
        sent = next(e for e in trace if e["type"] == "send")
        received = next(e for e in trace if e["type"] == "receive")
        after = next(e for e in trace if "Alert B" in e["label"])
        self.assertLess(sent["clock"], received["clock"])
        self.assertLess(received["clock"], after["clock"])

    def test_late_message_may_arrive_after_a_later_send(self):
        trace = run_clock_case("F3 — Delayed messages")["events"]
        sends = [e for e in trace if e["type"] == "send"]
        receives = [e for e in trace if e["type"] == "receive"]
        self.assertLess(sends[0]["at"], sends[1]["at"])
        self.assertEqual([e["message_id"] for e in receives], [2, 1])
        self.assertLess(receives[0]["clock"], receives[1]["clock"])


if __name__ == "__main__":
    unittest.main()
