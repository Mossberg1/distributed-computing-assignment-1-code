import unittest

from node import GossipNode
from scenarios import create_case


class PartBTests(unittest.TestCase):
    def test_local_deduplication_and_read(self):
        sent = []
        node = GossipNode("N0", lambda *args: sent.append(args))
        node.update_neighbors(["N1"])
        self.assertEqual(node.broadcast(104)["type"], "broadcast_ok")
        node.broadcast(104)
        node.broadcast(205)
        self.assertEqual(node.read(), [104, 205])
        self.assertEqual(node.pending["N1"], {104, 205})
        self.assertEqual(node.counters["duplicates"], 1)

    def test_gossip_reaches_all_independent_nodes(self):
        sim, duration = create_case("B — Healthy gossip")
        result = sim.run(duration)
        self.assertTrue(result["metrics"]["converged"])
        for ids in result["final"].values():
            self.assertEqual(ids, [104, 205, 306])
        self.assertGreater(result["metrics"]["gossip_attempted"], 0)
        self.assertEqual(result["metrics"]["retry_batches"], 0)


if __name__ == "__main__":
    unittest.main()
