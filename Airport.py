"""
******************************
CS 1026 - Assignment 4  – Air Travel
Code by: Sydney Koziel
Student ID: skoziel
File created: March 26, 2025
******************************
This file defines the Airport class.
Each Airport object represents an airport with a unique 3-letter code,
the city, and the country where it is located. It includes methods
for comparison, string representation, and accessing/modifying
airport attributes.
"""

class Airport:
    """Represents an airport with a unique 3-letter code, city, and country."""

    def __init__(self, country, city, code):
        """Initializes an Airport object."""
        self._country = country
        self._city = city
        self._code = code  # Initialize instance variable with provided code [cite: 25]

    def __str__(self):
        """Returns the string representation of the Airport."""
        return f"{self._code} [{self._city}, {self._country}]"  # Return string representation [cite: 26]

    def __eq__(self, other):
        """Checks if two Airport objects are equal based on their code."""
        if not isinstance(other, Airport):  # Check if other is an Airport object [cite: 27]
            return False
        return self._code == other._code  # Compare Airport codes [cite: 26]

    def get_code(self):
        """Returns the airport code."""
        return self._code

    def get_city(self):
        """Returns the city where the airport is located."""
        return self._city

    def get_country(self):
        """Returns the country where the airport is located."""
        return self._country

    def set_city(self, city):
        """Updates the city of the airport."""
        self._city = city

    def set_country(self, country):
        """Updates the country of the airport."""
        self._country = country


# Optional test cases within the main block
if __name__ == '__main__':
    # Test cases for the Airport class
    airport1 = Airport("Canada", "Toronto", "YYZ")
    airport2 = Airport("United States", "Chicago", "ORD")
    airport3 = Airport("Canada", "Vancouver", "YVR")

    print("--- Airport Class Tests ---")
    print(airport1)  # Test __str__
    print(airport2)

    print(f"airport1 == airport2: {airport1 == airport2}")  # Test __eq__ (False)
    print(f"airport1 == YYZ: {airport1 == Airport('Canada', 'Toronto', 'YYZ')}")  # Test __eq__ (True)
    print(f"airport1 == 'YYZ': {airport1 == 'YYZ'}")  # Test __eq__ with non-Airport object (False)

    print(f"Code: {airport1.get_code()}")  # Test getters
    print(f"City: {airport1.get_city()}")
    print(f"Country: {airport1.get_country()}")

    print("Updating airport1 city and country...")
    airport1.set_city("Mississauga")  # Test setters
    airport1.set_country("Ontario")
    print(f"Updated airport1: {airport1}")
    print("-" * 25)