"""
Patient.py

DESC:
    A simple class to store identifying information about a patient.

Author: David J. Kim,
Created: 01-16-2026,
Modified: 01-16-2026,
Version: 1.0.0

USAGE:
    - Instantiate with or without args. Can retrieve specific information using
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

import Date

class Patient:
    def __init__(self):
        self.first_name = "John"
        self.last_name = "Doe"
        self.title = "Mr."
        self.street = "123 Main Street"
        self.address = "Anytown, USA 12345"
        self.birthday = Date()
    
    def __init__(self, first_name: str, last_name: str, title: str, 
                 address: str, birthday: Date):
        self.first_name = first_name
        self.last_name = last_name
        self.title = title
        self.address = address
        self.birthday = birthday
        
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
    
    def get_street(self) -> str:
        return self.street
    
    def get_address(self) -> str:
        return self.address
    
    def get_birthday(self) -> Date:
        return self.birthday
    
# no need for setters, this is good for now