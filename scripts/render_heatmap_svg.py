"""Render contribution JSON as a compact, themed SVG heatmap."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def render(data: dict, output: Path) -> None:
    days = data["days"][-371:]
    cells = []
    first = date.fromisoformat(days[0]["date"])
    for item in days:
        current = date.fromisoformat(item["date"])
        x = ((current - first).days // 7) * 15 + 28
        y = current.weekday() * 15 + 40
        level = min(4, int(item.get("level", 0)))
        cells.append(f'<rect x="{x}" y="{y}" width="11" height="11" rx="2" class="l{level}"><title>{item["date"]}: {item["count"]} contributions</title></rect>')
    metrics = data["metrics"]
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 190" role="img">
<title>{data["username"]} contribution activity</title><rect width="100%" height="100%" rx="14" fill="#0d0d0d" stroke="#D4AF37"/>
<text x="28" y="25" fill="#D4AF37" font-family="monospace" font-size="13">CONTRIBUTIONS · {metrics["total"]} total · {metrics["current_streak"]} day streak</text>
{"".join(cells)}
<style>.l0{{fill:#202020}}.l1{{fill:#6d5520}}.l2{{fill:#9a772b}}.l3{{fill:#c39a3a}}.l4{{fill:#D4AF37}}rect{{animation:pop .45s ease-out both}}@keyframes pop{{from{{opacity:0;transform:scale(.4)}}to{{opacity:1;transform:scale(1)}}}}</style>
</svg>
"""
    output.write_text(svg, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=Path, default=Path("data/contributions.json"))
    parser.add_argument("-o", "--output", type=Path, default=Path("contrib-heatmap.svg"))
    args = parser.parse_args()
    render(json.loads(args.input.read_text(encoding="utf-8")), args.output)


if __name__ == "__main__":
    main()
