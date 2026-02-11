# Copyright (c) 2025 Md Mohaimenul Islam
# License: MIT

"""
Task G (Class version)
Refactor reservations data structure from list indices to objects (class instances).

Reads reservations.txt (same folder), converts rows into Reservation objects,
and prints the same outputs as the original program.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date, time
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class Reservation:
    """Represents one reservation as an object with attributes and helper methods."""
    reservation_id: int
    name: str
    email: str
    phone: str
    date: date
    time: time
    duration: int
    price: float
    confirmed: bool
    resource: str
    created: datetime

    def is_confirmed(self) -> bool:
        """Return True if reservation is confirmed."""
        return self.confirmed

    def is_long(self) -> bool:
        """Return True if reservation is long (duration >= 3)."""
        return self.duration >= 3

    def total_price(self) -> float:
        """Return total price (duration * price)."""
        return self.duration * self.price


def convert_reservation_data(fields: List[str]) -> Reservation:
    """Convert one reservation row (list of strings) into a Reservation object."""
    return Reservation(
        reservation_id=int(fields[0]),
        name=str(fields[1]),
        email=str(fields[2]),
        phone=str(fields[3]),
        date=datetime.strptime(fields[4], "%Y-%m-%d").date(),
        time=datetime.strptime(fields[5].strip(), "%H:%M").time(),
        duration=int(fields[6]),
        price=float(fields[7]),
        confirmed=True if fields[8].strip() == "True" else False,
        resource=str(fields[9]),
        created=datetime.strptime(fields[10].strip(), "%Y-%m-%d %H:%M:%S"),
    )


def fetch_reservations(reservation_file: str) -> List[Reservation]:
    """Read reservations from a text file and return list of Reservation objects."""
    reservations: List[Reservation] = []
    with open(reservation_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split("|")
            reservations.append(convert_reservation_data(fields))
    return reservations


def confirmed_reservations(reservations: List[Reservation]) -> None:
    """Print confirmed reservations."""
    for r in reservations:
        if r.is_confirmed():
            print(f'- {r.name}, {r.resource}, {r.date.strftime("%d.%m.%Y")} at {r.time.strftime("%H.%M")}')


def long_reservations(reservations: List[Reservation]) -> None:
    """Print long reservations (duration > 3 hours) to match original logic."""
    for r in reservations:
        if r.duration > 3:
            print(
                f'- {r.name}, {r.date.strftime("%d.%m.%Y")} at {r.time.strftime("%H.%M")}, '
                f'duration {r.duration} h, {r.resource}'
            )


def confirmation_statuses(reservations: List[Reservation]) -> None:
    """Print confirmation status for each reservation."""
    for r in reservations:
        status = "Confirmed" if r.is_confirmed() else "NOT Confirmed"
        # NOTE: use ASCII "->" to avoid Windows cp1252 UnicodeEncodeError
        print(f"{r.name} -> {status}")


def confirmation_summary(reservations: List[Reservation]) -> None:
    """Print how many are confirmed vs not confirmed."""
    confirmed_count = len([r for r in reservations if r.is_confirmed()])
    not_confirmed_count = len(reservations) - confirmed_count
    print(f"- Confirmed reservations: {confirmed_count} pcs")
    print(f"- Not confirmed reservations: {not_confirmed_count} pcs")


def total_revenue(reservations: List[Reservation]) -> None:
    """Print total revenue from confirmed reservations (Finnish decimal comma)."""
    revenue = sum(r.total_price() for r in reservations if r.is_confirmed())
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
