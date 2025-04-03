"""
******************************
CS 1026 - Assignment 4  – Air Travel
Code by: Sydney Koziel
Student ID: skoziel
File created: March 26, 2025
******************************
This file defines the Flight class.
Each Flight object represents a flight route from an origin Airport
to a destination Airport, including a flight number and duration.
It includes methods for comparison, combining flights (__add__),
determining if a flight is domestic, string representation, and
accessing/modifying flight attributes. It imports the Airport class.
"""
from Airport import * # Import the Airport class [cite: 29, 30]


class Flight:
    """Represents a flight between two airports."""

    def __init__(self, origin, destination, flight_number, duration):
        """Initializes a Flight object."""
        # Check if origin and destination are Airport objects [cite: 36, 37]
        if not isinstance(origin, Airport) or not isinstance(destination, Airport):
            raise TypeError("The origin and destination must be Airport objects")  # Raise TypeError if not Airport objects [cite: 37]

        self._origin = origin  # Initialize origin Airport [cite: 38]
        self._destination = destination  # Initialize destination Airport [cite: 38]
        self._flight_number = flight_number  # Initialize flight number [cite: 38]
        self._duration = duration  # Initialize duration [cite: 38]

    def __str__(self):
        """Returns the string representation of the Flight."""
        duration_int = int(round(self._duration))  # Round duration to nearest int [cite: 40]
        flight_type = "domestic" if self.is_domestic() else "international"  # Determine if flight is domestic or international [cite: 40, 48, 49]

        return f"{self._origin.get_city()} to {self._destination.get_city()} ({flight_type}) [{duration_int}h]"  # Format the string [cite: 41]

    def __eq__(self, other):
        """Checks if two Flight objects are equal based on origin and destination."""
        if not isinstance(other, Flight):  # Check if other is a Flight object [cite: 42]
            return False
        # Two flights are considered the same if they have the same origin and destination airports [cite: 41]
        return self._origin == other._origin and self._destination == other._destination

    def __add__(self, connecting_flight):
        """Combines two flights if the first ends where the second begins."""
        # Check if connecting_flight is a Flight object [cite: 43, 44]
        if not isinstance(connecting_flight, Flight):
            raise TypeError("The connecting_flight must be a Flight object")  # Raise TypeError if not a Flight object [cite: 43, 44]

        # Check if the destination of the first flight is the origin of the connecting flight [cite: 45, 46]
        if self._destination != connecting_flight._origin:
            raise ValueError("These flights cannot be combined")  # Raise ValueError if flights cannot be combined [cite: 46]

        # Create and return a new Flight object representing the combined flights [cite: 47]
        new_flight = Flight(
            self._origin,                       # Origin of the first flight [cite: 47]
            connecting_flight._destination,    # Destination of the second flight [cite: 47]
            self._flight_number,               # Use the flight number of the first flight [cite: 47]
            self._duration + connecting_flight._duration  # Sum the durations [cite: 47]
        )
        return new_flight

    def get_number(self):
        """Returns the flight number."""
        return self._flight_number

    def get_origin(self):
        """Returns the origin Airport object."""
        return self._origin

    def get_destination(self):
        """Returns the destination Airport object."""
        return self._destination

    def get_duration(self):
        """Returns the flight duration in hours."""
        return self._duration

    def is_domestic(self):
        """Returns True if the flight is domestic, False otherwise."""
        # A flight is domestic if origin and destination are in the same country [cite: 48, 49]
        return self._origin.get_country() == self._destination.get_country()

    def set_origin(self, origin):
        """Updates the origin Airport of the flight."""
        if not isinstance(origin, Airport):
            raise TypeError("The origin must be an Airport object")
        self._origin = origin

    def set_destination(self, destination):
        """Updates the destination Airport of the flight."""
        if not isinstance(destination, Airport):
            raise TypeError("The destination must be an Airport object")
        self._destination = destination


# Optional test cases within the main block
if __name__ == '__main__':
    # Setup for Flight tests
    airport1 = Airport("Canada", "Toronto", "YYZ")
    airport2 = Airport("United States", "Chicago", "ORD")
    airport3 = Airport("United States", "New York", "JFK")
    airport4 = Airport("Canada", "Montreal", "YUL")

    flight1 = Flight(airport1, airport2, "AC-789", 3.5) # Toronto to Chicago
    flight2 = Flight(airport2, airport3, "UA-456", 2.0) # Chicago to New York
    flight3 = Flight(airport1, airport4, "AC-123", 1.2) # Toronto to Montreal (Domestic)
    flight4 = Flight(airport1, airport2, "UA-999", 3.6) # Another Toronto to Chicago

    print("\n--- Flight Class Tests ---")
    print(f"Flight 1: {flight1}") # International, 4h
    print(f"Flight 3: {flight3}") # Domestic, 1h

    print(f"flight1 == flight2: {flight1 == flight2}") # False
    print(f"flight1 == flight4: {flight1 == flight4}") # True (same origin/dest)
    print(f"flight1 == 'AC-789': {flight1 == 'AC-789'}") # False

    print(f"Flight 1 Number: {flight1.get_number()}")
    print(f"Flight 1 Origin: {flight1.get_origin()}")
    print(f"Flight 1 Destination: {flight1.get_destination()}")
    print(f"Flight 1 Duration: {flight1.get_duration()}")
    print(f"Flight 1 Domestic?: {flight1.is_domestic()}") # False
    print(f"Flight 3 Domestic?: {flight3.is_domestic()}") # True

    print("Testing flight combination (flight1 + flight2):")
    try:
        combined_flight = flight1 + flight2 # YYZ -> ORD + ORD -> JFK should work
        print(f"Combined Flight: {combined_flight}") # Toronto to New York (international) [6h]
        print(f"Combined Flight Origin: {combined_flight.get_origin()}")
        print(f"Combined Flight Destination: {combined_flight.get_destination()}")
        print(f"Combined Flight Duration: {combined_flight.get_duration()}")
        print(f"Combined Flight Number: {combined_flight.get_number()}") # Should be flight1's number
    except (ValueError, TypeError) as e:
        print(f"Error combining flights: {e}")

    print("Testing invalid flight combination (flight2 + flight1):")
    try:
        # ORD -> JFK + YYZ -> ORD : Invalid combination
        invalid_combined_flight = flight2 + flight1
        print(invalid_combined_flight)
    except ValueError as e:
        print(f"Caught expected error: {e}") # Should print "These flights cannot be combined"

    print("Testing adding non-Flight object:")
    try:
        invalid_add = flight1 + "not a flight"
    except TypeError as e:
        print(f"Caught expected error: {e}") # Should print "The connecting_flight must be a Flight object"

    print("-" * 25)