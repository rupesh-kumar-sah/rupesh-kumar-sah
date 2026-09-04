"""Fetch public GitHub contribution data without requiring an API token."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def metrics(days: list[dict]) -> dict:
    best = max(days, key=lambda item: item["count"], default={"date": None, "count": 0})
    longest = current = 0
    for item in days:
        if item["count"]:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    streak = 0
    for item in reversed(days):
        if item["count"]:
            streak += 1
        else:
            break
    return {"total": sum(item["count"] for item in days), "current_streak": streak, "longest_streak": longest, "best_day": best}


def fetch(username: str) -> list[dict]:
    response = requests.get(f"https://github.com/users/{username}/contributions", timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    days = []
    for element in soup.select("td.ContributionCalendar-day"):
        raw = element.get("data-date")
        if not raw:
            continue
        tooltip = element.find_next("tool-tip")
        label = tooltip.get_text(" ", strip=True) if tooltip else ""
        match = re.search(r"([\d,]+) contribution", label)
        days.append({"date": raw, "count": int(match.group(1).replace(",", "")) if match else 0, "level": int(element.get("data-level", "0"))})
    if not days:
        raise RuntimeError("GitHub returned no contribution cells.")
    return sorted(days, key=lambda item: item["date"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("username", default="rupesh-kumar-sah", nargs="?")
    parser.add_argument("-o", "--output", type=Path, default=Path("data/contributions.json"))
    args = parser.parse_args()
    days = fetch(args.username)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"username": args.username, "updated": date.today().isoformat(), "days": days, "metrics": metrics(days)}, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
