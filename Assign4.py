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
# from Airport import *
# from MaintenanceRecord import *
#
# all_airports = {}  # Dictionary to store airports
# all_flights = []   # List to store flight data
#
# def load_flight_files(airports_filename, flights_filename):
#     global all_airports, all_flights  # Ensure global variables are updated
#
#     # Clear previous data in case function is called multiple times
#     all_airports.clear()
#     all_flights.clear()
#
#     # Read airports file
#     with open(airports_filename, "r", encoding="utf-8") as file:
#         for line in file:
#             line = line.strip()
#             if line:
#                 parts = line.split("-")
#                 if len(parts) == 3:
#                     code, country, city = parts
#                     all_airports[code.strip()] = (country.strip(), city.strip())
#
#     # Read flights file
#     with open(flights_filename, "r", encoding="utf-8") as file:
#         for line in file:
#             line = line.strip()
#             if line:
#                 parts = line.split("-")
#                 if len(parts) == 5:
#                     flight_code, num, src, dest, duration = parts
#                     all_flights.append((flight_code.strip(), num.strip(), src.strip(), dest.strip(), float(duration.strip())))
#
#
# def get_airport_using_code(code):
#     with open("airports_test.txt", "r") as f:
#         airports = {}
#         for line in f:
#             parts = line.strip().split("-")
#             if len(parts) < 3:
#                 continue
#             airport_code = parts[0].strip()
#             country = parts[1].strip()
#             city = parts[2].strip()
#             airports[airport_code] = (country, city)
#
#     print("Stored keys:", list(airports.keys()))  # Debugging line
#
#     if code.strip() not in airports:
#         raise ValueError(f"No airport with the given code: {code}")
#
#     return airports[code.strip()]
#
#
# def find_all_flights_city(city):
#     return [flight for flight in all_flights if
#             flight.get_origin().get_city() == city or flight.get_destination().get_city() == city]
#
# def find_all_flights_country(country):
#     return [flight for flight in all_flights if
#             flight.get_origin().get_country().strip() == country or
#             flight.get_destination().get_country().strip() == country]
#
#
# def has_flight_between(orig_airport, dest_airport):
#     return any(flight.dest_code == dest_airport.code for flight in all_flights.get(orig_airport.code, []))
#
#
# def shortest_flight_from(orig_airport):
#     if orig_airport.code in all_flights:
#         return min(all_flights[orig_airport.code], key=lambda f: f.duration, default=None)
#     return None
#
#
# def find_return_flight(first_flight):
#     dest_code = first_flight.dest_code
#     orig_code = first_flight.origin_code
#     for flight in all_flights.get(dest_code, []):
#         if flight.dest_code == orig_code:
#             return flight
#     raise ValueError(f"There is no flight from {dest_code} to {orig_code}")
#
#
# def create_maintenance_records(maintenance_file, flights_dict, airports_dict):
#     global maintenance_records
#     maintenance_records = []
#     try:
#         with open(maintenance_file, 'r') as mf:
#             for line in mf:
#                 line = line.strip()
#                 if line:
#                     record = MaintenanceRecord(line, flights_dict, airports_dict)
#                     if record not in maintenance_records:
#                         maintenance_records.append(record)
#         return True
#     except ValueError:
#         return False
#
#
# def find_total_cost(records):
#     return sum(record.get_total_cost() for record in records)
#
#
# def find_total_duration(records):
#     return sum(record.get_duration() for record in records)
#
#
# def sort_maintenance_records(records):
#     return sorted(records)

from Flight import *
from Airport import *
from MaintenanceRecord import *


# Global containers to store data
all_airports = {}  # or [] or set(), any suitable container
all_flights = {}  # MUST be a dictionary
maintenance_records = []  # MUST be a list


def load_flight_files(airport_file, flight_file):
    try:
        # Load airports
        with open(airport_file, 'r') as file:
            for line in file:
                parts = [part.strip() for part in line.strip().split('-')]
                if len(parts) == 3:
                    code, country, city = parts
                    all_airports[code] = Airport(country, city, code)  # Using code as key
                else:
                    return False  # Invalid airport data

        # Load flights
        with open(flight_file, 'r') as file:
            for line in file:
                parts = [part.strip() for part in line.strip().split('-')]
                if len(parts) == 4:
                    flight_number, origin_code, dest_code, duration_str = parts
                    try:
                        duration = float(duration_str)
                        origin = all_airports.get(origin_code)
                        destination = all_airports.get(dest_code)
                        if origin and destination:
                            flight = Flight(origin, destination, flight_number, duration)
                            if origin_code not in all_flights:
                                all_flights[origin_code] = []
                            all_flights[origin_code].append(flight)
                        else:
                            return False  # Invalid flight data (airport not found)
                    except ValueError:
                        return False  # Invalid duration format
                else:
                    return False  # Invalid flight data format

        return True

    except FileNotFoundError:
        return False
    except Exception:
        return False


def get_airport_using_code(code):
    airport = all_airports.get(code)
    if not airport:
        raise ValueError(f"No airport with the given code: {code}")
    return airport


def find_all_flights_city(city):
    result = []
    for flight_list in all_flights.values():
        for flight in flight_list:
            if flight.get_origin().get_city() == city or flight.get_destination().get_city() == city:
                result.append(flight)
    return result


def find_all_flights_country(country):
    result = []
    for flight_list in all_flights.values():
        for flight in flight_list:
            if flight.get_origin().get_country() == country or flight.get_destination().get_country() == country:
                result.append(flight)
    return result


def has_flight_between(orig_airport, dest_airport):
    if orig_airport.get_code() in all_flights:
        for flight in all_flights[orig_airport.get_code()]:
            if flight.get_destination() == dest_airport:
                return True
    return False


def shortest_flight_from(orig_airport):
    if orig_airport.get_code() in all_flights:
        shortest = all_flights[orig_airport.get_code()][0]
        for flight in all_flights[orig_airport.get_code()]:
            if flight.get_duration() < shortest.get_duration():
                shortest = flight
        return shortest
    return None


def find_return_flight(first_flight):
    dest_code = first_flight.get_destination().get_code()
    orig_code = first_flight.get_origin().get_code()

    if dest_code in all_flights:
        for flight in all_flights[dest_code]:
            if flight.get_destination().get_code() == orig_code:
                return flight
    raise ValueError(f"There is no flight from {dest_code} to {orig_code}")


def create_maintenance_records(maintenance_file, flights_dict, airports_list):
    try:
        with open(maintenance_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line:  # Skip empty lines
                    try:
                        record = MaintenanceRecord(line, flights_dict, airports_list)
                        if record not in maintenance_records:
                            maintenance_records.append(record)
                    except ValueError:
                        return False
        return True
    except FileNotFoundError:
        return False


def find_total_cost(records):


    total_cost = 0
    for record in records:
        total_cost += record.get_total_cost()
    return total_cost


def find_total_duration(records):
    total_duration = 0
    for record in records:
        total_duration += record.get_duration()
    return total_duration


def sort_maintenance_records(records):
    return sorted(records, key=lambda x: x.get_total_cost())


if __name__ == '__main__':
    # Test cases (as provided in the assignment)
    # These should work if the other classes are implemented correctly
    # and you have the data files (airports.txt, flights.txt, maintenance.txt)

    data = load_flight_files("airports.txt", "flights.txt")
    print(data, len(all_airports), len(all_flights))

    print(get_airport_using_code("ORD"))

    try:
        print(get_airport_using_code("ABC"))
    except ValueError as e:
        print(e)

    res = find_all_flights_city("Dallas")
    for r in res:
        print(r)

    res = find_all_flights_country("China")
    for r in res:
        print(r)

    pearson = get_airport_using_code("YYZ")
    ohare = get_airport_using_code("ORD")
    edm = get_airport_using_code("YEG")
    print(has_flight_between(edm, ohare))
    print(has_flight_between(edm, pearson))

    jfk = get_airport_using_code("JFK")
    print(shortest_flight_from(jfk))

    sf_to_sp = all_flights["SFO"][0]
    print(find_return_flight(sf_to_sp))

    f1 = all_flights["YEG"][0]
    f2 = all_flights["ORD"][0]
    print(f1 + f2)
    try:
        print(f2 + f1)
    except ValueError as e:
        print(e)

    # Create a dummy maintenance.txt for testing
    with open("maintenance.txt", "w") as f:
        f.write("QYR-830-LAX-50-1\n")
        f.write("XUC-141-ATL-20-15\n")
        f.write("QYR-830-LAX-50-1\n")
        f.write("XUC-141-ATL-20-1\n")
        f.write("XUC-141-ATL-20-15\n")

    create_maintenance_records("maintenance.txt", all_flights, all_airports)
    print(len(maintenance_records))
    print(maintenance_records[0])
    print(maintenance_records[1])

    m1 = MaintenanceRecord("YOI-104-ATL-1-2", all_flights, all_airports)
    m2 = MaintenanceRecord("RTK-498-ATL-15-5", all_flights, all_airports)
    m3 = MaintenanceRecord("ADJ-602-ATL-100-10", all_flights, all_airports)
    print(find_total_cost([m1, m2, m3]))
    print(find_total_duration([m1, m2, m3]))

    recs = [m1, m2, m3]
    print(recs[0].get_total_cost(), recs[1].get_total_cost(), recs[2].get_total_cost())
    sorted_recs = sort_maintenance_records(recs)
    print(sorted_recs[0].get_total_cost(), sorted_recs[1].get_total_cost(), sorted_recs[2].get_total_cost())

    # # These examples are from the assignment document.
    # # Note that you will need to implement the required classes, methods, and functions before these tests will work.
    # # Remove the pass keyword above and uncomment these when you are ready to test.
    #
    # print("Example 1: load_files(airport_file, flight_file)")
    # data = load_flight_files("airports.txt", "flights.txt")
    # print(data, len(all_airports), len(all_flights))
    #
    # print("\nExample 2: get_airport_by_code(code)")
    # print(get_airport_using_code("ORD"))
    # # print(get_airport_using_code("ABC"))  # Should cause an Exception
    #
    # print("\nExample 3: find_all_flights_city(city)")
    # res = find_all_flights_city("Dallas")
    # for r in res:
    #     print(r)
    #
    # print("\nExample 4: find_all_flights_country(country)")
    # res = find_all_flights_country("China")
    # for r in res:
    #     print(r)
    #
    # print("\nExample 5: find_flight_between(orig_airport, dest_airport)")
    # pearson = get_airport_using_code("YYZ")
    # ohare = get_airport_using_code("ORD")
    # edm = get_airport_using_code("YEG")
    # print(has_flight_between(edm, ohare))
    # print(has_flight_between(edm, pearson))
    # print(has_flight_between(pearson, ohare))
    #
    # print("\nExample 6: shortest_flight_from(orig_airport)")
    # jfk = get_airport_using_code("JFK")
    # print(shortest_flight_from(jfk))
    #
    # print("\nExample 7: find_return_flight(flight)")
    # sf_to_sp = all_flights["SFO"][0]
    # print(find_return_flight(sf_to_sp))
    #
    # print("\nExample 8: __add__(self, conn_flight) [in Flight.py]")
    # f1 = all_flights["YEG"][0]
    # f2 = all_flights["ORD"][0]
    # print(f1 + f2)
    # # print(f2 + f1)  # Should cause an Exception
    #
    # print("\nExample 9: create_maintenance_records(“file.txt”, all_flights, all_airports)")
    # create_maintenance_records("file.txt", all_flights, all_airports)
    # print(len(maintenance_records))
    # print(maintenance_records[0])
    # print(maintenance_records[1])
    #
    # print("\nExample 10: find_total_cost(records)")
    # m1 = MaintenanceRecord("YOI-104-ATL-1-2", all_flights, all_airports)
    # m2 = MaintenanceRecord("RTK-498-ATL-15-5", all_flights, all_airports)
    # m3 = MaintenanceRecord("ADJ-602-ATL-100-10", all_flights, all_airports)
    # print(find_total_cost([m1, m2, m3]))
    #
    # print("\nExample 12: find_total_duration(records)")
    # print(find_total_duration([m1, m2, m3]))
    #
    # print("\nExample 13: sort_maintenance_records(records)")
    # recs = [m3, m2, m1]
    # print(recs[0].get_total_cost(),
    #       recs[1].get_total_cost(),
    #       recs[2].get_total_cost())
    # sorted_recs = sort_maintenance_records(recs)
    # print(sorted_recs[0].get_total_cost(),
    #       sorted_recs[1].get_total_cost(),
    #       sorted_recs[2].get_total_cost())