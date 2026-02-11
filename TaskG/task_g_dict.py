# Copyright (c) 2025 Md Mohaimenul Islam
# License: MIT

"""
Task G (Dictionary version)
Refactor reservations data structure from list indices to dictionaries.

Reads reservations.txt (same folder), converts rows into dicts,
and prints the same outputs as the original program.
"""

from __future__ import annotations

from datetime import datetime, date, time
from pathlib import Path
from typing import Dict, List, Any


def convert_reservation_data(fields: List[str]) -> Dict[str, Any]:
    """Convert one reservation row (list of strings) into a dictionary with proper data types."""
    return {
        "id": int(fields[0]),
        "name": str(fields[1]),
        "email": str(fields[2]),
        "phone": str(fields[3]),
        "date": datetime.strptime(fields[4], "%Y-%m-%d").date(),
        "time": datetime.strptime(fields[5].strip(), "%H:%M").time(),
        "duration": int(fields[6]),
        "price": float(fields[7]),
        "confirmed": True if fields[8].strip() == "True" else False,
        "resource": str(fields[9]),
        "created": datetime.strptime(fields[10].strip(), "%Y-%m-%d %H:%M:%S"),
    }


def fetch_reservations(reservation_file: str) -> List[Dict[str, Any]]:
    """Read reservations from a text file and return list of reservation dictionaries."""
    reservations: List[Dict[str, Any]] = []
    with open(reservation_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split("|")
            reservations.append(convert_reservation_data(fields))
    return reservations


def confirmed_reservations(reservations: List[Dict[str, Any]]) -> None:
    """Print confirmed reservations."""
    for r in reservations:
        if r["confirmed"]:
            print(
                f'- {r["name"]}, {r["resource"]}, {r["date"].strftime("%d.%m.%Y")} '
                f'at {r["time"].strftime("%H.%M")}'
            )


def long_reservations(reservations: List[Dict[str, Any]]) -> None:
    """Print long reservations (duration >= 3 hours)."""
    for r in reservations:
        if r["duration"] > 3:
            print(
                f'- {r["name"]}, {r["date"].strftime("%d.%m.%Y")} at {r["time"].strftime("%H.%M")}, '
                f'duration {r["duration"]} h, {r["resource"]}'
            )


def confirmation_statuses(reservations: List[Dict[str, Any]]) -> None:
    """Print confirmation status for each reservation."""
    for r in reservations:
        status = "Confirmed" if r["confirmed"] else "NOT Confirmed"
        # NOTE: use ASCII "->" to avoid Windows cp1252 UnicodeEncodeError
        print(f'{r["name"]} -> {status}')


def confirmation_summary(reservations: List[Dict[str, Any]]) -> None:
    """Print how many are confirmed vs not confirmed."""
    confirmed_count = len([r for r in reservations if r["confirmed"]])
    not_confirmed_count = len(reservations) - confirmed_count
    print(f"- Confirmed reservations: {confirmed_count} pcs")
    print(f"- Not confirmed reservations: {not_confirmed_count} pcs")


def total_revenue(reservations: List[Dict[str, Any]]) -> None:
    """Print total revenue from confirmed reservations (Finnish decimal comma)."""
    revenue = sum((r["duration"] * r["price"]) for r in reservations if r["confirmed"])
    print(f"Total revenue from confirmed reservations: {revenue:.2f} EUR".replace(".", ","))


def main() -> None:
    """Main: load reservations from same folder and print required sections."""
    base_dir = Path(__file__).parent
    reservations_path = base_dir / "reservations.txt"

    reservations = fetch_reservations(str(reservations_path))

    print("1) Confirmed Reservations")
    confirmed_reservations(reservations)

    # NOTE: use >= (ASCII) to avoid UnicodeEncodeError
    print("2) Long Reservations (>= 3 h)")
    long_reservations(reservations)

    print("3) Reservation Confirmation Status")
    confirmation_statuses(reservations)

    print("4) Confirmation Summary")
    confirmation_summary(reservations)

    print("5) Total Revenue from Confirmed Reservations")
    total_revenue(reservations)


if __name__ == "__main__":
    main()
