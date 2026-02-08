# Copyright (c) 2026 Md Mohaimenul Islam
# License: MIT

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, date
from pathlib import Path


WEEKDAY_NAMES = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


@dataclass
class DaySummary:
    """Stores daily totals (kWh) for consumption and production (3 phases)."""

    day: date
    cons_v1: float
    cons_v2: float
    cons_v3: float
    prod_v1: float
    prod_v2: float
    prod_v3: float


def parse_iso_datetime(value: str) -> datetime:
    """Converts an ISO timestamp string into a datetime object."""
    return datetime.fromisoformat(value.strip())


def wh_to_kwh(value_wh: float) -> float:
    """Converts Wh to kWh."""
    return value_wh / 1000.0


def format_kwh_fi(value: float) -> str:
    """Formats a float using two decimals and comma as decimal separator."""
    return f"{value:.2f}".replace(".", ",")


def format_date_fi(d: date) -> str:
    """Formats a date as dd.mm.yyyy."""
    return d.strftime("%d.%m.%Y")


def read_week_csv(path: Path) -> list[tuple[date, float, float, float, float, float, float]]:
    """
    Reads one weekly CSV file and returns rows as:
    (day, cons1_wh, cons2_wh, cons3_wh, prod1_wh, prod2_wh, prod3_wh)

    CSV uses semicolon delimiter and ISO timestamps.
    """
    rows: list[tuple[date, float, float, float, float, float, float]] = []

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader, None)  # skip header row

        for line in reader:
            if not line or len(line) < 7:
                continue

            dt = parse_iso_datetime(line[0])
            day = dt.date()

            c1 = float(line[1])
            c2 = float(line[2])
            c3 = float(line[3])
            p1 = float(line[4])
            p2 = float(line[5])
            p3 = float(line[6])

            rows.append((day, c1, c2, c3, p1, p2, p3))

    return rows


def compute_daily_summaries(
    rows: list[tuple[date, float, float, float, float, float, float]]
) -> list[DaySummary]:
    """
    Groups hourly rows by day and returns a list of DaySummary objects
    in chronological order.
    """
    totals: dict[date, list[float]] = {}

    for day, c1, c2, c3, p1, p2, p3 in rows:
        if day not in totals:
            totals[day] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        totals[day][0] += c1
        totals[day][1] += c2
        totals[day][2] += c3
        totals[day][3] += p1
        totals[day][4] += p2
        totals[day][5] += p3

    summaries: list[DaySummary] = []
    for d in sorted(totals.keys()):
        c1_wh, c2_wh, c3_wh, p1_wh, p2_wh, p3_wh = totals[d]

        summaries.append(
            DaySummary(
                day=d,
                cons_v1=wh_to_kwh(c1_wh),
                cons_v2=wh_to_kwh(c2_wh),
                cons_v3=wh_to_kwh(c3_wh),
                prod_v1=wh_to_kwh(p1_wh),
                prod_v2=wh_to_kwh(p2_wh),
                prod_v3=wh_to_kwh(p3_wh),
            )
        )

    return summaries


def build_week_section(week_number: int, summaries: list[DaySummary]) -> str:
    """
    Builds a formatted report section for one week as a string.
    """
    lines: list[str] = []
    lines.append(f"Week {week_number} electricity consumption and production (kWh, by phase)")
    lines.append("")
    lines.append("Day          Date        Consumption [kWh]               Production [kWh]")
    lines.append("            (dd.mm.yyyy)  v1      v2      v3             v1     v2     v3")
    lines.append("---------------------------------------------------------------------------")

    for s in summaries:
        weekday = WEEKDAY_NAMES[s.day.weekday()]
        date_str = format_date_fi(s.day)

        c1 = format_kwh_fi(s.cons_v1)
        c2 = format_kwh_fi(s.cons_v2)
        c3 = format_kwh_fi(s.cons_v3)
        p1 = format_kwh_fi(s.prod_v1)
        p2 = format_kwh_fi(s.prod_v2)
        p3 = format_kwh_fi(s.prod_v3)

        lines.append(
            f"{weekday:<12}  {date_str:<10}  "
            f"{c1:>6}  {c2:>6}  {c3:>6}           "
            f"{p1:>6}  {p2:>6}  {p3:>6}"
        )

    lines.append("")  # blank line after table
    return "\n".join(lines)


def write_report(output_path: Path, content: str) -> None:
    """Writes the full report content to summary.txt using UTF-8 encoding."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


def main() -> None:
    """
    Main function:
    Reads week41.csv, week42.csv, week43.csv, computes daily summaries,
    and writes the report to summary.txt.
    """
    base_dir = Path(__file__).parent

    week_files = {
        41: base_dir / "week41.csv",
        42: base_dir / "week42.csv",
        43: base_dir / "week43.csv",
    }

    report_parts: list[str] = []

    for week_no, path in week_files.items():
        rows = read_week_csv(path)
        summaries = compute_daily_summaries(rows)
        report_parts.append(build_week_section(week_no, summaries))

    full_report = "\n".join(report_parts)

    out_path = base_dir / "summary.txt"
    write_report(out_path, full_report)

    print("Wrote report to summary.txt")


if __name__ == "__main__":
    main()
