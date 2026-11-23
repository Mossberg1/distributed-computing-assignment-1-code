# Distributed Computing — Assignment 1 (Python-only student starter)

## First three steps

1. Install **Python 3.10 or newer**. No Docker, Maelstrom, Java, server, or pip package is needed.
2. Extract the ZIP. Open a terminal **inside this folder**, where `run_simulation.py` and `node.py` are located.
3. Read `STUDENT_START_HERE.md` and complete TODOs in `node.py` in order.

Part A uses the previously provided browser-based Raft exercise. Parts B–F use this Python simulator.

| Student edits | Parts |
| --- | --- |
| `node.py`: `learn`, `broadcast`, `read`, `receive_gossip` | B |
| `node.py`: `receive_ack`, retry logic in `tick` | C |
| `node.py`: historical sync in `update_neighbors` | E |
| `logical_clock.py`: `local_event`, `receive_message` | F |

All other files are **supplied infrastructure**. Do not edit `network.py`, `scenarios.py`, `ordering.py`, or the test files to make them pass.

**Run Part B tests after completing B:**

```sh
python -m unittest discover -s tests -p 'test_b*.py' -v
python run_simulation.py --stage B
```

Open `output/simulation_visualizer.html` in a browser. Part B does not yet process ACKs or retry lost gossip, so do not expect the C/E scenarios to work until those TODOs are complete.


