"""
******************************
CS 1026 - Assignment 4  – Air Travel
Code by: Sydney Koziel
Student ID: skoziel
File created: March 26, 2025
******************************
COMMENT
"""
# class Airport:
#     """Represents an airport with a unique 3-letter code, city, and country."""
#
#     def __init__(self, country, city, code):
#         self._country = country
#         self._city = city
#         self._code = code
#
#     def __str__(self):
#         return f"{self._code} [{self._city}, {self._country}]"
#
#     def __eq__(self, other):
#         if isinstance(other, Airport):
#             return self._code == other._code
#         return False
#
#     def get_code(self):
#         return self._code
#
#     def get_city(self):
#         return self._city
#
#     def get_country(self):
#         return self._country
#
#     def set_city(self, city):
#         self._city = city
#
#     def set_country(self, country):
#         self._country = country


class Airport:

    def __init__(self, country, city, code):
        self._country = country
        self._city = city
        self._code = code  # Initialize instance variable with provided code [cite: 25]

    def __str__(self):
        return f"{self._code} [{self._city}, {self._country}]"  # Return string representation [cite: 26]

    def __eq__(self, other):
        if not isinstance(other, Airport):  # Check if other is an Airport object [cite: 27]
            return False
        return self._code == other._code  # Compare Airport codes [cite: 26]

    def get_code(self):
        return self._code

    def get_city(self):
        return self._city

    def get_country(self):
        return self._country

    def set_city(self, city):
        self._city = city

    def set_country(self, country):
        self._country = country


if __name__ == '__main__':
    # Test cases for the Airport class
    airport1 = Airport("Canada", "Toronto", "YYZ")
    airport2 = Airport("United States", "Chicago", "ORD")
    airport3 = Airport("Canada", "Vancouver", "YVR")

    print(airport1)  # Test __str__
    print(airport2)

    print(airport1 == airport2)  # Test __eq__ (False)
    print(airport1 == Airport("Canada", "Toronto", "YYZ"))  # Test __eq__ (True)
    print(airport1 == "YYZ")  # Test __eq__ with non-Airport object (False)

    print(airport1.get_code())  # Test getters
    print(airport1.get_city())
    print(airport1.get_country())

    airport1.set_city("Mississauga")  # Test setters
    airport1.set_country("Ontario")
    print(airport1)