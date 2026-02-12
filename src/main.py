"""
main.py

DESC:
    Main execution file for AutoSOAP. Program generates or 'fills in' SOAP-formatted 
    notes in-between existing exams in .rtf format.

Author: David J. Kim,
Created: 01-16-2026,
Modified: 01-30-2026,
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
    - collections
    - enum
    - os    
    - re
    - simplertf
    - striprtf
    - Date
    - Patient
    - Ratings
"""

import os, re
import tkinter as tk
from simplertf import simplertf

from datetime import date
from enum import Enum
from striprtf.striprtf import rtf_to_text
from tkcalendar import Calendar

# custom classes
from Date import Date
from Note import Note
from Patient import Patient
from Ratings import Ratings

r = simplertf.RTF("Test Generation")
r.stylesheet = "English"

class Operations(Enum):
    SINGLE_FILL = 1
    PARTIAL_FILL = 2
    FULL_FILL = 3
    
class Sections(Enum):
    SUBJECTIVE = 0
    OBJECTIVE = 1
    ASSESSMENT = 2
    
NOTES_PATH = '../' # directory to check for existing soap notes
PAGE_HEIGHT = "11in"
PAGE_WIDTH = "8.5in"
MARGIN_TOP = MARGIN_BOTTOM = MARGIN_LEFT = MARGIN_RIGHT = "1in"

# # do initial page set up
# r.set_layout(ph="11in", pw="8.5in", mt="1in", mb="1in", ml="1in", mr="1in")

# prefixes to denote different terminal msgs
ERROR_MSG_PREFIX = "[ERROR]: "
DEBUG_MSG_PREFIX = "[DEBUG]: "
INFO_MSG_PREFIX = "[INFO]: "
    
debug_enabled = False # used to enable/disable debug prints msgs
patient = None # Patient obj to store all demographic info

# spinous regions related to tenderness
tender_cervical_regions = []
tender_thoracic_regions = []
tender_lumbar_regions = []

# various sentences to help reconstruct the new note document

# sorted via index:
# 0 -> tone, 1 -> trigger, 2 -> rom, 3 -> pain
sorted_cervical_sentences = []
sorted_thoracic_sentences = []
sorted_lumbar_sentences = []
lumbar_tenderness_sentence = []

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
#   > date retrieval                                X
#   > SOAP note patient info retrieval              X
#   > ratings, etc. retrieval                       X
#   > note generation algo                          *
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
            print(f"{ERROR_MSG_PREFIX}{e}. Please try again.\n")    
            
            
def get_single_date_prompt() -> Date:
    while True:
        user_input = input("")

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
            print(f"{ERROR_MSG_PREFIX}{e}. Please try again.\n")
            
            
def find_previous_note() -> str:
    # check whether soap docs exist
    # this is required for retrieval to succeed
    doc_exists = False
    for filename in os.listdir(NOTES_PATH): # search parent directory
        if filename.endswith('.rtf') and 'SD' in filename:
            if debug_enabled:
                print(f"{DEBUG_MSG_PREFIX}found {filename}")
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
            print(f"{DEBUG_MSG_PREFIX}Previous note found -> {prev_note}.")
        return prev_note
            
    # in case files are moved/deleted during runtime
    raise ValueError("No matching files found")    


def retrieve_info_from_SD(filename: str) -> None:
    # retrieve information from prev_note that was found
    global patient, tender_cervical_regions, tender_thoracic_regions, tender_lumbar_regions, sorted_cervical_sentences, sorted_thoracic_sentences, sorted_lumbar_sentences, lumbar_tenderness_sentence

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
            
        # add overall pain and health ratings
        after_title = normalized.split("Complaint", 1)[-1] # get all words after 'Complaint'
        all_numbers = re.findall(r"\d+", after_title) # get all numbers
        pain_health_ratings = {
            "pain": int(all_numbers[2]), # get pain rating
            "health": int(all_numbers[5]) # get health rating
        }
        ratings.update(pain_health_ratings) # add to ratings dict
        
        if debug_enabled:
            print(f"{DEBUG_MSG_PREFIX}rating_sentence -> {rating_sentence}")   

    else:
        raise ValueError("Failed to find ratings in note document, check syntax")
    
    # find title
    title = ""
    title_pattern = r"(Mr\.|Mrs\.|Ms\.|Dr\.)"
    title_match = re.search(title_pattern, normalized, re.IGNORECASE)
    if title_match:
        title = title_match.group(1)
        if debug_enabled:
            print(f"{DEBUG_MSG_PREFIX}title -> {title}")
    else:
        raise ValueError("Failed to find title in note document, check syntax")
    
    # find patient info and store in Patient obj
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
            print(f"{DEBUG_MSG_PREFIX}name -> {name}")
            print(f"{DEBUG_MSG_PREFIX}dob -> {dob}")
        
        name_parts = name.strip().split(" ")
        if len(name_parts) != 2:
            raise ValueError("Incorrect number of parts in patient name. Only 2 parts supported")
        first, last = map(str, name_parts)
        
        date_parts = dob.strip().split("/")
        month, day, year = map(int, date_parts)
        
        # find street and address
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
                print(f"{DEBUG_MSG_PREFIX}street -> {street}")
                print(f"{DEBUG_MSG_PREFIX}address -> {address}")
        else:
            raise ValueError("Failed to find street or address in note document, check syntax")
        
        # create Patient obj and consolidate necessary information
        patient = Patient(first, last, title, street, address, Date(month, day, year), Ratings(ratings))
        if debug_enabled:
            print(f"{DEBUG_MSG_PREFIX}{patient.get_title()} {patient.get_full_name()}")
            print(f"{DEBUG_MSG_PREFIX}{patient.get_street()}")
            print(f"{DEBUG_MSG_PREFIX}{patient.get_address()}")
            print(f"{DEBUG_MSG_PREFIX}{patient.get_birthday().get_date_readable()}")
            print(f"{DEBUG_MSG_PREFIX}{patient.get_ratings()}")   
    else:
        raise ValueError("Failed to extract patient data. Check whether read note has correct formatting for name, street, address, and dob")     
    
    # find regions in regards to tenderness/palpation
    # problem with this is that it gets ALL cervical regions, this is not correct
    # one way to do this is to get all sentences that mention a spinous process then scan for C#, T#, or L# since
    # those sentences are always related to tenderness/palpation (afaik)
    
    tenderness_targets = ["spinous process", "spinous levels", "following levels"]
    tenderness_region_sentences = []
    find_sentences(tenderness_targets, tenderness_region_sentences, normalized, re.IGNORECASE)
    
    for sentence in tenderness_region_sentences:
        # for every sentence found, scan for these patterns within them, then add to list  if found
        tender_cervical_regions.extend(re.findall(r"\bC\d+", sentence, re.IGNORECASE))
        tender_thoracic_regions.extend(re.findall(r"\bT\d+", sentence, re.IGNORECASE))
        tender_lumbar_regions.extend(re.findall(r"\bL\d+", sentence, re.IGNORECASE))
    
    if not tender_cervical_regions:
        print(f"{INFO_MSG_PREFIX}No cervical regions found, continuing...")
        
    if not tender_thoracic_regions:
        print(f"{INFO_MSG_PREFIX}No thoracic regions found, continuing...")    
        
    if not tender_lumbar_regions:
        print(f"{INFO_MSG_PREFIX}No lumbar regions found, continuing...")
    
    if debug_enabled:
        print(f"{DEBUG_MSG_PREFIX}tender_cervical_regions -> {tender_cervical_regions}")
        print(f"{DEBUG_MSG_PREFIX}tender_thoracic_regions -> {tender_thoracic_regions}")
        print(f"{DEBUG_MSG_PREFIX}tender_lumbar_regions -> {tender_lumbar_regions}")


    # extract OBJECTIVE paragraph content
    objective_paragraph = re.search(r"Objective\s+(.*?)\s+Assessment", normalized, re.DOTALL)
    if objective_paragraph:
        print(f"{DEBUG_MSG_PREFIX}objective_paragraph -> {objective_paragraph.group(1).strip()}")
    else:
        raise ValueError("No objective paragraph found")
    
    # break up the paragraph into individual sentences, remove last element as it's blank
    objective_sentences = objective_paragraph.group(1).strip().split(".")[:-1]
    print(f"{DEBUG_MSG_PREFIX}objective_sentences -> {objective_sentences}")
    
    
    # each sentence now has an index associated with it
    
    # handle each case:
    # - there are 2^3 cases. there are 3 distinct sections and each of them may or may not be present in the paragraph.
    # - the hardest part is categorizing each sentence correctly to each section since this is not explicitly denoted and the wording varies.
    # - having the index can be useful in SOME cases
    
    
    # we can go through the individual sentences found in the objective section and easily find indices that are part of one section or the other.
    # the most obvious pattern is the list of spinous levels which do split the paragraph into their distinct sections
    # the only exception is lumbar as it mentions tender regions before listing its spinous process
    
    # get the indices where the sections start
    section_end_indices = []
    for i, sentence in enumerate(objective_sentences):
        if re.search(r"[A-Z]\d+", sentence):
            section_end_indices.append(i)
            
    # store sentences inside distinct regions within the objective paragraph
    cervical_sentences = []
    thoracic_sentences = []
    lumbar_sentences = []
            
    # we can identify which section is which by referring to the regions we found in the previous paragraph
    # handle each unique case by categorizing accordingly
    if not tender_cervical_regions:
        if not tender_thoracic_regions:
            if not tender_lumbar_regions:
                raise ValueError("No regions found. Check document syntax")
            else:
                # only lumbar region
                lumbar_sentences.extend(objective_sentences)
                
        else:
            if not tender_lumbar_regions:
                # only thoracic region
                thoracic_sentences.extend(objective_sentences)
                
            else:            
                # thoracic, lumbar
                for i, sentence in enumerate(objective_sentences):
                    if (i < section_end_indices[1]):
                        thoracic_sentences.append(sentence)
                    else:
                        lumbar_sentences.append(sentence)
            
    else:
        if not tender_thoracic_regions:
            if not tender_lumbar_regions:
                # only cervical region
                cervical_sentences.extend(objective_sentences)
                
            else:
                # cervical, lumbar
                for i, sentence in enumerate(objective_sentences):
                    if (i < section_end_indices[1]):
                        cervical_sentences.append(sentence)
                    else:
                        lumbar_sentences.append(sentence)
                
        else:
            if not tender_lumbar_regions:
                # cervical, thoracic
                for i, sentence in enumerate(objective_sentences):
                    if (i < section_end_indices[1]):
                        cervical_sentences.append(sentence)
                    else:
                        thoracic_sentences.append(sentence)
                
            else:               
                # all regions present 
                for i, sentence in enumerate(objective_sentences):
                    if (i < section_end_indices[1]):
                        cervical_sentences.append(sentence)
                    elif (i < section_end_indices[2]):
                        thoracic_sentences.append(sentence)
                    else:
                        lumbar_sentences.append(sentence)
        
    # find and categorize sentences within each region
    cervical_tone = ""
    thoracic_tone = ""
    lumbar_tone = ""
    cervical_trigger = ""
    thoracic_trigger = ""
    lumbar_trigger = ""   
    cervical_rom = ""
    thoracic_rom = ""
    lumbar_rom = ""  
    cervical_pain = ""
    thoracic_pain = ""
    lumbar_pain = ""
    if cervical_sentences:
        for sentence in cervical_sentences:
            if re.search(r"hypertonicity|increased tonus|muscle tone", sentence, re.IGNORECASE):
                cervical_tone = sentence
            if "trigger points" in sentence:
                cervical_trigger = sentence
            if re.search(r"ROM|range of motion|ranges of motion", sentence):
                cervical_rom = sentence            
            if re.search(r"experienced discomfort|experienced pain|complained|reported pain|pain was elicited|there is pain|there was pain|increased pain|felt discomfort", sentence):
                cervical_pain = sentence                    
                
    if thoracic_sentences:
        for sentence in thoracic_sentences:   
            if re.search(r"hypertonicity|increased tonus|muscle tone", sentence, re.IGNORECASE):
                thoracic_tone = sentence
            if "trigger points" in sentence:
                thoracic_trigger = sentence   
            if re.search(r"ROM|range of motion|ranges of motion", sentence):
                thoracic_rom = sentence                       
            if re.search(r"experienced discomfort|experienced pain|complained|reported pain|pain was elicited|there is pain|there was pain|increased pain|felt discomfort", sentence):
                thoracic_pain = sentence                       
                
    if lumbar_sentences:
        for sentence in lumbar_sentences:    
            if re.search(r"hypertonicity|increased tonus|muscle tone", sentence, re.IGNORECASE):
                lumbar_tone = sentence
            if "trigger points" in sentence:
                lumbar_trigger = sentence    
            if re.search(r"ROM|range of motion|ranges of motion", sentence):
                lumbar_rom = sentence
            if re.search(r"experienced discomfort|experienced pain|complained|reported pain|pain was elicited|there is pain|there was pain|increased pain|felt discomfort", sentence):
                lumbar_pain = sentence                       
    
    lumbar_tenderness_targets = ["there is tenderness in", "there is tenderness upon",
                                 "tenderness is notable", "reveals tenderness",
                                 "tenderness is present", "pain in the lumbar",
                                 "reveals tender areas"]
    find_sentences(lumbar_tenderness_targets, lumbar_tenderness_sentence, normalized, re.IGNORECASE)    
    
    sorted_cervical_sentences = [cervical_tone, cervical_trigger, cervical_rom, cervical_pain]
    sorted_thoracic_sentences = [thoracic_tone, thoracic_trigger, thoracic_rom, thoracic_pain]
    sorted_lumbar_sentences = [lumbar_tone, lumbar_trigger, lumbar_rom, lumbar_pain]
    
    if debug_enabled:
        print(f"{DEBUG_MSG_PREFIX}cervical_sentences -> {cervical_sentences}")
        print(f"{DEBUG_MSG_PREFIX}cervical_tone -> {cervical_tone}")
        print(f"{DEBUG_MSG_PREFIX}cervical_trigger -> {cervical_trigger}")
        print(f"{DEBUG_MSG_PREFIX}cervical_rom -> {cervical_rom}")
        print(f"{DEBUG_MSG_PREFIX}cervical_pain -> {cervical_pain}")

        print(f"{DEBUG_MSG_PREFIX}thoracic_sentences -> {thoracic_sentences}")
        print(f"{DEBUG_MSG_PREFIX}thoracic_tone -> {thoracic_tone}")
        print(f"{DEBUG_MSG_PREFIX}thoracic_trigger -> {thoracic_trigger}")
        print(f"{DEBUG_MSG_PREFIX}thoracic_rom -> {thoracic_rom}")        
        print(f"{DEBUG_MSG_PREFIX}thoracic_pain -> {thoracic_pain}")
                
        print(f"{DEBUG_MSG_PREFIX}lumbar_sentences -> {lumbar_sentences}")
        print(f"{DEBUG_MSG_PREFIX}lumbar_tone -> {lumbar_tone}")
        print(f"{DEBUG_MSG_PREFIX}lumbar_trigger -> {lumbar_trigger}")
        print(f"{DEBUG_MSG_PREFIX}lumbar_rom -> {lumbar_rom}")   
        print(f"{DEBUG_MSG_PREFIX}lumbar_pain -> {lumbar_pain}")                 
        print(f"{DEBUG_MSG_PREFIX}lumbar tenderness sentence -> {lumbar_tenderness_sentence}")
        
        print(f"{DEBUG_MSG_PREFIX}sorted_cervical_sentences -> {sorted_cervical_sentences}")  
        print(f"{DEBUG_MSG_PREFIX}sorted_thoracic_sentences -> {sorted_thoracic_sentences}")  
        print(f"{DEBUG_MSG_PREFIX}sorted_lumbar_sentences -> {sorted_lumbar_sentences}")  
        print(f"{DEBUG_MSG_PREFIX}section_end_indices -> {section_end_indices}")

    
def find_sentences(targets: list[str], destination: list[str], content: str, search_flag) -> bool:
    # do search of target strings
    group = rf"\b({'|'.join(map(re.escape, targets))})\b"
    matches = re.findall(rf"([^.]*?{group}[^.]*\.)", content, search_flag)
    
    # clean then append matches to passed-in list
    if matches:
        for sentences in matches:
            sentence = sentences[0]
            destination.append(str(sentence).strip())
        return True
    
    # no matches found
    print(f"{INFO_MSG_PREFIX}no sentences found, continuing...")
    return False


def print_success_msg() -> None:
    print("\n=============")
    print("|  SUCCESS  |")
    print("=============\n")
    
    
def get_date_from_calendar() -> date | None:
    selected_date: date | None = None

    root = tk.Tk()
    root.withdraw()

    win = tk.Toplevel(root)
    win.title("Select a date")

    cal = Calendar(
        win,
        selectmode="day",
        date_pattern="mm/dd/yyyy"
    )
    cal.pack(padx=10, pady=10)

    def ok():
        nonlocal selected_date
        selected_date = cal.selection_get()
        win.destroy()
        root.destroy()

    tk.Button(win, text="OK", command=ok).pack(pady=5)

    win.grab_set()
    win.wait_window()

    return selected_date
    
    
def add_header_section(date: Date) -> None:
    if not patient:
        raise ValueError("Patient is None")
    
    # do initial page set up
    r.set_layout(ph=PAGE_HEIGHT, pw=PAGE_WIDTH, mt=MARGIN_TOP, mb=MARGIN_BOTTOM, ml=MARGIN_LEFT, mr=MARGIN_RIGHT)
    
    # add page content
    r.par("Back to Wellness", style="s26")
    r.par("4629 168th St SW Ste B", style="s26")
    r.par("Lynnwood, WA 98037", style="s26")
    r.par("425-741-0600", style="s26")
    r.par("Doctor: Sungjun Jung", style="s26")
    
    # add patient info
    r.par(f"{patient.get_full_name()}", style="s27")
    r.par(f"{patient.get_street()}", style="s27")
    r.par(f"{patient.get_address()}", style="s27")
    r.par(f"Date of Birth: {patient.get_birthday().get_date_standard()}", style="s27")

    # add title
    r.par("AutoSOAP Notes", style="s25") # title

    # add date
    r.par(f"{date.get_date_standard()}", style="s28")


def generate_content() -> None:
    global patient, tender_cervical_regions, tender_thoracic_regions, tender_lumbar_regions, sorted_cervical_sentences, sorted_thoracic_sentences, sorted_lumbar_sentences, lumbar_tenderness_sentence
    if not patient:
        raise ValueError("Patient is None")
    
    sorted_sentences = {
        "tender_cervical": tender_cervical_regions,
        "tender_thoracic": tender_thoracic_regions,
        "tender_lumbar": tender_lumbar_regions,
        "sorted_cervical": sorted_cervical_sentences,
        "sorted_thoracic": sorted_thoracic_sentences,
        "sorted_lumbar": sorted_lumbar_sentences,
        "lumbar_tenderness": lumbar_tenderness_sentence
    }
    
    note = Note(patient, sorted_sentences)

    # add sections
    r.par(f"Subjective Complaint", style="s28")
    r.par(note.get_paragraph(Sections.SUBJECTIVE.value), style="s21")
    r.par(f"Objective", style="s28")
    r.par(note.get_paragraph(Sections.OBJECTIVE.value), style="s21")
    r.par(f"Assessment", style="s28")
    r.par(note.get_paragraph(Sections.ASSESSMENT.value), style="s21")
    r.par(f"Plan", style="s28")


def do_single_fill() -> None:
    # get patient info from notes
    print(f"Retieving patient info...")
    filename = find_previous_note()
    # retrieve_info_from_SD(filename)
    retrieve_info_from_SD("SD_Three_Regions_1.rtf")
    # retrieve_info_from_SD("SD_opened_with_word_alt.rtf")
    
    # ask for a date
    date = get_date_from_calendar()
    temp = None
    if date:
        temp = Date(date.month, date.day, date.year)
    else:
        raise ValueError("Recieved date is None")
    
    # split note generation into 4 sections:
    # - page setup & document header        X
    # - SUBJECTIVE                          X
    # - OBJECTIVE                           X
    # - ASSESSMENT                          X
    # - PLAN & TREATMENT                    *
    add_header_section(temp)
    generate_content()
    r.create("test") # output .rtf file
    print_success_msg()
    

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
        print(f"{ERROR_MSG_PREFIX}{e}. Please try again.\n")
    
if __name__ == "__main__":
    main()