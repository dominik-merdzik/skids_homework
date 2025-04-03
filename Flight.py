"""
******************************
CS 1026 - Assignment 4  – Air Travel
Code by: Sydney Koziel
Student ID: skoziel
File created: March 26, 2025
******************************
COMMENT
"""
# from Airport import *
#
#
# class Flight:
#     def __init__(self, origin, destination, flight_number, duration):
#         if not isinstance(origin, Airport) or not isinstance(destination, Airport):
#             raise TypeError("The origin and destination must be Airport objects")
#
#         self._origin = origin
#         self._destination = destination
#         self._flight_number = flight_number
#         self._duration = duration
#
#     def __str__(self):
#         flight_type = "domestic" if self.is_domestic() else "international"
#         return f"{self._origin.get_city()} to {self._destination.get_city()} ({flight_type}) [{round(self._duration)}h]"
#
#     def __eq__(self, other):
#         if not isinstance(other, Flight):
#             return False
#         return self._origin == other._origin and self._destination == other._destination
#
#     def __add__(self, conn_flight):
#         if not isinstance(conn_flight, Flight):
#             raise TypeError("The connecting flight must be a Flight object")
#         if self._destination != conn_flight._origin:
#             raise ValueError("These flights cannot be combined")
#         return Flight(self._origin, conn_flight._destination, self._flight_number,
#                       self._duration + conn_flight._duration)
#
#     def get_number(self):
#         return self._flight_number
#
#     def get_origin(self):
#         return self._origin
#
#     def get_destination(self):
#         return self._destination
#
#     def get_duration(self):
#         return self._duration
#
#     def is_domestic(self):
#         return self._origin.get_country() == self._destination.get_country()
#
#     def set_origin(self, origin):
#         if not isinstance(origin, Airport):
#             raise TypeError("The origin must be an Airport object")
#         self._origin = origin
#
#     def set_destination(self, destination):
#         if not isinstance(destination, Airport):
#             raise TypeError("The destination must be an Airport object")
#         self._destination = destination

from Airport import * # Import the Airport class [cite: 29, 30]


class Flight:
    def __init__(self, origin, destination, flight_number, duration):
        # Check if origin and destination are Airport objects [cite: 36, 37]
        if not isinstance(origin, Airport) or not isinstance(destination, Airport):
            raise TypeError("The origin and destination must be Airport objects")  # Raise TypeError if not Airport objects [cite: 37]

        self._origin = origin  # Initialize origin Airport [cite: 38]
        self._destination = destination  # Initialize destination Airport [cite: 38]
        self._flight_number = flight_number  # Initialize flight number [cite: 38]
        self._duration = duration  # Initialize duration [cite: 38]

    def __str__(self):
        duration_int = int(round(self._duration))  # Round duration to nearest int [cite: 40]
        flight_type = "domestic" if self.is_domestic() else "international"  # Determine if flight is domestic or international [cite: 40, 48, 49]

        return f"{self._origin.get_city()} to {self._destination.get_city()} ({flight_type}) [{duration_int}h]"  # Format the string [cite: 41]

    def __eq__(self, other):
        if not isinstance(other, Flight):  # Check if other is a Flight object [cite: 42]
            return False
        return self._origin == other._origin and self._destination == other._destination  # Compare origin and destination [cite: 41]

    def __add__(self, connecting_flight):
        # Check if connecting_flight is a Flight object [cite: 43, 44]
        if not isinstance(connecting_flight, Flight):
            raise TypeError("The connecting_flight must be a Flight object")  # Raise TypeError if not a Flight object [cite: 43, 44]

        # Check if the destination of the first flight is the origin of the connecting flight [cite: 45, 46]
        if self._destination != connecting_flight._origin:
            raise ValueError("These flights cannot be combined")  # Raise ValueError if flights cannot be combined [cite: 46]

        # Create and return a new Flight object representing the combined flights [cite: 47]
        new_flight = Flight(
            self._origin,
            connecting_flight._destination,
            self._flight_number,  # Use the flight number of the first flight [cite: 47]
            self._duration + connecting_flight._duration,  # Sum the durations [cite: 47]
        )
        return new_flight

    def get_number(self):
        return self._flight_number

    def get_origin(self):
        return self._origin

    def get_destination(self):
        return self._destination

    def get_duration(self):
        return self._duration

    def is_domestic(self):
        return self._origin.get_country() == self._destination.get_country()  # Compare origin and destination countries [cite: 48, 49]

    def set_origin(self, origin):
        if not isinstance(origin, Airport):
            raise TypeError("The origin must be an Airport object")
        self._origin = origin

    def set_destination(self, destination):
        if not isinstance(destination, Airport):
            raise TypeError("The destination must be an Airport object")
        self._destination = destination


if __name__ == '__main__':
    try:
        combined_flight = flight2 + flight1
        print(combined_flight)
    except ValueError as e:
        print(e)

    try:
        invalid_add = flight1 + "not a flight"
    except TypeError as e:
        print(e)