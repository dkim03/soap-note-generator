"""
Date.py

DESC:
    A simple class to store month, day, and year values as ints.

Author: David J. Kim,
Created: 01-16-2026,
Modified: 01-16-2026,
Version: 1.0.0

USAGE:
    - Instantiate with or without args. Can retrieve and set specific information
    using getter and setter methods.
    
PLANNED:
    - Add module to verify dates more thoroughly. Only checks if month, day, and year
    values are within bounds instead of checking whether they exist or not.
    
LIMITATIONS:
    Date verification is extremely simple. Some bad dates can still pass through.

DEPENDENCIES:
    - enum
"""

from enum import Enum

UNSET = -1 # default int value for unset variables

# enums for internal use
class _Month(Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

# months to convert from decimal to string
months = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
    -1: "INVALID"
}

class Date:
    def __init__(self, month: int, day: int, year: int):
        if (self._is_bad_date(month, day, year)):
            # set variables to default
            self.month = UNSET
            self.day = UNSET
            self.year = UNSET
            return        
        self.month = month
        self.day = day
        self.year = year        
        
    def get_date_standard(self) -> str:
        return f"{self.month}/{self.day}/{self.year}"
    
    def get_date_readable(self) -> str:
        return f"{months[self.month]} {self.day}, {self.year}"
    
    def get_month(self) -> int:
        return self.month
    
    def get_day(self) -> int:
        return self.day

    def get_year(self) -> int:
        return self.year
    
    def set_month(self, month: int) -> bool:
        # check validity
        if (self._is_bad_date(month, self.day, self.year)):
            return False # fail state
        self.month = month
        return True

    def set_day(self, day: int) -> bool:
        if (self._is_bad_date(self.month, day, self.year)):
            return False
        self.day = day
        return True
        
    def set_year(self, year: int) -> bool:
        if (self._is_bad_date(self.month, self.day, year)):
            return False
        self.year = year
        return True
    
    def set_date(self, month, day, year) -> bool:
        if (self._is_bad_date(month, day, year)):
            return False
        self.month = month
        self.day = day
        self.year = year
        return True       

    # returns true if incorrect, false otherwise
    # private method, no public use
    def _is_bad_date(self, month: int, day: int, year: int) -> bool:
        return (month < _Month.JANUARY.value or
                month > _Month.DECEMBER.value or
                day < 0 or day > 31 or year < 0 or
                (day > 29 and month is _Month.FEBRUARY.value))
