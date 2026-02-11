# Copyright (c) 2026 Ville Heikkiniemi, Luka Hietala, Luukas Kola
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Modified by nnn according to given task

"""
A program that prints reservation information according to requirements

The data structure and example data record:

reservationId | name | email | phone | reservationDate | reservationTime | durationHours | price | confirmed | reservedResource | createdAt
------------------------------------------------------------------------
201 | Moomin Valley | moomin@whitevalley.org | 0509876543 | 2025-11-12 | 09:00:00 | 2 | 18.50 | True | Forest Area 1 | 2025-08-12 14:33:20
int | str | str | str | date | time | int | float | bool | str | datetime

"""

from datetime import datetime


def convert_reservation_data(reservation: list) -> list:
    """
    Convert data types to meet program requirements

    Parameters:
     reservation (list): Unconverted reservation -> 11 columns 

    Returns:
     converted (list): Converted data types
    """
    converted = []
    converted.append(int(reservation[0]))  # reservationId (str -> int)
    converted.append(str(reservation[1]))  # name (str)
    converted.append(str(reservation[2]))  # email (str)
    converted.append(str(reservation[3]))  # phone (str)
    converted.append(datetime.strptime(reservation[4], "%Y-%m-%d").date())  # reservationDate (date)
    converted.append(datetime.strptime(reservation[5], "%H:%M").time())  # reservationTime (time)
    converted.append(int(reservation[6]))  # durationHours (int)
    converted.append(float(reservation[7]))  # price (float)
    converted.append(True if reservation[8].strip() == 'True' else False)  # confirmed (bool)
    converted.append(str(reservation[9]))  # reservedResource (str)
    converted.append(datetime.strptime(str(reservation[10]).strip(), "%Y-%m-%d %H:%M:%S"))  # createdAt (datetime)
    return converted


def fetch_reservations(reservation_file: str) -> list[list]:
    """
    Reads reservations from a file and returns the reservations converted
    You don't need to modify this function!

    Parameters:
     reservation_file (str): Name of the file containing the reservations

    Returns:
     reservations (list): Read and converted reservations
    """
    reservations = []
    reservations.append(
        [
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
    )
    with open(reservation_file, "r", encoding="utf-8") as f:
        for line in f:
            if len(line) > 1:
                fields = line.split("|")
                reservations.append(convert_reservation_data(fields))
    return reservations

def confirmed_reservations(reservations: list[list]) -> None:
    """
    Print confirmed reservations

    Parameters:
     reservations (list): Reservations
    """
    for reservation in reservations[1:]:
        if reservation[8]: # If confirmed
            print(f'- {reservation[1]}, {reservation[-2]}, {reservation[4].strftime("%d.%m.%Y")} at {reservation[5].strftime("%H.%M")}')

def long_reservations(reservations : list[list]) -> None:
    """
    Print long reservations

    Parameters:
     reservations (list): Reservations
    """
    for reservation in reservations[1:]:
        if reservation[6] > 3: # If long
            print(f'- {reservation[1]}, {reservation[4].strftime("%d.%m.%Y")} at {reservation[5].strftime("%H.%M")}, duration {reservation[6]} h, {reservation[-2]}')


def confirmation_statuses(reservations: list[list]) -> None:
    """
    Print confirmation statuses

    Parameters:
     reservations (list): Reservations
    """
    for reservation in reservations[1:]:
        name : str = reservation[1]
        confirmed : bool = reservation[8]

        print(f'{name} → {"Confirmed" if confirmed else "NOT Confirmed"}')

def confirmation_summary(reservations: list[list]) -> None:
    """
    Print confirmation summary

    Parameters:
     reservations (list): Reservations
    """
    confirmed : int = len([x for x in reservations[1:] if x[8]])
    print(f'- Confirmed reservations: {confirmed} pcs\n- Not confirmed reservations: {len(reservations) - confirmed} pcs')

def total_revenue(reservations: list[list]) -> None:
    """
    Print total revenue

    Parameters:
     reservations (list): Reservations
    """
    revenue : float = sum(x[6] * x[7] for x in reservations[1:] if x[8])
    print(f'Total revenue from confirmed reservations: {revenue:.2f} €'.replace('.', ','))

def main():
    """
    Prints reservation information according to requirements
    Reservation-specific printing is done in functions
    """
    reservations = fetch_reservations("reservations.txt")
    print("1) Confirmed Reservations")
    confirmed_reservations(reservations)
    print("2) Long Reservations (≥ 3 h)")
    long_reservations(reservations)
    print("3) Reservation Confirmation Status")
    confirmation_statuses(reservations)
    print("4) Confirmation Summary")
    confirmation_summary(reservations)
    print("5) Total Revenue from Confirmed Reservations")
    total_revenue(reservations)

if __name__ == "__main__":
    main()