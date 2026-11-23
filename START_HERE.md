# Run, test, and visualize — one stage at a time

Start in the extracted project folder, not inside `tests/`. On Windows, if `python` is not recognized, use `py -3` in place of `python`.

## Part A — Raft

Use the previously supplied Raft visualizer and the existing Part A worksheet. No code in this ZIP is required for Part A.

## Part B — Basic gossip

1. In `node.py`, implement `learn`, `broadcast`, `read`, `receive_gossip` (marked TODO B1 and B2).
2. Test:

```sh
python -m unittest discover -s tests -p 'test_b*.py' -v
```

3. Generate and open the healthy-network visualization:

```sh
python run_simulation.py --stage B
```

Open `output/simulation_visualizer.html`. Play, pause, scrub the timeline, and select alert 104. Observe its propagation through the ring. The initial-sending portion of `tick` is already provided; retry logic comes in C.

## Part C — Acknowledgement, loss, retry, and partition

1. In `node.py`, implement `receive_ack` and finish the timeout/retry TODO in `tick`.
2. Test:

```sh
python -m unittest discover -s tests -p 'test_c*.py' -v
python run_simulation.py --stage C
```

Open the visualizer and select `C — 20% message loss` or `C — Partition and healing`. Inspect the red dashed links during partition, dropped messages, and final convergence.

## Part D — Experiments (no additional algorithm)

```sh
python -m unittest discover -s tests -p 'test_d*.py' -v
python run_experiments.py
```

Open `output/convergence_comparison.svg`, `message_comparison.svg`, and `retry_comparison.svg`. Read `output/experiment_results.csv` in a spreadsheet or text editor. Complete the results template in `RESULTS_TEMPLATE.md`.

## Part E — Dynamic node membership

1. In `node.py`, extend `update_neighbors` to queue **all known alert IDs** when a peer first joins or reconnects. Remove pending state for disconnected peers.
2. Test and visualize:

```sh
python -m unittest discover -s tests -p 'test_e*.py' -v
python run_simulation.py --stage E
```

Open `output/simulation_visualizer.html`. Select each E case. For crash/restart, pause at 4.0 s to observe the restarted node's empty local set, then play to watch catch-up.

## Part F — Lamport logical clocks

1. Implement the two TODOs in `logical_clock.py`.
2. Test and visualize:

```sh
python -m unittest discover -s tests -p 'test_f*.py' -v
python run_simulation.py --stage F
```

Open `output/logical_clocks.html`. Compare independent events, a causal chain, and delayed messages. Note how send and receive of the same message are linked by the message ID.

## Final verification

Once all TODOs are complete, run:

```sh
python -m unittest discover -s tests -v
python run_simulation.py
python run_experiments.py
```


