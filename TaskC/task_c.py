from datetime import datetime
from pathlib import Path

HEADERS = [
    "reservationId",
    "name",
    "email",
    "phone",
    "reservationDate",
    "reservationTime",
    "durationHours",
    "price",
    "confirmed",
    "reservedResource",
    "createdAt",
]


def convert_reservation_data(reservation: list) -> list:
    """
    Convert data types to meet program requirements

    Parameters:
     reservation (list): Unconverted reservation -> 11 columns (strings)

    Returns:
     converted (list): Converted data types in correct order
    """
    # Clean values (remove newline etc.)
    row = [x.strip() for x in reservation]

    reservation_id = int(row[0])
    name = row[1]
    email = row[2]
    phone = row[3]

    reservation_date = datetime.strptime(row[4], "%Y-%m-%d").date()
    reservation_time = datetime.strptime(row[5], "%H:%M").time()

    duration_hours = int(row[6])
    price = float(row[7])

    confirmed = (row[8] == "True")

    reserved_resource = row[9]
    created_at = datetime.strptime(row[10], "%Y-%m-%d %H:%M:%S")

    return [
        reservation_id,
        name,
        email,
        phone,
        reservation_date,
        reservation_time,
        duration_hours,
        price,
        confirmed,
        reserved_resource,
        created_at,
    ]


def fetch_reservations(reservation_file: str) -> list:
    """
    Reads reservations from a file and returns the reservations converted
    You don't need to modify this function!
    """
    reservations = []
    with open(reservation_file, "r", encoding="utf-8") as f:
        for line in f:
            fields = line.split("|")
            reservations.append(convert_reservation_data(fields))
    return reservations


def confirmed_reservations(reservations: list[list]) -> None:
    """1) Print confirmed reservations in required format."""
    for r in reservations:
        if r[8]:
            name = r[1]
            resource = r[9]
            date_fi = r[4].strftime("%d.%m.%Y")
            time_fi = r[5].strftime("%H.%M")
            print(f"- {name}, {resource}, {date_fi} at {time_fi}")


def long_reservations(reservations: list[list]) -> None:
    """2) Print long reservations (duration >= 3h) in required format."""
    for r in reservations:
        duration = r[6]
        if duration >= 3:
            name = r[1]
            date_fi = r[4].strftime("%d.%m.%Y")
            time_fi = r[5].strftime("%H.%M")
            resource = r[9]
            print(f"- {name}, {date_fi} at {time_fi}, duration {duration} h, {resource}")


def confirmation_statuses(reservations: list[list]) -> None:
    """3) Print confirmation status for each reservation."""
    for r in reservations:
        name = r[1]
        confirmed = r[8]
        status = "Confirmed" if confirmed else "NOT Confirmed"
        print(f"{name} -> {status}")  # safer than unicode arrow


def confirmation_summary(reservations: list[list]) -> None:
    """4) Print summary counts for confirmed vs not confirmed."""
    confirmed_count = 0
    not_confirmed_count = 0

    for r in reservations:
        if r[8]:
            confirmed_count += 1
        else:
            not_confirmed_count += 1

    print(f"- Confirmed reservations: {confirmed_count} pcs")
    print(f"- Not confirmed reservations: {not_confirmed_count} pcs")


def total_revenue(reservations: list[list]) -> None:
    """5) Print total revenue from confirmed reservations (comma decimal)."""
    total = 0.0

    for r in reservations:
        if r[8]:
            duration = r[6]
            price = r[7]
            total += duration * price

    total_str = f"{total:.2f}".replace(".", ",")
    print(f"Total revenue from confirmed reservations: {total_str} EUR")


def main() -> None:
    """Prints reservation information according to requirements (PART B only)."""
    filename = Path(__file__).with_name("reservations.txt")
    reservations = fetch_reservations(str(filename))

    print("1) Confirmed Reservations")
    confirmed_reservations(reservations)
    print()

    # FIX: >= instead of ≥ (prevents UnicodeEncodeError in cp1252)
    print("2) Long Reservations (>= 3 h)")
    long_reservations(reservations)
    print()

    print("3) Reservation Confirmation Status")
    confirmation_statuses(reservations)
    print()

    print("4) Confirmation Summary")
    confirmation_summary(reservations)
    print()

    print("5) Total Revenue from Confirmed Reservations")
    total_revenue(reservations)


if __name__ == "__main__":
    main()
