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
    - enum
    - re
    - os
    - Date
    - Patient
"""

import os, re
from enum import Enum

# custom classes
from Date import Date
from Patient import Patient

class Operations(Enum):
    SINGLE_FILL = 1
    PARTIAL_FILL = 2
    FULL_FILL = 3
    
NOTES_PATH = '../' # directory to check for existing soap notes
    
debug_enabled = False # used to enable/disable debug prints

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

def natural_sort_key(s):
    # splits "SD100" into ["SD", 100]
    return [int(text) if text.isdigit() else text.lower() 
            for text in re.split(r'(\d+)', s)]

def ask_for_debug() -> None:
    global debug_enabled # need to declare the global var explicitly
    while True:
        user_input = input("Enable debug messages? (Y/N) ")
        try:
            # input checks
            if not len(user_input) == 1:
                raise ValueError("Input must be 1 character in length")
            
            if 'Y' not in user_input and 'y' not in user_input and 'N' not in user_input and 'n' not in user_input:
                raise ValueError("Input must be a 'Y' or 'N'")
            
            if 'Y' in user_input or 'y' in user_input:
                debug_enabled = True
            return

        except ValueError as e:
            print(f"[ERROR]: {e}. Please try again.\n")    

def select_function_prompt() -> int:
    # 1 -> single
    # 2 -> partial
    # 3 -> full
    while True:
        user_input = input("""Please select a fill function:\n  Enter '1' for SINGLE FILL
  Enter '2' for PARTIAL FILL\n  Enter '3' for FULL FILL\n""")
        try:
            # input checks
            if not len(user_input) == 1:
                raise ValueError("Input must be 1 character in length")
            
            if '1' not in user_input and '2' not in user_input and '3' not in user_input:
                raise ValueError("Input must be a '1', '2', or '3'")

            return int(user_input)

        except ValueError as e:
            print(f"[ERROR]: {e}. Please try again.\n")
            
def do_single_fill() -> None:
    # check whether soap docs exist
    # this is required for retrieval to succeed
    doc_exists = False
    for filename in os.listdir(NOTES_PATH): # search parent directory
        if filename.endswith('.rtf') and 'SD' in filename:
            if debug_enabled:
                print(f"[DEBUG]: Found {filename}")
            doc_exists = True
            break
        
    if (not doc_exists):
        raise ValueError("SOAP document does not exist in directory. Must be '.rtf' and have 'SD' in filename")
    
    # if notes exist in parent dir, find the most recent file by filtering the filename
    files = os.listdir(NOTES_PATH)
    
    # filter the file list to only include the ones we're searching for
    # - no folders
    # - is .rtf
    # - has 'SD' in filename
    files = [
        f for f in os.listdir(NOTES_PATH)
        if os.path.isfile(os.path.join(NOTES_PATH, f)) and f.endswith('.rtf') and 'SD' in f
    ]
    
    if files:
        prev_note = max(files, key=natural_sort_key)
        if debug_enabled:
            print(f"[DEBUG]: Previous note found -> {prev_note}.")
            
    else: # in the case files are moved/deleted during runtime
        raise ValueError("No matching files found")
    
    # retrieve information, then do single fill generation
    # ...TODO
    
    print("SUCCESS")

# TODO
def do_partial_fill() -> None:
    pass

# TODO
def do_full_fill() -> None:
    pass
        
def main():
    ask_for_debug()
    
    # first thing to do is to prompt the user whether they want to proceed w/
    # single, partial, or full fill for SOAP generation
    try:
        match select_function_prompt():
            case Operations.SINGLE_FILL.value:
                do_single_fill()
                
            case Operations.PARTIAL_FILL.value:
                do_partial_fill()
                
            case Operations.FULL_FILL.value:
                do_full_fill()
            
    except ValueError as e:
        print(f"[ERROR]: {e}. Please try again.\n")
    
if __name__ == "__main__":
    main()