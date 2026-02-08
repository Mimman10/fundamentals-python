# Copyright (c) 2025 Mohaimenul Islam
# License: MIT

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Measurement:
    """Represents one hourly measurement row from the CSV file."""
    timestamp: datetime
    consumption_kwh: float
    production_kwh: float
    temperature_c: float


def parse_float_fi(value: str) -> float:
    """Parses a number that may use Finnish decimal comma into float."""
    return float(value.strip().replace(",", "."))


def format_float_fi(value: float) -> str:
    """Formats a float with 2 decimals and Finnish decimal comma."""
    return f"{value:.2f}".replace(".", ",")


def format_date_fi(d: date) -> str:
    """Formats a date as dd.mm.yyyy."""
    return f"{d.day}.{d.month}.{d.year}"


def read_data(path: Path) -> List[Measurement]:
    """
    Reads 2025.csv and returns a list of Measurement rows.
    The CSV is expected to contain:
      timestamp, consumption (kWh), production (kWh), temperature (°C)
    Separator may be ';' or ',' (auto-detected).
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    # detect delimiter using a small sample
    sample = path.read_text(encoding="utf-8", errors="ignore")[:2000]
    delimiter = ";" if sample.count(";") >= sample.count(",") else ","

    rows: List[Measurement] = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=delimiter)

        # normalize header keys
        fieldnames = reader.fieldnames or []
        normalized = {name: name.strip() for name in fieldnames}

        # Try to find columns by common names
        # You can adjust these if your file uses different headers.
        def find_col(candidates: List[str]) -> str:
            for cand in candidates:
                for fn in normalized.values():
                    if fn.lower() == cand.lower():
                        return fn
            # fallback: try contains
            for cand in candidates:
                for fn in normalized.values():
                    if cand.lower() in fn.lower():
                        return fn
            raise ValueError(f"Could not find column. Tried: {candidates}. Found headers: {fieldnames}")

        col_time = find_col(["timestamp", "aika", "time"])
        col_cons = find_col(["consumption", "kulutus", "consumption (net) in kwh", "consumption_kwh"])
        col_prod = find_col(["production", "tuotanto", "production (net) in kwh", "production_kwh"])
        col_temp = find_col(["temperature", "avg temperature", "daily average temperature", "lampotila", "lämpötila", "temp"])

        for row in reader:
            time_str = (row.get(col_time) or "").strip()
            if not time_str:
                continue

            # Timestamp is ISO like 2025-10-13T00:00:00
            ts = datetime.fromisoformat(time_str)

            cons = parse_float_fi(str(row.get(col_cons, "0")))
            prod = parse_float_fi(str(row.get(col_prod, "0")))
            temp = parse_float_fi(str(row.get(col_temp, "0")))

            rows.append(Measurement(ts, cons, prod, temp))

    if not rows:
        raise ValueError("No rows were read. Check delimiter and column names in 2025.csv.")
    return rows


def build_daily_index(rows: List[Measurement]) -> Dict[date, List[Measurement]]:
    """Groups measurements by date."""
    daily: Dict[date, List[Measurement]] = {}
    for m in rows:
        d = m.timestamp.date()
        daily.setdefault(d, []).append(m)
    return daily


def parse_date_input(prompt: str) -> date:
    """
    Asks user for a date in dd.mm.yyyy format and returns a date object.
    Keeps asking until valid.
    """
    while True:
        raw = input(prompt).strip()
        try:
            # accept both "1.11.2025" and "01.11.2025"
            parts = raw.split(".")
            if len(parts) != 3:
                raise ValueError
            day = int(parts[0])
            month = int(parts[1])
            year = int(parts[2])
            return date(year, month, day)
        except ValueError:
            print("Invalid date. Use format dd.mm.yyyy (e.g., 1.11.2025 or 01.11.2025).")


def ask_int_in_range(prompt: str, min_v: int, max_v: int) -> int:
    """Asks user for an integer in [min_v, max_v]."""
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if min_v <= val <= max_v:
                return val
            print(f"Please enter a number between {min_v} and {max_v}.")
        except ValueError:
            print("Invalid number. Try again.")


def show_main_menu() -> str:
    """Prints the main menu and returns the user selection."""
    print("\nChoose a report type:")
    print("1) Daily summary for a date range")
    print("2) Monthly summary for one month")
    print("3) Full year 2025 summary")
    print("4) Exit the program")
    return input("Choose (1-4): ").strip()


def show_after_menu() -> str:
    """Shows the post-report menu and returns the user selection."""
    print("\nWhat would you like to do next?")
    print("1) Write the report to the file report.txt")
    print("2) Create a new report")
    print("3) Exit")
    return input("Choose (1-3): ").strip()


def create_daily_report(daily: Dict[date, List[Measurement]]) -> List[str]:
    """Builds a report for a selected date range (inclusive)."""
    start = parse_date_input("Enter start date (dd.mm.yyyy): ")
    end = parse_date_input("Enter end date (dd.mm.yyyy): ")

    if end < start:
        start, end = end, start  # swap

    total_cons = 0.0
    total_prod = 0.0
    temps: List[float] = []

    cur = start
    while cur <= end:
        rows = daily.get(cur, [])
        for m in rows:
            total_cons += m.consumption_kwh
            total_prod += m.production_kwh
            temps.append(m.temperature_c)
        cur = date.fromordinal(cur.toordinal() + 1)

    avg_temp = (sum(temps) / len(temps)) if temps else 0.0

    lines = [
        "-" * 53,
        f"Report for the period {format_date_fi(start)}–{format_date_fi(end)}",
        f"- Total consumption: {format_float_fi(total_cons)} kWh",
        f"- Total production: {format_float_fi(total_prod)} kWh",
        f"- Average temperature: {format_float_fi(avg_temp)} °C",
    ]
    return lines


def month_name_en(month: int) -> str:
    """Returns English month name (as in examples)."""
    names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]
    return names[month - 1]


def create_monthly_report(daily: Dict[date, List[Measurement]]) -> List[str]:
    """Builds a monthly summary report for a selected month number (1–12)."""
    month = ask_int_in_range("Enter month number (1–12): ", 1, 12)

    total_cons = 0.0
    total_prod = 0.0
    daily_avg_temps: List[float] = []

    # For each day in the year that matches the month
    for d, rows in daily.items():
        if d.year == 2025 and d.month == month:
            day_cons = sum(m.consumption_kwh for m in rows)
            day_prod = sum(m.production_kwh for m in rows)
            day_temp_avg = (sum(m.temperature_c for m in rows) / len(rows)) if rows else 0.0

            total_cons += day_cons
            total_prod += day_prod
            daily_avg_temps.append(day_temp_avg)

    avg_temp = (sum(daily_avg_temps) / len(daily_avg_temps)) if daily_avg_temps else 0.0

    lines = [
        "-" * 53,
        f"Report for the month: {month_name_en(month)}",
        f"- Total consumption: {format_float_fi(total_cons)} kWh",
        f"- Total production: {format_float_fi(total_prod)} kWh",
        f"- Average temperature: {format_float_fi(avg_temp)} °C",
    ]
    return lines


def create_yearly_report(rows: List[Measurement]) -> List[str]:
    """Builds a full-year 2025 summary report."""
    year_rows = [m for m in rows if m.timestamp.year == 2025]

    total_cons = sum(m.consumption_kwh for m in year_rows)
    total_prod = sum(m.production_kwh for m in year_rows)
    avg_temp = (sum(m.temperature_c for m in year_rows) / len(year_rows)) if year_rows else 0.0

    lines = [
        "-" * 53,
        "Report for the year: 2025",
        f"- Total consumption: {format_float_fi(total_cons)} kWh",
        f"- Total production: {format_float_fi(total_prod)} kWh",
        f"- Average temperature: {format_float_fi(avg_temp)} °C",
    ]
    return lines


def print_report_to_console(lines: List[str]) -> None:
    """Prints report lines to the console."""
    for line in lines:
        print(line)


def write_report_to_file(path: Path, lines: List[str]) -> None:
    """Writes report lines to report.txt (overwrites old content)."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main() -> None:
    """
    Main function: reads data, shows menus, generates reports,
    and optionally writes them to report.txt.
    """
    base_dir = Path(__file__).parent
    csv_path = base_dir / "2025.csv"
    out_path = base_dir / "report.txt"

    rows = read_data(csv_path)
    daily = build_daily_index(rows)

    last_report: List[str] = []

    while True:
        choice = show_main_menu()

        if choice == "1":
            last_report = create_daily_report(daily)
            print_report_to_console(last_report)

        elif choice == "2":
            last_report = create_monthly_report(daily)
            print_report_to_console(last_report)

        elif choice == "3":
            last_report = create_yearly_report(rows)
            print_report_to_console(last_report)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Unknown choice. Please select 1-4.")
            continue

        # After-report menu
        while True:
            after = show_after_menu()
            if after == "1":
                write_report_to_file(out_path, last_report)
                print(f"Wrote report to {out_path.name}")
            elif after == "2":
                break  # back to main menu
            elif after == "3":
                print("Goodbye!")
                return
            else:
                print("Unknown choice. Please select 1-3.")


if __name__ == "__main__":
    main()
