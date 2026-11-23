import unittest

from scenarios import create_scale_case


class PartDTests(unittest.TestCase):
    def test_same_event_count_and_convergence_across_conditions(self):
        for n, loss, partition in ((3, 0, False), (5, 0, False),
                                   (7, 0, False), (5, .2, False), (5, 0, True)):
            with self.subTest(nodes=n, loss=loss, partition=partition):
                sim, duration = create_scale_case(n, loss_rate=loss, partition=partition)
                result = sim.run(duration)
                self.assertTrue(result["metrics"]["converged"])
                self.assertEqual(len(result["expected"]), 6)
                self.assertGreaterEqual(result["metrics"]["convergence_seconds"], 0)


if __name__ == "__main__":
    unittest.main()
