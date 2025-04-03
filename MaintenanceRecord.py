"""
******************************
CS 1026 - Assignment 4  – Air Travel
Code by: Sydney Koziel
Student ID: skoziel
File created: March 26, 2025
******************************
This file defines the MaintenanceRecord class.
Each MaintenanceRecord object represents a maintenance task for a specific
flight at a specific airport, including duration and cost per hour.
It parses maintenance data from a string, finds associated Flight and
Airport objects, calculates total cost, and supports comparison based
on total cost. It imports Flight and Airport classes.
"""
from Flight import Flight
from Airport import Airport
import re # Import regex for parsing

class MaintenanceRecord:
    """Represents a maintenance record for a flight."""

    # Regex to capture: FlightNum (AAA-111), AirportCode (AAA), Duration (float), Cost (float)
    # Allows variable whitespace (\s*) around hyphens
    MAINT_LINE_RE = re.compile(r'^\s*([A-Za-z]{3}-\d{3})\s*-\s*([A-Za-z]{3})\s*-\s*([\d.]+)\s*-\s*([\d.]+)\s*$')

    def __init__(self, input_line, all_flights, all_airports):
        """
        Initializes a MaintenanceRecord object by parsing a line of text using regex.

        Args:
            input_line (str): A string containing maintenance data.
            all_flights (dict): A dictionary of all flights {origin_code: [Flight,...]}.
            all_airports (dict or list): Container holding all Airport objects.

        Raises:
            ValueError: If input_line format is invalid, or flight/airport not found.
        """
        match = self.MAINT_LINE_RE.match(input_line.strip())
        if not match:
            raise ValueError(f"Invalid data string format: '{input_line}'")

        # Extract parts from regex match groups
        flight_number_str = match.group(1)
        maintenance_airport_code = match.group(2)
        duration_str = match.group(3)
        cost_per_hour_str = match.group(4)

        # Validate and convert duration and cost (already checked as numbers by regex)
        try:
            self._maintenance_duration = float(duration_str)
            self._maintenance_cost_per_hour = float(cost_per_hour_str)
            if self._maintenance_duration < 0 or self._maintenance_cost_per_hour < 0:
                 raise ValueError("Duration and cost cannot be negative.")
        except ValueError:
             # Should be unlikely if regex matches, but good safety check
             raise ValueError("Invalid data string: Duration or cost per hour is not a valid number.")

        # Find the flight object (Corrected logic from previous version)
        found_flight = None
        for origin_code in all_flights:
            for flight in all_flights[origin_code]:
                if flight.get_number() == flight_number_str:
                    found_flight = flight
                    break
            if found_flight:
                break

        if not found_flight:
            raise ValueError(f"Flight not found: {flight_number_str}")
        self._flight = found_flight

        # Find the maintenance airport object
        found_airport = None
        if isinstance(all_airports, dict):
            found_airport = all_airports.get(maintenance_airport_code)
        elif isinstance(all_airports, list):
            for airport in all_airports:
                if airport.get_code() == maintenance_airport_code:
                    found_airport = airport
                    break
        else:
             raise TypeError("all_airports must be a dictionary or a list")

        if not found_airport:
            raise ValueError(f"Airport not found: {maintenance_airport_code}")
        self._maintenance_airport = found_airport

    def get_total_cost(self):
        """Calculates and returns the total maintenance cost."""
        return self._maintenance_cost_per_hour * self._maintenance_duration

    def get_duration(self):
        """Returns the maintenance duration."""
        return self._maintenance_duration

    def get_flight(self):
        """Returns the Flight object associated with this record."""
        return self._flight

    def get_maintenance_airport(self):
        """Returns the Airport object where maintenance occurs."""
        return self._maintenance_airport

    def get_cost_per_hour(self):
        """Returns the cost per hour for maintenance."""
        return self._maintenance_cost_per_hour

    def __str__(self):
        """Returns the string representation of the MaintenanceRecord."""
        flight_str = str(self._flight)
        origin_airport = self._flight.get_origin()
        origin_airport_str = f"{origin_airport.get_code()} [{origin_airport.get_city()}, {origin_airport.get_country()}]"
        maint_airport_str = f"{self._maintenance_airport.get_code()} [{self._maintenance_airport.get_city()}, {self._maintenance_airport.get_country()}]"
        total_cost = self.get_total_cost()

        return (
            f"{self._flight.get_number()} ({flight_str}) from {origin_airport_str} "
            f"to be maintained at {maint_airport_str} for {self._maintenance_duration} hours "
            f"@ ${self._maintenance_cost_per_hour:.1f}/hour (${total_cost:.1f})"
        )

    def __eq__(self, other):
        """Checks if two MaintenanceRecord objects are equal."""
        if not isinstance(other, MaintenanceRecord):
            return False
        return (
            self._flight == other._flight
            and self._maintenance_airport == other._maintenance_airport
            and self._maintenance_duration == other._maintenance_duration
            and self._maintenance_cost_per_hour == other._maintenance_cost_per_hour
        )

    def __ne__(self, other):
        """Checks if two MaintenanceRecord objects are not equal."""
        return not self.__eq__(other)

    def __lt__(self, other):
        """Compares two MaintenanceRecords based on total cost (less than)."""
        if not isinstance(other, MaintenanceRecord):
            return NotImplemented
        return self.get_total_cost() < other.get_total_cost()

    def __le__(self, other):
        """Compares two MaintenanceRecords based on total cost (less than or equal)."""
        if not isinstance(other, MaintenanceRecord):
            return NotImplemented
        return self.get_total_cost() <= other.get_total_cost()

    def __gt__(self, other):
        """Compares two MaintenanceRecords based on total cost (greater than)."""
        if not isinstance(other, MaintenanceRecord):
            return NotImplemented
        return self.get_total_cost() > other.get_total_cost()

    def __ge__(self, other):
        """Compares two MaintenanceRecords based on total cost (greater than or equal)."""
        if not isinstance(other, MaintenanceRecord):
            return NotImplemented
        return self.get_total_cost() >= other.get_total_cost()

# Keep the __main__ block for testing if desired
if __name__ == '__main__':
    # Sample Airport and Flight objects for testing
    print("\n--- MaintenanceRecord Class Tests ---")
    airport_jfk = Airport("United States", "New York", "JFK")
    airport_den = Airport("United States", "Denver", "DEN")
    airport_lax = Airport("United States", "Los Angeles", "LAX")
    airport_atl = Airport("United States", "Atlanta", "ATL")
    airport_mex = Airport("Mexico", "Mexico City", "MEX")
    airport_mia = Airport("United States", "Miami", "MIA") # Add MIA for test case
    airport_yeg = Airport("Canada", "Edmonton", "YEG") # Add YEG for test case

    # Note: all_flights structure matches Assign4.py (keyed by origin)
    all_flights_test = {
        "JFK": [
            Flight(airport_jfk, airport_den, "XUC-141", 5.0),
            Flight(airport_jfk, airport_mex, "QYR-830", 6.0)
        ],
        "ORD": [ # Need flight MQC-437 for maintenance test
            Flight(Airport("United States", "Chicago", "ORD"), Airport("United States", "Philadelphia", "PHL"), "MQC-437", 2.0)
        ],
        "DFW": [ # Need flight NGF-735 for maintenance test
             Flight(Airport("United States", "Dallas", "DFW"), airport_jfk, "NGF-735", 4.25)
        ]

        # Add other necessary flights for maintenance.txt examples if needed
    }
    all_airports_test = {
        "JFK": airport_jfk, "DEN": airport_den, "LAX": airport_lax,
        "MEX": airport_mex, "ATL": airport_atl, "YYZ": Airport("Canada","Toronto","YYZ"),
        "MIA": airport_mia, "YEG": airport_yeg,
        "ORD": all_flights_test["ORD"][0].get_origin(), # Get ORD object
        "PHL": all_flights_test["ORD"][0].get_destination(), # Get PHL object
        "DFW": all_flights_test["DFW"][0].get_origin(), # Get DFW object
        }

    # Test valid record creation using lines from maintenance.txt
    valid_lines = [
         "MQC-437 -MIA-50-12",
         "NGF-735- YEG-65-10",
         "   XUC-141-ATL-20 -15  ",
         "QYR-830 -LAX-50-1",
         "EWQ-950-LAX-300-12" # Assuming EWQ-950 exists
    ]
    # Add EWQ-950 to test data if needed
    if "ORD" not in all_flights_test: all_flights_test["ORD"] = []
    if not any(f.get_number() == "EWQ-950" for f in all_flights_test["ORD"]):
         all_flights_test["ORD"].append(Flight(all_airports_test["ORD"], all_airports_test["YYZ"], "EWQ-950", 2.75))

    print("\nTesting Valid Record Creation with Regex:")
    records = []
    for line in valid_lines:
         try:
             print(f"Processing line: '{line}'")
             record = MaintenanceRecord(line, all_flights_test, all_airports_test)
             records.append(record)
             print(f"  Success: {record}")
             print(f"  Cost: {record.get_total_cost()}")
         except ValueError as e:
             print(f"  *** Error creating record: {e}") # Should not happen for these if flights/airports exist


    # Test invalid data remains invalid
    invalid_lines_re = [
        "Invalid-Data",                 # Bad format
        "ABC-123-XYZ-10-10",            # Invalid flight num format
        "XYZ-999-LAX-10-10",            # Valid flight num format, but flight likely not found
        "QYR-830-XXX-10-10",            # Airport not found
        "QYR-830-LAX-ABC-10",           # Duration not a number
        "QYR-830-LAX-10-XYZ",           # Cost not a number
        "QYR-830-LAX-10",               # Wrong number of parts (regex won't match)
    ]
    print("\nTesting Invalid Record Creation with Regex:")
    for line in invalid_lines_re:
        try:
            print(f"Processing invalid line: '{line}'")
            MaintenanceRecord(line, all_flights_test, all_airports_test)
            print("  *** Unexpected Success (Should have failed)")
        except ValueError as e:
            print(f"  Caught expected error: {e}")

    print("-" * 25)