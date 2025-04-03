"""
******************************
CS 1026 - Assignment 4  – Air Travel
Code by: Sydney Koziel
Student ID: skoziel
File created: March 26, 2025
******************************
COMMENT
"""
# from Flight import *
#
# class MaintenanceRecord:
#     def __init__(self, input_line, all_flights, all_airports):
#         parts = input_line.strip().split('-')
#
#         if len(parts) != 5:
#             raise ValueError("Invalid data string")
#
#         flight_number, airport_code, duration, cost_per_hour = parts[0] + '-' + parts[1], parts[2], parts[3], parts[4]
#
#         if flight_number not in all_flights:
#             raise ValueError("Flight not found")
#         if airport_code not in all_airports:
#             raise ValueError("Airport not found")
#
#         self._flight = all_flights[flight_number]
#         self._maintenance_airport = all_airports[airport_code]
#         self._maintenance_duration = float(duration)
#         self._maintenance_cost_per_hour = float(cost_per_hour)
#
#     def get_total_cost(self):
#         return self._maintenance_duration * self._maintenance_cost_per_hour
#
#     def get_duration(self):
#         return self._maintenance_duration
#
#     def __str__(self):
#         return (f"{self._flight.get_number()} ({self._flight}) from {self._flight.get_origin().get_code()} "
#                 f"[{self._flight.get_origin().get_city()}, {self._flight.get_origin().get_country()}] "
#                 f"to be maintained at {self._maintenance_airport.get_code()} "
#                 f"[{self._maintenance_airport.get_city()}, {self._maintenance_airport.get_country()}] "
#                 f"for {self._maintenance_duration} hours @ ${self._maintenance_cost_per_hour:.1f}/hour "
#                 f"(${self.get_total_cost():.1f})")
#
#     def __eq__(self, other):
#         if not isinstance(other, MaintenanceRecord):
#             return False
#         return (self._flight == other._flight and
#                 self._maintenance_airport == other._maintenance_airport and
#                 self._maintenance_duration == other._maintenance_duration and
#                 self._maintenance_cost_per_hour == other._maintenance_cost_per_hour)
#
#     def __ne__(self, other):
#         return not self.__eq__(other)
#
#     def __lt__(self, other):
#         return self.get_total_cost() < other.get_total_cost()
#
#     def __le__(self, other):
#         return self.get_total_cost() <= other.get_total_cost()
#
#     def __gt__(self, other):
#         return self.get_total_cost() > other.get_total_cost()
#
#     def __ge__(self, other):
#         return self.get_total_cost() >= other.get_total_cost()


from Flight import Flight
from Airport import Airport


class MaintenanceRecord:
    def __init__(self, input_line, all_flights, all_airports):
        parts = input_line.strip().split('-')  # Split the line into parts, removing extra whitespace

        if len(parts) != 4 or not parts[0] or not parts[1] or not parts[2] or not parts[3]:
            raise ValueError("Invalid data string")  # Raise ValueError for invalid input

        flight_number = parts[0].strip()
        airport_code = parts[1].strip()
        duration_str = parts[2].strip()
        cost_per_hour_str = parts[3].strip()

        if not self._is_valid_flight_number(flight_number):
            raise ValueError("Invalid data string")

        try:
            self._maintenance_duration = float(duration_str)
            self._maintenance_cost_per_hour = float(cost_per_hour_str)
        except ValueError:
            raise ValueError("Invalid data string")

        if flight_number not in all_flights:
            raise ValueError("Flight not found")
        self._flight = all_flights[flight_number]

        found_airport = None
        if isinstance(all_airports, dict):
            if airport_code not in all_airports:
                raise ValueError("Airport not found")
            found_airport = all_airports[airport_code]
        elif isinstance(all_airports, list):
            for airport in all_airports:
                if airport.get_code() == airport_code:
                    found_airport = airport
                    break
            if not found_airport:
                raise ValueError("Airport not found")
        self._maintenance_airport = found_airport

    def _is_valid_flight_number(self, flight_number):
        if len(flight_number) != 7 or flight_number[3] != '-':
            return False
        if not flight_number[:3].isalpha() or not flight_number[4:].isdigit():
            return False
        return True

    def get_total_cost(self):
        return self._maintenance_cost_per_hour * self._maintenance_duration

    def get_duration(self):
        return self._maintenance_duration

    def __str__(self):
        flight_str = str(self._flight) if self._flight else "None"
        origin_airport_str = str(self._flight.get_origin()) if self._flight else "None"
        maintenance_airport_str = str(self._maintenance_airport) if self._maintenance_airport else "None"
        total_cost = self.get_total_cost()

        return (
            f"{self._flight.get_number()} ({flight_str}) from {origin_airport_str} "
            f"to be maintained at {maintenance_airport_str} for {self._maintenance_duration} hours "
            f"@ ${self._maintenance_cost_per_hour}/hour (${total_cost})"
        )

    def __eq__(self, other):
        if not isinstance(other, MaintenanceRecord):
            return False
        return (
            self._flight == other._flight
            and self._maintenance_airport == other._maintenance_airport
            and self._maintenance_duration == other._maintenance_duration
            and self._maintenance_cost_per_hour == other._maintenance_cost_per_hour
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.get_total_cost() < other.get_total_cost()

    def __le__(self, other):
        return self.get_total_cost() <= other.get_total_cost()

    def __gt__(self, other):
        return self.get_total_cost() > other.get_total_cost()

    def __ge__(self, other):
        return self.get_total_cost() >= other.get_total_cost()


if __name__ == '__main__':
    # Sample Airport and Flight objects for testing
    airport1 = Airport("Canada", "Toronto", "YYZ")
    airport2 = Airport("United States", "New York", "JFK")
    airport3 = Airport("United States", "Denver", "DEN")

    flight1 = Flight(airport2, airport3, "XUC-141", 5)
    flight2 = Flight(airport2, airport3, "QYR-830", 6)

    all_flights = {"XUC-141": flight1, "QYR-830": flight2}
    all_airports = {"JFK": airport2, "DEN": airport3, "YYZ": airport1}

    # Test cases for MaintenanceRecord
    try:
        m1 = MaintenanceRecord("XUC-141-JFK-20-15", all_flights, all_airports)
        m2 = MaintenanceRecord("QYR-830-LAX-50-1", all_flights, all_airports)
        m3 = MaintenanceRecord("XUC-141-JFK-20-50", all_flights, all_airports)

        print(m1)
        print(m2)

        print(m1 == m2)  # False
        print(m1 == m3)  # False

        print(m1 != m2)  # True

        print(m1.get_total_cost())  # 300.0
        print(m1.get_duration())  # 20

        #test lt, le, gt, ge
        print(m1 < m2) #false
        print(m1 <= m3) #true
        print(m2 > m3) #true
        print(m2 >= m1) #true

    except ValueError as e:
        print(f"ValueError: {e}")

    try:
        m4 = MaintenanceRecord("Invalid-Data", all_flights, all_airports)
    except ValueError as e:
        print(f"ValueError: {e}")

    try:
        m5 = MaintenanceRecord("XUC-141-AAA-20-15", all_flights, all_airports)
    except ValueError as e:
        print(f"ValueError: {e}")
