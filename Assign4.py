"""
******************************
CS 1026 - Assignment 4  – Air Travel
Code by: Sydney Koziel
Student ID: skoziel
File created: March 26, 2025
******************************
This file serves as the main program script for Assignment 4.
It loads airport and flight data from specified files into
Airport and Flight objects, storing them in global containers.
It defines functions to query this data (e.g., find flights by city/country,
find shortest flights, check connectivity, find return flights).
It also loads maintenance records from a file, calculating total costs
and durations, and sorting records. Imports Airport, Flight, and
MaintenanceRecord classes.
"""
from Flight import *
from Airport import *
from MaintenanceRecord import *
import re # Import regex for parsing
import os # Import os for file checks

# Global containers to store data
all_airports = {}
all_flights = {}
maintenance_records = []

# --- Regular Expressions for Parsing ---
# Airport: Code (AAA), Country (any chars not '-'), City (any chars not '-')
# Allows variable space around hyphens and within Country/City
AIRPORT_LINE_RE = re.compile(r'^\s*([A-Za-z]{3})\s*-\s*([^-]+?)\s*-\s*([^-]+?)\s*$')

# Flight: FlightNum (AAA-111), Origin (AAA), Dest (AAA), Duration (float)
# Allows variable space around hyphens
FLIGHT_LINE_RE = re.compile(r'^\s*([A-Za-z]{3}-\d{3})\s*-\s*([A-Za-z]{3})\s*-\s*([A-Za-z]{3})\s*-\s*([\d.]+)\s*$')
# --- End Regular Expressions ---


def load_flight_files(airport_file, flight_file):
    """
    Loads airport and flight data from files into global containers using regex parsing.

    Args:
        airport_file (str): The name of the airport data file.
        flight_file (str): The name of the flight data file.

    Returns:
        bool: True if both files are loaded successfully (or with warnings), False on fatal error.
    """
    global all_airports, all_flights
    all_airports.clear()
    all_flights.clear()
    success = True # Assume success unless fatal error

    try:
        # Load airports using Regex
        print(f"Loading airports from: {airport_file}")
        with open(airport_file, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                line_content = line.strip()
                if not line_content: continue

                match = AIRPORT_LINE_RE.match(line_content)
                if match:
                    code, country, city = match.groups() # Extract matched groups
                    # Further strip just in case regex captures trailing space in names
                    country = country.strip()
                    city = city.strip()
                    if not code or not country or not city:
                         print(f"Warning (Line {i+1}): Skipping airport line with empty parts after parsing: {line_content}")
                         continue
                    all_airports[code] = Airport(country, city, code)
                    # print(f"  Loaded Airport: {code} - {city}, {country}") # Debug print
                else:
                    print(f"Warning (Line {i+1}): Skipping invalid airport line format: {line_content}")
                    # Continue processing other lines

        # Load flights using Regex
        print(f"\nLoading flights from: {flight_file}")
        with open(flight_file, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                line_content = line.strip()
                if not line_content: continue

                match = FLIGHT_LINE_RE.match(line_content)
                if match:
                    flight_number, origin_code, dest_code, duration_str = match.groups()

                    origin = all_airports.get(origin_code)
                    destination = all_airports.get(dest_code)

                    if not origin:
                        print(f"Warning (Line {i+1}): Skipping flight '{flight_number}' - Origin airport '{origin_code}' not found.")
                        continue
                    if not destination:
                        print(f"Warning (Line {i+1}): Skipping flight '{flight_number}' - Destination airport '{dest_code}' not found.")
                        continue

                    try:
                        duration = float(duration_str)
                        if duration < 0:
                             print(f"Warning (Line {i+1}): Skipping flight '{flight_number}' - Invalid negative duration '{duration_str}'.")
                             continue
                    except ValueError:
                        print(f"Warning (Line {i+1}): Skipping flight '{flight_number}' - Invalid duration format '{duration_str}'.")
                        continue

                    try:
                        flight = Flight(origin, destination, flight_number, duration)
                        if origin_code not in all_flights:
                            all_flights[origin_code] = []
                        all_flights[origin_code].append(flight)
                        # print(f"  Loaded Flight: {flight_number} from {origin_code} to {dest_code}") # Debug print
                    except TypeError as e:
                         print(f"Error creating Flight object for line {i+1} '{line_content}': {e}")
                         # Continue processing

                else:
                    # This regex is quite specific, failure might indicate a real format issue
                    print(f"Warning (Line {i+1}): Skipping invalid flight line format: {line_content}")
                    # Continue processing

        return success # Return True even if warnings occurred

    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during file loading: {e}")
        return False

# --- Functions below remain the same as the previous corrected version ---
# (get_airport_using_code, find_all_flights_city, find_all_flights_country,
#  has_flight_between, shortest_flight_from, find_return_flight,
#  create_maintenance_records, find_total_cost, find_total_duration,
#  sort_maintenance_records)

def get_airport_using_code(code):
    """
    Retrieves an Airport object from the global all_airports dictionary.

    Args:
        code (str): The 3-letter airport code.

    Returns:
        Airport: The Airport object corresponding to the code.

    Raises:
        ValueError: If no airport with the given code is found.
    """
    airport = all_airports.get(code.strip())
    if not airport:
        raise ValueError(f"No airport with the given code: {code}")
    return airport

def find_all_flights_city(city):
    """
    Finds all flights involving a specific city (as origin or destination).

    Args:
        city (str): The name of the city.

    Returns:
        list: A list of Flight objects involving the city. Empty if none found.
    """
    result_flights = []
    target_city = city.strip()
    for flight_list in all_flights.values():
        for flight in flight_list:
            if flight.get_origin().get_city() == target_city or flight.get_destination().get_city() == target_city:
                result_flights.append(flight)
    return result_flights

def find_all_flights_country(country):
    """
    Finds all flights involving a specific country (as origin or destination).

    Args:
        country (str): The name of the country.

    Returns:
        list: A list of Flight objects involving the country. Empty if none found.
    """
    result_flights = []
    target_country = country.strip()
    for flight_list in all_flights.values():
        for flight in flight_list:
            if flight.get_origin().get_country() == target_country or flight.get_destination().get_country() == target_country:
                result_flights.append(flight)
    return result_flights

def has_flight_between(orig_airport, dest_airport):
    """
    Checks if there is a direct flight between two specific airports.

    Args:
        orig_airport (Airport): The origin Airport object.
        dest_airport (Airport): The destination Airport object.

    Returns:
        bool: True if a direct flight exists, False otherwise.
    """
    if not isinstance(orig_airport, Airport) or not isinstance(dest_airport, Airport):
        print("Error: has_flight_between requires Airport objects as input.")
        return False

    origin_code = orig_airport.get_code()
    if origin_code in all_flights:
        for flight in all_flights[origin_code]:
            if flight.get_destination() == dest_airport:
                return True
    return False

def shortest_flight_from(orig_airport):
    """
    Finds the shortest flight (by duration) departing from a specific airport.

    Args:
        orig_airport (Airport): The origin Airport object.

    Returns:
        Flight or None: The Flight object with the shortest duration, or None if no flights depart from the origin.
    """
    if not isinstance(orig_airport, Airport):
        print("Error: shortest_flight_from requires an Airport object as input.")
        return None

    origin_code = orig_airport.get_code()
    if origin_code in all_flights and all_flights[origin_code]:
        shortest = min(all_flights[origin_code], key=lambda flight: flight.get_duration())
        return shortest
    else:
        return None

def find_return_flight(first_flight):
    """
    Finds the first available return flight for a given flight.

    Args:
        first_flight (Flight): The initial Flight object.

    Returns:
        Flight: The return Flight object (flying Dest -> Orig).

    Raises:
        ValueError: If no return flight is found.
        TypeError: If input is not a Flight object.
    """
    if not isinstance(first_flight, Flight):
        raise TypeError("Input must be a Flight object.")

    original_destination = first_flight.get_destination()
    original_origin = first_flight.get_origin()
    return_origin_code = original_destination.get_code()

    if return_origin_code in all_flights:
        for return_flight in all_flights[return_origin_code]:
            if return_flight.get_destination() == original_origin:
                return return_flight

    raise ValueError(f"There is no flight from {original_destination.get_code()} to {original_origin.get_code()}")

def create_maintenance_records(maintenance_file, flights_dict, airports_dict):
    """
    Reads a maintenance file, creates unique MaintenanceRecord objects,
    and adds them to the global maintenance_records list. Uses updated MaintenanceRecord parsing.

    Args:
        maintenance_file (str): The name of the maintenance data file.
        flights_dict (dict): The global dictionary of all flights.
        airports_dict (dict): The global dictionary of all airports.

    Returns:
        bool: True if file processed without fatal errors (individual line errors are warnings).
              False only on fatal errors like file not found or unexpected exceptions.
              *Correction:* Assignment spec implies return False if *any* record construction fails.
    """
    global maintenance_records
    # maintenance_records.clear() # Uncomment if list should be cleared on each call

    try:
        with open(maintenance_file, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                line_content = line.strip()
                if not line_content:
                    continue

                try:
                    # MaintenanceRecord init now uses robust regex parsing
                    record = MaintenanceRecord(line_content, flights_dict, airports_dict)
                    if record not in maintenance_records:
                        maintenance_records.append(record)
                except ValueError as e:
                    # If MaintenanceRecord.__init__ raises ValueError, per spec, return False
                    print(f"Error (Line {i+1}): Failed to create maintenance record from '{line_content}': {e}")
                    return False # Exit immediately on first failed record creation

        # If loop completes without returning False, all valid lines were processed ok
        return True

    except FileNotFoundError:
        print(f"Error: Maintenance file '{maintenance_file}' not found.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred processing maintenance file: {e}")
        return False


def find_total_cost(records):
    """
    Calculates the total maintenance cost for a given list of records.

    Args:
        records (list): A list of MaintenanceRecord objects.

    Returns:
        float: The sum of total costs for all records in the list.
    """
    total_cost = 0.0
    for record in records:
        if isinstance(record, MaintenanceRecord):
            total_cost += record.get_total_cost()
        else:
            print("Warning: Item in list is not a MaintenanceRecord.")
    return total_cost

def find_total_duration(records):
    """
    Calculates the total maintenance duration for a given list of records.

    Args:
        records (list): A list of MaintenanceRecord objects.

    Returns:
        float: The sum of durations for all records in the list.
    """
    total_duration = 0.0
    for record in records:
         if isinstance(record, MaintenanceRecord):
            total_duration += record.get_duration()
         else:
             print("Warning: Item in list is not a MaintenanceRecord.")
    return total_duration

def sort_maintenance_records(records):
    """
    Sorts a list of MaintenanceRecord objects by total cost (ascending).

    Args:
        records (list): A list of MaintenanceRecord objects.

    Returns:
        list: A *new* sorted list of MaintenanceRecord objects.
    """
    # Ensure all items are MaintenanceRecords before sorting
    valid_records = [r for r in records if isinstance(r, MaintenanceRecord)]
    if len(valid_records) != len(records):
         print("Warning: Sorting a list containing non-MaintenanceRecord items.")
    # Sort using the implemented comparison methods
    return sorted(valid_records)

# --- Main execution block ---
if __name__ == '__main__':
    print("--- Assign4 Script Start (Regex Parsing) ---")

    # Use the actual filenames provided by the user
    airport_filename = "airports.txt"
    flight_filename = "flights.txt"
    maintenance_filename = "maintenance.txt"

    # Check if files exist before trying to load
    if not os.path.exists(airport_filename):
        print(f"Error: Airport file '{airport_filename}' not found.")
    elif not os.path.exists(flight_filename):
         print(f"Error: Flight file '{flight_filename}' not found.")
    else:
        # Example 1: load_flight_files
        print("\n--- Example 1: load_flight_files ---")
        load_success = load_flight_files(airport_filename, flight_filename)
        print(f"\nFiles loaded successfully reported: {load_success}")
        print(f"Number of airports loaded: {len(all_airports)}")
        print(f"Number of origin airports with flights: {len(all_flights)}")
        total_flights_loaded = sum(len(v) for v in all_flights.values())
        print(f"Total number of flights loaded: {total_flights_loaded}") # Should be non-zero now

        # Check if required airports for later tests were loaded
        required_airports = ["ORD", "ABC", "YEG", "YYZ", "JFK", "SFO", "ATL"]
        for code in required_airports:
             if code not in all_airports and code != "ABC": # ABC is expected not to exist
                 print(f"Warning: Required airport {code} not loaded.")

        # Example 2: get_airport_using_code
        print("\n--- Example 2: get_airport_using_code ---")
        try:
            ord_airport = get_airport_using_code("ORD")
            print(f"Found ORD: {ord_airport}")
            abc_airport = get_airport_using_code("ABC")
            print(f"Found ABC: {abc_airport}")
        except ValueError as e:
            print(f"Caught expected error: {e}")

        # Example 3: find_all_flights_city
        print("\n--- Example 3: find_all_flights_city ---")
        dallas_flights = find_all_flights_city("Dallas")
        print("Flights involving Dallas:")
        if dallas_flights:
            for flight in dallas_flights: print(f"  {flight}")
        else: print("  None found.")

        # Example 4: find_all_flights_country
        print("\n--- Example 4: find_all_flights_country ---")
        china_flights = find_all_flights_country("China")
        print("Flights involving China:")
        if china_flights:
            for flight in china_flights: print(f"  {flight}")
        else: print("  None found.")

        # Example 5: has_flight_between
        print("\n--- Example 5: has_flight_between ---")
        try:
            edm_airport = get_airport_using_code("YEG")
            pearson_airport = get_airport_using_code("YYZ")
            ohare_airport = get_airport_using_code("ORD")
            print(f"Flight from Edmonton (YEG) to Chicago (ORD)? {has_flight_between(edm_airport, ohare_airport)}")
            print(f"Flight from Edmonton (YEG) to Toronto (YYZ)? {has_flight_between(edm_airport, pearson_airport)}")
            print(f"Flight from Toronto (YYZ) to Chicago (ORD)? {has_flight_between(pearson_airport, ohare_airport)}")
        except ValueError as e: print(f"Error during has_flight_between setup: {e}")

        # Example 6: shortest_flight_from
        print("\n--- Example 6: shortest_flight_from ---")
        try:
            jfk_airport = get_airport_using_code("JFK")
            shortest = shortest_flight_from(jfk_airport)
            print(f"Shortest flight from JFK: {shortest}") # Should find one now
        except ValueError as e: print(f"Error during shortest_flight_from setup: {e}")

        # Example 7: find_return_flight
        print("\n--- Example 7: find_return_flight ---")
        try:
            # Need SFO->GRU flight (EKR-896) and GRU->SFO (BBH-704)
            if "SFO" in all_flights and all_flights["SFO"]:
                 # Find the specific flight if multiple exist from SFO
                 sfo_gru_flight = next((f for f in all_flights["SFO"] if f.get_number() == "EKR-896"), None)
                 if sfo_gru_flight:
                      print(f"Finding return for: {sfo_gru_flight}")
                      return_f = find_return_flight(sfo_gru_flight)
                      print(f"Found return flight: {return_f}")
                 else: print("Flight EKR-896 from SFO not found.")
            else: print("SFO flights not loaded, skipping test.")

            # Test non-existent return
            if "YEG" in all_flights and all_flights["YEG"]:
                 yeg_ord_flight = next((f for f in all_flights["YEG"] if f.get_number() == "XPA-230"), None)
                 if yeg_ord_flight:
                      print(f"Finding return for: {yeg_ord_flight} (expect failure)")
                      try:
                           find_return_flight(yeg_ord_flight)
                      except ValueError as e: print(f"Caught expected error: {e}")
                 else: print("Flight XPA-230 from YEG not found.")
            else: print("YEG flights not loaded, skipping non-return test.")

        except (KeyError, IndexError, ValueError, TypeError) as e: print(f"Error during return flight test: {e}")

        # Example 8: __add__ (Flight combination)
        print("\n--- Example 8: __add__ (Flight combination) ---")
        try:
            # Need YEG->ORD (XPA-230) and ORD->JFK (OXD-016)
            f1 = next((f for f in all_flights.get("YEG",[]) if f.get_number() == "XPA-230"), None)
            f2 = next((f for f in all_flights.get("ORD",[]) if f.get_number() == "OXD-016"), None)
            if f1 and f2:
                combined = f1 + f2
                print(f"Combined {f1.get_number()} + {f2.get_number()}: {combined}")
                print("Testing invalid combination:")
                invalid_combined = f2 + f1 # Should fail
            else:
                 print("Required flights for combination test not found.")
        except (KeyError, IndexError, ValueError, TypeError) as e: print(f"Caught expected error: {e}")

        # Example 9: create_maintenance_records
        print("\n--- Example 9: create_maintenance_records ---")
        maintenance_records.clear() # Start fresh
        if not os.path.exists(maintenance_filename):
             print(f"Error: Maintenance file '{maintenance_filename}' not found.")
        else:
             maint_success = create_maintenance_records(maintenance_filename, all_flights, all_airports)
             print(f"create_maintenance_records reported success: {maint_success}") # Should be False if any line invalid
             print(f"Number of unique, valid maintenance records loaded: {len(maintenance_records)}")
             print("First few loaded records:")
             for i, rec in enumerate(maintenance_records[:3]): # Print first 3
                  print(f"  {i+1}: {rec}")

        # Example 10: find_total_cost
        print("\n--- Example 10: find_total_cost ---")
        # PDF uses YOI-104, RTK-498, ADJ-602 with ATL maint airport
        cost_test_records_pdf = []
        try:
             # Need flights YOI-104(PEK-MIA), RTK-498(YVR-LAX), ADJ-602(ORD-YHZ)
             rec1_pdf_str = "YOI-104-ATL-1-2"
             rec2_pdf_str = "RTK-498-ATL-15-5"
             rec3_pdf_str = "ADJ-602-ATL-100-10"
             # Need to ensure these flights exist in all_flights before creating records
             flights_found = True
             if not any(f.get_number() == "YOI-104" for flist in all_flights.values() for f in flist): flights_found=False; print("YOI-104 not found")
             if not any(f.get_number() == "RTK-498" for flist in all_flights.values() for f in flist): flights_found=False; print("RTK-498 not found")
             if not any(f.get_number() == "ADJ-602" for flist in all_flights.values() for f in flist): flights_found=False; print("ADJ-602 not found")

             if flights_found and "ATL" in all_airports:
                 cost_test_records_pdf.append(MaintenanceRecord(rec1_pdf_str, all_flights, all_airports)) # Cost 2.0
                 cost_test_records_pdf.append(MaintenanceRecord(rec2_pdf_str, all_flights, all_airports)) # Cost 75.0
                 cost_test_records_pdf.append(MaintenanceRecord(rec3_pdf_str, all_flights, all_airports)) # Cost 1000.0
                 total_c_pdf = find_total_cost(cost_test_records_pdf)
                 print(f"Total cost for PDF example records: ${total_c_pdf:.1f}") # Expect 1077.0
             else:
                 print("Could not create all records for PDF cost test due to missing flights/airport.")

        except ValueError as e: print(f"Error creating records for PDF cost test: {e}")

        # Example 11: find_total_duration
        print("\n--- Example 11: find_total_duration ---")
        if len(cost_test_records_pdf) == 3:
            total_d_pdf = find_total_duration(cost_test_records_pdf)
            print(f"Total duration for PDF example records: {total_d_pdf} hours") # Expect 1 + 15 + 100 = 116
        else: print("Skipping duration test as cost test records incomplete.")

        # Example 12: sort_maintenance_records
        print("\n--- Example 12: sort_maintenance_records ---")
        if len(cost_test_records_pdf) == 3:
            recs_to_sort_pdf = cost_test_records_pdf[:] # Copy
            print("Original order costs (PDF):", [r.get_total_cost() for r in recs_to_sort_pdf])
            sorted_recs_pdf = sort_maintenance_records(recs_to_sort_pdf)
            print("Sorted order costs (PDF):", [r.get_total_cost() for r in sorted_recs_pdf]) # Expect [2.0, 75.0, 1000.0]
        else: print("Skipping sort test as cost test records incomplete.")

    print("\n--- Assign4 Script End ---")