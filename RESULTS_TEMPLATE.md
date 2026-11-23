# Part D — Experiment results and analysis template

Name/group: ________________________     Date: __________

All baseline experiments use a ring topology, six alert injections, 0.1 s message latency, 0.5 s retry interval, and seed 42. Do not change these settings when filling this table.

| Scenario | Nodes | Convergence time (s) | Messages attempted | Dropped messages | Retry batches |
| --- | ---: | ---: | ---: | ---: | ---: |
| Healthy, 3 nodes | 3 | | | | |
| Healthy, 5 nodes | 5 | | | | |
| Healthy, 7 nodes | 7 | | | | |
| 20% message loss, 5 nodes | 5 | | | | |
| Partition/healing, 5 nodes | 5 | | | | |

## Required figures

Attach `convergence_comparison.svg`, `message_comparison.svg`, and `retry_comparison.svg` from `output/`.

## Analysis (300–500 words total)

1. How did additional nodes affect message count and convergence time?
2. What did loss change? Why were retries needed?
3. How did a partition affect time to full convergence?
4. What does a single deterministic trial fail to tell us about variability?
5. Why can independent sensor alerts be eventually disseminated without a Raft leader, whereas a single agreed ordered log requires a consensus mechanism?

**Measurement note:** the reported convergence time is from the **last alert injection** to the first full convergence *after the experiment's final fault recovery*. The `recovery_seconds` column in the JSON result, when provided, measures from healing to convergence and should not be substituted for the convergence-time column above.
