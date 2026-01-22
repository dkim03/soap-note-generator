"""
Ratings.py

DESC:
    A simple class to store a list of complaints and corresponding ratings. Uses
    a dict to store and link these two categories.

Author: David J. Kim,
Created: 01-21-2026,
Modified: 01-21-2026,
Version: 1.0.0

USAGE:
    - Instantiate with a dict. Can retrieve list of complaints and ratings using
      a getter method.
    
PLANNED:
    - ...
    
LIMITATIONS:
    ...

DEPENDENCIES:
    - None
"""

# example dict structure where key is name of complaint and value is rating
# ratings = {
#   "Pain": 8,
#   "Health": 3,
#   "Headache": 9,
#   "Neck": 5
#   "Upper back": 6,
#   "Lower back": 7,
#   ...there may be more than what is listed here
# }

# to add a new key to dict, use:
# patient["dob"] = "01/01/1980"
#           OR use
# patient.update(new_data), where new_data is a dict

class Ratings:
    def __init__(self, rating_dict=None):
        if rating_dict is None:
            rating_dict = {}
        self.ratings = rating_dict
        
    def get_ratings(self) -> dict:
        return self.ratings