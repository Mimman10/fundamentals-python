from datetime import datetime
from pathlib import Path


def print_reservation_number(reservation: list[str]) -> None:
    """Prints the reservation number (int)."""
    reservation_number = int(reservation[0])
    print(f"Reservation number: {reservation_number}")


def print_booker(reservation: list[str]) -> None:
    """Prints the booker name (str)."""
    booker = reservation[1]
    print(f"Booker: {booker}")


def print_date(reservation: list[str]) -> None:
    """Prints the date in Finnish format (dd.mm.yyyy)."""
    day = datetime.strptime(reservation[2], "%Y-%m-%d").date()
    finnish_day = day.strftime("%d.%m.%Y")
    print(f"Date: {finnish_day}")


def print_start_time(reservation: list[str]) -> None:
    """Prints the start time in Finnish format (hh.mm)."""
    start_time = datetime.strptime(reservation[3], "%H:%M").time()
    finnish_time = start_time.strftime("%H.%M")
    print(f"Start time: {finnish_time}")


def print_hours(reservation: list[str]) -> None:
    """Prints the number of hours (int)."""
    hours = int(reservation[4])
    print(f"Number of hours: {hours}")


def print_hourly_rate(reservation: list[str]) -> None:
    """Prints the hourly price in Finnish format with €."""
    hourly_price = float(reservation[5])
    hourly_price_str = f"{hourly_price:.2f}".replace(".", ",")
    print(f"Hourly price: {hourly_price_str} €")


def print_total_price(reservation: list[str]) -> None:
    """Prints the total price (hours * hourly price) in Finnish format with €."""
    hours = int(reservation[4])
    hourly_price = float(reservation[5])
    total_price = hours * hourly_price
    total_price_str = f"{total_price:.2f}".replace(".", ",")
    print(f"Total price: {total_price_str} €")


def print_paid(reservation: list[str]) -> None:
    """Prints 'Yes' if paid is True, otherwise 'No'."""
    paid = reservation[6] == "True"
    print(f"Paid: {'Yes' if paid else 'No'}")


def print_venue(reservation: list[str]) -> None:
    """Prints the venue/location (str)."""
    venue = reservation[7]
    print(f"Location: {venue}")


def print_phone(reservation: list[str]) -> None:
    """Prints the phone number (str)."""
    phone = reservation[8]
    print(f"Phone: {phone}")


def print_email(reservation: list[str]) -> None:
    """Prints the email (str)."""
    email = reservation[9]
    print(f"Email: {email}")


def main() -> None:
    """Reads reservation data from a file and prints it using functions."""
    filename = Path(__file__).with_name("reservations.txt")

    with open(filename, "r", encoding="utf-8") as f:
        line = f.readline().strip()

    reservation = line.split("|")

    print_reservation_number(reservation)
    print_booker(reservation)
    print_date(reservation)
    print_start_time(reservation)
    print_hours(reservation)
    print_hourly_rate(reservation)
    print_total_price(reservation)
    print_paid(reservation)
    print_venue(reservation)
    print_phone(reservation)
    print_email(reservation)


if __name__ == "__main__":
    main()
