"""
main.py

DESC:
    Main execution file for AutoSOAP. Program generates or 'fills in' SOAP-formatted 
    notes in-between existing exams in .rtf format.

Author: David J. Kim,
Created: 01-16-2026,
Modified: 01-16-2026,
Version: 1.0.0

USAGE:
    Place .exe in target directory w/ patient exams and notes, then run .exe in CMD 
    terminal.
    
PLANNED:
    - User-friendly GUI using Tkinter Python library to remove CLI entirely and 
    lower the learning curve
    - Add 'NO EXAM OR NOTES' function that will generate all required exams and 
    notes given patient information
    - Add directory search for info retrieval to avoid having to move .exe around
    
LIMITATIONS:
    Requires existing exams or notes to retrieve patient information. Absence of 
    these files will make program unusable.

DEPENDENCIES:
    - re
    - os
    - Date
    - Patient
"""

import os
import re

# custom classes
from Date import Date
from Patient import Patient

# ------------------------------------------------------------------------------------------------------------------------
#                                             AutoSOAP EXECUTION FLOW outline
# ------------------------------------------------------------------------------------------------------------------------
# there are different functions the user can use to generate notes
# - FULL FILL when exams exist, but no notes in-between
# - PARTIAL FILL when exams and notes exist, but some notes are missing
# - SINGLE FILL when you just want to generate a single note
# - NO EXAMS OR NOTES when you want to completely generate all docs (extended in later version)

# ==================================================
#                    FULL FILL
# ==================================================
# info retrieved from user:
# - list of dates (1/2/26, 1/7/26, etc.)
#
# info retrieved from exam:
# - list of injuries (headache, upper back, lower back, etc.)
# - list of starting injury ratings (6, 7, 4, etc.), excl.
# - necessary patient info
#   - name & title
#   - address
#   - dob
#
# info retrieved from user:
# - list of desired end ratings for each injury (2, 0, 1, etc.), incl.
# 
# how this function works:
# - using any reference exam (EI, EN, EF), user can fully generate the missing notes in-between each exam 

# ==================================================
#                   PARTIAL FILL
# ==================================================
# info retrieved from user:
# - list of dates (1/2/26, 1/7/26, etc.)
# 
# info retrieved from previous SOAP note:
# - list of injuries (headache, upper back, lower back, etc.)
# - list of starting injury ratings (6, 7, 4, etc.), excl.
# - necessary patient info
#   - name & title
#   - address
#   - dob
# 
# info retrieved from user:
# - list of desired end ratings for each injury (2, 0, 1, etc.), incl.
# 
# how this function works:
# - if notes (SD) already exist, use prev note as the reference. using this info, user can generate the missing notes up to some rating

# ==================================================
#                    SINGLE FILL
# ==================================================
# info retrieved from user:
# - single date (1/2/26, 1/7/26, etc.)
# 
# info retrieved from previous SOAP note:
# - list of injuries (headache, upper back, lower back, etc.)
# - list of starting injury ratings (6, 7, 4, etc.), excl.
# - necessary patient info
#   - name & title
#   - address
#   - dob
# 
# info retrieved from user:
# - list of desired end ratings for each injury (2, 0, 1, etc.), incl.
# 
# how this function works:
# - if notes (SD) already exist, use prev note as the reference. using this info, user can generate a single note up to some rating

# ==================================================
#                 NO EXAMS OR NOTES
# ==================================================
# [to be extended later], ignore
# ------------------------------------------------------------------------------------------------------------------------
#                                                         END
# ------------------------------------------------------------------------------------------------------------------------


# PROJECT PROGRESS ('X' -> done, '*' -> WIP, '-' -> not started, '|' -> blocked)
#   SINGLE FILL                                 *
#   > date retrieval                                *
#   > SOAP note info retrieval                      -
#   > rating retrieval                              -
#   > note generation algo                          -
#   PARTIAL FILL                                -
#   FULL FILL                                   -
#   Tkinter GUI integration                     -
#   Deployable prototype                        -
#   NO EXAMS OR NOTES                           |

# OTHER THINGS TO CONSIDER
# - None
        
def main():
    pass
    
if __name__ == "__main__":
    main()