"""
Patient.py

DESC:
    A simple class to store identifying information about a patient.

Author: David J. Kim,
Created: 01-16-2026,
Modified: 01-16-2026,
Version: 1.0.0

USAGE:
    - Instantiate with args. Can retrieve specific information using
    getter methods.
    
PLANNED:
    - Add a simple name verifier to ensure names are proper (i.e. no numbers, 
    symbols) before setting.
    - Add a autoformatter before setting to make sure names are capitalized correctly.
    - Add middle name variable.
    
LIMITATIONS:
    Cannot set variables after instantiating, at least, you shouldn't. No setters
    exist yet. Values are not verified before setting, assumes that passed values are
    valid.

DEPENDENCIES:
    - Date
"""

from Date import Date
from Ratings import Ratings

class Patient:
    def __init__(self, first_name: str, last_name: str, title: str, 
                 street: str, address: str, birthday: Date, ratings: Ratings):
        self.first_name = first_name
        self.last_name = last_name
        self.title = title
        self.street = street
        self.address = address
        self.birthday = birthday
        self.ratings = ratings
        
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def get_formal_name(self) -> str:
        return f"{self.title} {self.last_name}"
        
    def get_first_name(self) -> str:
        return self.first_name
    
    def get_last_name(self) -> str:
        return self.last_name
    
    def get_title(self) -> str:
        return self.title
    
    def get_pronoun(self) -> str:
        if self.title is "Mr.":
            return "he"
        return "she"
    
    def get_pronoun_possessive(self) -> str:
        if self.title is "Mr.":
            return "his"
        return "her"        
    
    def get_street(self) -> str:
        return self.street
    
    def get_address(self) -> str:
        return self.address
    
    def get_birthday(self) -> Date:
        return self.birthday
    
    def get_ratings(self) -> dict:
        return self.ratings.get_ratings()
    
# no need for setters, this is good for now