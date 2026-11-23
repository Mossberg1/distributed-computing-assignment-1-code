import unittest

from node import GossipNode
from scenarios import create_case


class PartCTests(unittest.TestCase):
    def test_lost_message_is_retried_until_ack(self):
        sent = []
        node = GossipNode("N0", lambda dest, kind, data: sent.append((dest, kind, data)))
        node.update_neighbors(["N1"])
        node.broadcast(104)
        node.tick(0.0)
        node.tick(0.1)
        self.assertEqual(len(sent), 1)
        node.tick(0.5)
        self.assertEqual(len(sent), 2)
        self.assertEqual(node.counters["retry_batches"], 1)
        node.receive_ack("N1", [104])
        node.tick(1.0)
        self.assertEqual(len(sent), 2)

    def test_loss_and_partition_recover(self):
        for name in ("C — 20% message loss", "C — Partition and healing"):
            with self.subTest(name=name):
                sim, duration = create_case(name)
                result = sim.run(duration)
                self.assertTrue(result["metrics"]["converged"])
                self.assertGreater(result["metrics"]["messages_dropped"], 0)
                self.assertGreater(result["metrics"]["retry_batches"], 0)
                self.assertEqual(set(result["final"]["N0"]), set(result["expected"]))

    def test_partition_temporarily_diverges(self):
        sim, duration = create_case("C — Partition and healing")
        result = sim.run(duration)
        frame = next(frame for frame in result["timeline"] if frame["at"] == 3.0)
        self.assertTrue(frame["blocked"])
        self.assertNotEqual(frame["nodes"]["N0"]["known"], frame["nodes"]["N3"]["known"])
        self.assertEqual({e["type"] for e in result["trace"]} & {"partition", "heal"},
                         {"partition", "heal"})


if __name__ == "__main__":
    unittest.main()
