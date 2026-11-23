#!/usr/bin/env python3
"""Part D: execute controlled node-count and fault experiments (stdlib only)."""
from __future__ import annotations

import csv
from pathlib import Path
from xml.sax.saxutils import escape

from scenarios import create_scale_case


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"


def make_svg(rows: list[dict], key: str, title: str, path: Path, unit: str) -> None:
    width, height = 850, 365
    left, top, bottom = 72, 67, 70
    chart_h = height - top - bottom
    max_value = max(float(row[key]) for row in rows) or 1.0
    max_y = max_value * 1.15
    bar_space = (width - left - 25) / len(rows)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
             '<rect width="100%" height="100%" fill="#ffffff"/>',
             f'<text x="28" y="38" font-family="Arial" font-weight="bold" font-size="20" fill="#153452">{escape(title)}</text>',
             f'<text x="29" y="55" font-family="Arial" font-size="11" fill="#66798b">{escape(unit)} — six broadcasts, ring topology, seed 42</text>']
    for i in range(5):
        y = top + chart_h * i / 4
        label = max_y * (1 - i / 4)
        parts.extend([f'<line x1="{left}" y1="{y:.1f}" x2="{width-18}" y2="{y:.1f}" stroke="#e4ebf2"/>',
                      f'<text x="{left-10}" y="{y+4:.1f}" text-anchor="end" font-family="Arial" font-size="11" fill="#62748a">{label:.1f}</text>'])
    for i, row in enumerate(rows):
        value = float(row[key])
        x = left + bar_space * i + bar_space * .24
        w = bar_space * .53
        bar_h = value / max_y * chart_h
        y = top + chart_h - bar_h
        shade = "#DB794F" if "loss" in row["scenario"].lower() or "partition" in row["scenario"].lower() else "#347FC1"
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{bar_h:.1f}" rx="5" fill="{shade}"/>')
        parts.append(f'<text x="{x+w/2:.1f}" y="{max(top+12,y-9):.1f}" text-anchor="middle" font-family="Arial" font-size="12" fill="#183952">{value:g}</text>')
        label = row["scenario"].replace(" nodes", "n").replace("5n, ", "")
        parts.append(f'<text x="{x+w/2:.1f}" y="{top+chart_h+24}" text-anchor="middle" font-family="Arial" font-size="11" fill="#314c64">{escape(label)}</text>')
    parts.append('</svg>')
    path.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    experiments = [
        ("3 nodes", 3, 0.0, False),
        ("5 nodes", 5, 0.0, False),
        ("7 nodes", 7, 0.0, False),
        ("5n, 20% loss", 5, 0.20, False),
        ("5n, partition", 5, 0.0, True),
    ]
    rows = []
    for label, count, loss, partition in experiments:
        sim, duration = create_scale_case(count, loss_rate=loss, partition=partition)
        result = sim.run(duration)
        m = result["metrics"]
        if not m["converged"]:
            raise RuntimeError(f"Scenario did not converge: {label}")
        rows.append({"scenario": label, "nodes": count, "events": len(result["expected"]),
                     "convergence_seconds": m["convergence_seconds"],
                     "recovery_seconds": m["recovery_seconds"],
                     "messages_attempted": m["messages_attempted"],
                     "messages_dropped": m["messages_dropped"],
                     "retry_batches": m["retry_batches"], "converged": m["converged"]})

    with (OUT / "experiment_results.csv").open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    make_svg(rows, "convergence_seconds", "Time to full convergence", OUT / "convergence_comparison.svg", "seconds from final alert to convergence")
    make_svg(rows, "messages_attempted", "Network communication overhead", OUT / "message_comparison.svg", "all gossip and ACK attempts")
    make_svg(rows, "retry_batches", "Gossip retransmissions", OUT / "retry_comparison.svg", "retransmitted gossip batches")
    print("Scenario                 Converge(s)   Messages   Retries   Dropped")
    for row in rows:
        print(f"{row['scenario']:<24} {row['convergence_seconds']:>10.2f} "
              f"{row['messages_attempted']:>10} {row['retry_batches']:>9} "
              f"{row['messages_dropped']:>9}")
    print("\nGenerated output/experiment_results.csv and three offline SVG charts.")


if __name__ == "__main__":
    main()
