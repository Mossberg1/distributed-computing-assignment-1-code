#!/usr/bin/env python3
"""Run all B/C/E and F teaching scenarios; build two offline HTML visualizers."""
from __future__ import annotations

import json
import argparse
from pathlib import Path

from ordering import CLOCK_CASES, run_clock_case
from scenarios import CASE_NAMES, create_case


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"


def write_html(template: str, placeholder: str, data: dict, target: str) -> None:
    content = (ROOT / template).read_text(encoding="utf-8")
    if content.count(placeholder) != 1:
        raise ValueError(f"Missing or repeated marker {placeholder} in {template}")
    safe_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    (OUT / target).write_text(content.replace(placeholder, safe_json), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate the selected assignment stage")
    parser.add_argument("--stage", choices=["B", "C", "E", "F", "all"], default="all")
    stage = parser.parse_args().stage
    OUT.mkdir(exist_ok=True)
    if stage != "F":
        cases = []
        selected_cases = [n for n in CASE_NAMES if stage == "all" or n.startswith(("B", "C", "E")[:{"B": 1,"C": 2,"E": 3}[stage]])]
        for name in selected_cases:
            sim, duration = create_case(name)
            result = sim.run(duration)
            result["name"] = name
            assert result["metrics"]["converged"], f"Not converged: {name}"
            cases.append(result)
            print(f"{name:<31} converged={result['metrics']['converged']} "
                  f"messages={result['metrics']['messages_attempted']:<3} "
                  f"dropped={result['metrics']['messages_dropped']:<3} "
                  f"retries={result['metrics']['retry_batches']}")
        data = {"runs": cases, "description": "Deterministic in-process simulation; not real networking"}
        (OUT / "simulation_results.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
        write_html("visualizer_template.html", "__SIMULATION_DATA__", data, "simulation_visualizer.html")
        print("Open output/simulation_visualizer.html in a browser.")
    if stage in ("F", "all"):
        clocks = {"runs": [run_clock_case(case) for case in CLOCK_CASES]}
        (OUT / "logical_clock_results.json").write_text(json.dumps(clocks, indent=2), encoding="utf-8")
        write_html("clocks_template.html", "__CLOCK_DATA__", clocks, "logical_clocks.html")
        print("Open output/logical_clocks.html in a browser.")


if __name__ == "__main__":
    main()
