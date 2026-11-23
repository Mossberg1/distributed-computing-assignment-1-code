import unittest

from scenarios import create_case


class PartETests(unittest.TestCase):
    def test_late_join_gets_historical_alerts(self):
        sim, duration = create_case("E — Late node join")
        result = sim.run(duration)
        before = next(x for x in result["timeline"] if x["at"] == 2.0)
        self.assertFalse(before["nodes"]["N4"]["online"])
        self.assertTrue(result["metrics"]["converged"])
        self.assertEqual(result["final"]["N4"], [104, 205, 306, 407])

    def test_offline_node_catches_up(self):
        sim, duration = create_case("E — Disconnect and rejoin")
        result = sim.run(duration)
        frame = next(x for x in result["timeline"] if x["at"] == 3.0)
        self.assertFalse(frame["nodes"]["N2"]["online"])
        self.assertTrue(result["metrics"]["converged"])

    def test_restart_loses_memory_then_recovers(self):
        sim, duration = create_case("E — Crash and restart")
        result = sim.run(duration)
        frame = next(x for x in result["timeline"] if x["at"] == 4.0)
        self.assertEqual(frame["nodes"]["N3"]["known"], [])
        self.assertEqual(result["final"]["N3"], [104, 205, 306, 407])
        self.assertTrue(result["metrics"]["converged"])


if __name__ == "__main__":
    unittest.main()
