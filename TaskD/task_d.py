from __future__ import annotations

import csv
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Tuple


Row = Tuple[datetime, int, int, int, int, int, int]
Totals = Dict[date, List[float]]  # [c1, c2, c3, p1, p2, p3] in kWh


FINNISH_WEEKDAYS = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}


def read_data(filename: str) -> List[Row]:
    """
    Reads the CSV file and returns rows in a structured format.

    Returns:
        List of tuples:
        (timestamp_dt, c1_wh, c2_wh, c3_wh, p1_wh, p2_wh, p3_wh)
    """
    rows: List[Row] = []

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)  # skip header

        for parts in reader:
            # Example time: 2025-10-13T00:00:00
            ts = datetime.fromisoformat(parts[0])

            c1 = int(parts[1])
            c2 = int(parts[2])
            c3 = int(parts[3])
            p1 = int(parts[4])
            p2 = int(parts[5])
            p3 = int(parts[6])

            rows.append((ts, c1, c2, c3, p1, p2, p3))

    return rows


def wh_to_kwh(value_wh: float) -> float:
    """
    Converts Wh to kWh.

    Args:
        value_wh: energy in Wh

    Returns:
        energy in kWh
    """
    return value_wh / 1000.0


def to_finnish_decimal(value: float) -> str:
    """
    Formats a float with two decimals and comma as decimal separator.

    Example: 12.35 -> "12,35"
    """
    return f"{value:.2f}".replace(".", ",")


def calculate_daily_totals(rows: List[Row]) -> Totals:
    """
    Groups data by date and calculates daily totals in kWh for:
    consumption phases 1-3 and production phases 1-3.

    Returns:
        dict: date -> [c1_kwh, c2_kwh, c3_kwh, p1_kwh, p2_kwh, p3_kwh]
    """
    totals: Totals = {}

    for ts, c1, c2, c3, p1, p2, p3 in rows:
        d = ts.date()

        if d not in totals:
            totals[d] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        totals[d][0] += wh_to_kwh(c1)
        totals[d][1] += wh_to_kwh(c2)
        totals[d][2] += wh_to_kwh(c3)
        totals[d][3] += wh_to_kwh(p1)
        totals[d][4] += wh_to_kwh(p2)
        totals[d][5] += wh_to_kwh(p3)

    return totals


def print_report(daily: Totals) -> None:
    """
    Prints the weekly electricity report as a table.

    Requirements:
    - Finnish weekday name (Mon–Sun)
    - Date: dd.mm.yyyy
    - Consumption/Production in kWh (2 decimals, comma decimal separator)
    """
    print("Week 42 electricity consumption and production (kWh, by phase)\n")

    header1 = (
        "Day          Date        Consumption [kWh]               "
        "Production [kWh]"
    )
    header2 = (
        "            (dd.mm.yyyy)  v1      v2      v3             "
        "v1     v2     v3"
    )
    print(header1)
    print(header2)
    print("-" * 75)

    for d in sorted(daily.keys()):
        values = daily[d]
        weekday_name = FINNISH_WEEKDAYS[d.weekday()]
        date_str = d.strftime("%d.%m.%Y")

        c1 = to_finnish_decimal(values[0])
        c2 = to_finnish_decimal(values[1])
        c3 = to_finnish_decimal(values[2])
        p1 = to_finnish_decimal(values[3])
        p2 = to_finnish_decimal(values[4])
        p3 = to_finnish_decimal(values[5])

        print(
            f"{weekday_name:<12} {date_str:<10}  "
            f"{c1:>6}  {c2:>6}  {c3:>6}           "
            f"{p1:>6}  {p2:>6}  {p3:>6}"
        )


def main() -> None:
    """
    Main function: reads data, computes daily totals, and prints the report.
    """
    filename = Path(__file__).with_name("week42.csv")
    rows = read_data(str(filename))
    daily = calculate_daily_totals(rows)
    print_report(daily)


if __name__ == "__main__":
    main()
