"""
main.py

DESC:
    Main execution file for AutoSOAP. Program generates or 'fills in' SOAP-formatted 
    notes in-between existing exams in .rtf format.

Author: David J. Kim,
Created: 01-16-2026,
Modified: 01-22-2026,
Version: 1.0.0

USAGE:
    Place .exe in target directory w/ patient exams and notes, then run .exe in CMD 
    terminal.
    
PLANNED:
    - User-friendly GUI using Tkinter Python library to remove CLI entirely and 
      lower the learning curve.
    - Add 'NO EXAM OR NOTES' function that will generate all required exams and 
      notes given patient information.
    - Add directory search for info retrieval to avoid having to move .exe around.
    
LIMITATIONS:
    - Requires existing exams or notes to retrieve patient information. Absence of 
      these files will make program unusable.
    - Previous notes must be named in the format: 'SD_Patient_Name_1' ...
      'SD_Patient_Name_3' to work correctly.
    - Exams must be named similar to 'EI_Patient_Name' for initial exam,
      'EN_Patient_Name_1' for intermediate exams, and 'EF_Patient_Name' for
      final exam.

DEPENDENCIES:
    - enum
    - re
    - os
    - Date
    - Patient
"""

import os, re
from enum import Enum
from striprtf.striprtf import rtf_to_text

# custom classes
from Date import Date
from Patient import Patient
from Ratings import Ratings

class Operations(Enum):
    SINGLE_FILL = 1
    PARTIAL_FILL = 2
    FULL_FILL = 3
    
NOTES_PATH = '../' # directory to check for existing soap notes
    
debug_enabled = False # used to enable/disable debug prints
patient = None

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
#   > SOAP note patient info retrieval              X
#   > rating retrieval                              X
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
            
def find_previous_note() -> str:
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
    
    # find the previous note by finding the file with the biggest number postfix
    # - note name must follow this format: SD_Patient_Name_100
    if files:
        prev_note = max(files, key=natural_sort_key)
        if debug_enabled:
            print(f"[DEBUG]: Previous note found -> {prev_note}.")
        return prev_note
            
    # in case files are moved/deleted during runtime
    raise ValueError("No matching files found")    

def retrieve_info_from_SD(filename: str) -> None:
    # retrieve information from prev_note that was found
    global patient

    # read the file
    with open(f"{NOTES_PATH}{filename}", 'r', encoding='cp1252') as f:
        raw_rtf = f.read()
    
    # convert to plain text, removing rtf junk and space elements out evenly
    plain_text = str(rtf_to_text(raw_rtf))
    normalized = " ".join(plain_text.split())
    
    # used to space elements out evenly to keep it consistent to ensure
    # patterns can be used for street, address retrieval
    raw_rtf_normalized = " ".join(raw_rtf.split())
    
    if debug_enabled:
        print(plain_text)
        
    # find ratings
    ratings = {}
    rating_pattern = r"On a scale of 0 to 10 with 10 being the worst,.*?\."
    rating_match = re.search(rating_pattern, normalized, re.IGNORECASE | re.DOTALL)
    if rating_match:
        rating_sentence = rating_match.group(0)
        
        if debug_enabled:
            print(f"[DEBUG]: found -> {rating_sentence}")
        
        # within found sentence, find pairs
        pair_pattern = r"(?P<complaint>.*?) as a (?P<rating>\d+)"
        pair_matches = re.findall(pair_pattern, rating_sentence)
        if not pair_matches:
            raise ValueError("Failed to find complaint-rating pairs, check syntax")
        
        # clean up pronouns, extract complaint & rating then store in dict
        for complaint, rating in pair_matches:
            clean_complaint = re.sub(r".*?(his|her|and)", "", complaint, flags=re.IGNORECASE).strip()
            clean_complaint = clean_complaint.lstrip(',').strip() # remove comma and any whitespace
            ratings[clean_complaint] = int(rating)
        
    else:
        raise ValueError("Failed to find ratings in note document, check syntax")
    
    # find title
    title = ""
    title_pattern = r"(Mr\.|Mrs\.|Ms\.)"
    title_match = re.search(title_pattern, normalized, re.IGNORECASE)
    if title_match:
        title = title_match.group(1)
        if debug_enabled:
            print(f"[DEBUG]: read {title}")
    else:
        raise ValueError("Failed to find title in note document, check syntax")
    
    # find patient info
    name_date_pattern = (
        r"Doctor:\s*Sungjun\s*Jung\s+"                         # anchor
        r"(?P<name>.*?)\s+"                                    # match name until we see numbers
        r"(?P<street>\d+[\s\w]+?)\s+"                          # ignore
        r"(?P<address>.+?)\s+"                                 # ignore
        r"Date\s+of\s+Birth:\s+(?P<dob>\d{1,2}/\d{1,2}/\d{4})" # match strictly the date format
    )    
    name_date_match = re.search(name_date_pattern, normalized, re.IGNORECASE)
    
    if name_date_match:
        # extract data from groups
        name = name_date_match.group('name').strip()
        dob = name_date_match.group('dob').strip()
        
        if debug_enabled:
            print(f"[DEBUG]: read {name}")
            print(f"[DEBUG]: read {dob}")
        
        name_parts = name.strip().split(" ")
        if len(name_parts) != 2:
            raise ValueError("Incorrect number of parts in patient name. Only 2 parts supported")
        first, last = map(str, name_parts)
        
        date_parts = dob.strip().split("/")
        month, day, year = map(int, date_parts)
        
        street_address_pattern = (
            rf"{last}\s*\\par\s*"          # start after the last name
            r"(?P<street>[^\\]+?)\s*\\par\s*"      # match street until the next \par
            r"(?P<address>[^\\]+?)\s*\\par\s*"     # match address until the next \par
            r"Date"                                # stop at "Date"
        )
        street_address_match = re.search(street_address_pattern, raw_rtf_normalized, re.IGNORECASE)
        
        street = ""
        address = ""
        if street_address_match:
            street = street_address_match.group('street').strip()
            address = street_address_match.group('address').strip()
            
            if debug_enabled:
                print(f"[DEBUG]: read {street}")
                print(f"[DEBUG]: read {address}")
        else:
            raise ValueError("Failed to find street or address in note document, check syntax")
        
        # create Patient obj and consolidate necessary information
        patient = Patient(first, last, title, street, address, Date(month, day, year), Ratings(ratings))
        if debug_enabled:
            print(f"[DEBUG]: {patient.get_title()} {patient.get_full_name()}")
            print(f"[DEBUG]: {patient.get_street()}")
            print(f"[DEBUG]: {patient.get_address()}")
            print(f"[DEBUG]: {patient.get_birthday().get_date_readable()}")
            print(f"[DEBUG]: {patient.get_ratings()}")   

    else:
        raise ValueError("Failed to extract patient data")     

def do_single_fill() -> None:
    # get patient info for note
    print(f"Retieving patient info...")
    retrieve_info_from_SD(find_previous_note())
    
    
    print("\nSUCCESS")

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