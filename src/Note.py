"""
Note.py

DESC:
    A simple class to store lists of sentences in order to generate SOAP notes

Author: David J. Kim,
Created: 01-23-2026,
Modified: 01-23-2026,
Version: 1.0.0

USAGE:
    - Instantiate with a dict. Can retrieve list of complaints and ratings using
      a getter method.
    
PLANNED:
    - ...
    
LIMITATIONS:
    ...

DEPENDENCIES:
    - Patient
"""

import random
import re
from enum import Enum
from Patient import Patient

RATING_CEILING = 10

class Sections(Enum):
    SUBJECTIVE = 0
    OBJECTIVE = 1
    ASSESSMENT = 2
    PLAN = 3
    
target_ratings: dict[str, int] = {}
overall_assessment = ""
improving_complaints = []
unchanged_complaints = []
worsening_complaints = []

# start at 1, idx 0 is storing the prev note ratings
note_counter = 1

class Note:
    def __init__(self, patient: Patient, sorted_sentences: dict[str, list], complaint_ratings=None):
        global target_ratings, overall_assessment, improving_complaints, unchanged_complaints, worsening_complaints, note_counter
        self.patient = patient
        
        # reset global variables
        overall_assessment = ""
        improving_complaints.clear()
        unchanged_complaints.clear()
        worsening_complaints.clear()
        
        # are ratings already generated?
        if not complaint_ratings: # no, do manual
            target_ratings = self.get_target_ratings() # get the target rating for this note obj manually
        else: # yes, map the ratings out
            for i, (complaint, rating) in enumerate(patient.get_ratings().items()):
                target_ratings[complaint] = complaint_ratings[i][note_counter]
            note_counter+=1 # increment to next set of ratings for next note
        
        self.sorted_sentences = sorted_sentences
        
        # SUBJECTIVE sentence bank
        self.subjective_intro = [
            f"{self.patient.get_formal_name()} was evaluated today to determine progress and response to the current treatment plan.",
            f"{self.patient.get_formal_name()} was evaluated today to assess {self.patient.get_pronoun_possessive()} response to care.",
            f"{self.patient.get_formal_name()} was evaluated today for progress and response to treatment.",
            f"{self.patient.get_formal_name()} was checked for {self.patient.get_pronoun_possessive()} responsiveness to the treatment plan.",
            f"{self.patient.get_formal_name()} was assessed today for progress and response to the plan of care.",
            f"{self.patient.get_formal_name()} was examined today to determine progress with the current treatment plan.",
            f"{self.patient.get_formal_name()}'s overall response to the treatment plan was evaluated today."
        ]

        self.subjective_pain_intro = [
            f" The following are the patient's subjective response to questions regarding {self.patient.get_pronoun_possessive()} pain levels: ",
            " The patient's subjective response to a question regarding pain levels: ",
            f" The patient was asked about {self.patient.get_pronoun_possessive()} pain levels which {self.patient.get_pronoun()} rated as follows: ",
            " The patient's subjective responses to questions are as follows in regards to pain levels: ",
            f" The patient rated {self.patient.get_pronoun_possessive()} overall pain level today on a scale of 0 (no pain) to 10 (excruciating pain). ",
            f" The patient was questioned about {self.patient.get_pronoun_possessive()} pain scale: ",
            f" The patient was asked subjective questions regarding {self.patient.get_pronoun_possessive()} pain levels: "
        ]
        
        self.subjective_overall_pain = [
            " Overall pain level today on a scale of 0 (no pain) to 10 (excruciating pain) is considered a ",
            " Current pain level today on a scale of 0 (no pain) to 10 (unbearable pain) is considered a ",
            f" {self.patient.get_pronoun_possessive()} pain level today on a scale of 0 (no pain) to 10 (unbearable pain) is reported to be ",
            f" General pain level today, on a scale of 0 (no pain) to 10 (unbearable pain), is evaluated as "
        ]
        
        self.subjective_health = [
            f" The patient rated {self.patient.get_pronoun_possessive()} overall health on a scale of 1 to 10 as a ",
            f" The patient reported that {self.patient.get_pronoun_possessive()} overall health on a scale of 1 to 10 is rated as a ",
            " The patient's general health was rated on a scale of 1 to 10; it was rated as a ",
            " Overall health on a scale of 1 to 10 is rated as ",
            " Current health on a scale of 1 to 10 is rated a "
        ]
        
        # optional sentence(s)
        # - improving, unchanging, worsening complaints (this depends on generated ratings)
        self.subjective_assessment_improving = [
            f" The patient disclosed {self.patient.get_pronoun()} is feeling improvements in {self.patient.get_pronoun_possessive()} ",
            f" The patient reported that {self.patient.get_pronoun()} felt improvements in {self.patient.get_pronoun_possessive()} ",
            f" Today, the patient says there are improvements in {self.patient.get_pronoun_possessive()} "
        ]
        
        self.subjective_assessment_unchanged = [
            " The patient reported that the following complaints have not changed since the last visit: ",
            " Today, there is no change in the patient's ",
            f" During today's visit, the patient reported no change in {self.patient.get_pronoun_possessive()} "
        ]
        
        self.subjective_assessment_worsening = [
            " The patient's complaints have become worse since the last visit; notably, in their ",
            " Today, the following complaints have become worse since the last visit: "
        ]
        
        self.subjective_ratings = [
            f" On a scale of 0 to 10 with 10 being the worst, {self.patient.get_pronoun()} rated {self.patient.get_pronoun_possessive()} "
        ]
        
        # OBJECTIVE sentence bank
        self.objective_tender_cervical = [
            "Palpation of the cervical spine displayed tenderness in the spinous process at: ",
            "Evaluation of the cervical spine revealed tenderness at the following levels: ",
            "Examination of the cervical region indicated discomfort and pain in the spinous process at: ",
            "Evaluation of the cervical spinal areas showed discomfort to be present in the spinous process at: ",
            "There is tenderness of the following cervical spinous levels: ",
            "Cervical spine tenderness was noted in the spinous process region at: ",
            "Cervical spine palpation elicited tenderness of spinous process at "
        ]
        
        self.objective_tone_cervical = [
            " Palpation of the cervical musculature demonstrates hypertonicity in the ",
            " Examination of the cervical spine region indicates the presence of increased tonus in the ",
            " Evaluation of the cervical spinal area shows hypertonicity in the ",
            " There is hypertonicity of the ",
            " Hypertonicity is palpable in the ",
            " Hypertonicity is found in the ",
            " Cervical spine palpation reveals increased muscle tone of the "
        ]
        
        self.objective_trigger_cervical = [
            " Palpatory examination of the cervical musculature displays myofascial trigger points of the ",
            " Palpation of the cervical musculature reveals myofascial trigger points of the ",
            " Examination of the cervical spine reveals myofascial trigger points of the ",
            " Palpation of the cervical region indicates the presence of trigger points in the ",
            " Myofascial trigger points are palpated in the ",
            " Myofascial trigger points are present in the "
        ]
        
        self.objective_rom_cervical = [
            " Examination of the cervical spine revealed ROM has decreased.",
            " Cervical spine evaluation shows that range of motion has decreased.",
            " Cervical spine evaluation shows that ROM has deteriorated.",
            " Ranges of motion in the cervical region have lowered.",
            " Cervical range of motion has decreased.",
            " Cervical spine ROM has worsened."
        ]
        
        self.objective_tender_thoracic = [
            " Palpation of the thoracic spine displayed tenderness in the spinous process at: ",
            " Examination of the thoracic spine revealed tenderness at the following levels: ",
            " There is tenderness of the following thoracic spinous levels: ",
            " Examination of the thoracic region indicated discomfort and pain in the spinous process at: ",
            " Evaluation of the thoracic spinal areas showed discomfort to be present in the spinous process at: ",
            " Thoracic spine tenderness was noted in the spinous process region at: ",
            " Thoracic spine palpation elicited tenderness of spinous process at "
        ]
        
        self.objective_tone_thoracic = [
            " Palpation of the thoracic musculature demonstrates hypertonicity in the ",
            " Examination of the thoracic spine region indicates the presence of increased tonus in the ",
            " Evaluation of the thoracic spinal area shows hypertonicity in the ",
            " There is hypertonicity of the thoracic spinal area in the ",
            " Hypertonicity of the thoracic spine is palpable in the ",
            " Hypertonicity is palpable in the ",
            " Hypertonicity is found in the ",
            " Thoracic spine palpation reveals increased muscle tone of the "        
        ]
        
        self.objective_trigger_thoracic = [
            " Palpatory examination of the thoracic musculature displays myofascial trigger points of the ",
            " Evaluation of the thoracic spinal areas indicates that trigger points are present in the ",
            " Palpation of the thoracic musculature reveals myofascial trigger points of the ",
            " Examination of the thoracic spine reveals myofascial trigger points of the ",
            " Palpation of the thoracic region indicates the presence of trigger points in the ",
            " Myofascial trigger points are palpated in the ",
            " Myofascial trigger points are present in the "
        ]
        
        self.objective_rom_thoracic = [
            " Examination of the thoracic spine revealed ROM has decreased.",
            " thoracic spine evaluation shows that range of motion has decreased.",
            " thoracic spine evaluation shows that ROM has deteriorated.",
            " Ranges of motion in the thoracic region have lowered.",
            " thoracic range of motion has decreased.",
            " thoracic region ROM has worsened."
        ]   
        
        self.objective_tender_lumbar = [
            " Palpation of the lumbar spine displayed tenderness in the spinous process at: ",
            " Palpation of the lumbar spine revealed tenderness at the following levels: ",
            " Examination of the lumbar region indicated discomfort and pain in the spinous process at: ",
            " Evaluation of the lumbar spinal areas showed discomfort to be present in the spinous process at: ",
            " Examination of the lumbar region indicated discomfort and pain in the spinous process at: ",
            " There is tenderness of the following lumbar spinous levels: ",
            " The spinous processes were tender on palpation at the following levels: ",
            " Lumbar spine palpation elicited tenderness of spinous process at ",
            " There was tenderness on the spinous process at: "
        ]
        
        self.objective_tone_lumbar = [
            " Palpation of the lumbar musculature demonstrates hypertonicity in the ",
            " Examination of the lumbar spine region indicates the presence of increased tonus in the ",
            " Evaluation of the lumbar spinal area shows hypertonicity in the ",
            " There is hypertonicity of the lumbar spinal area in the ",
            " Hypertonicity of the lumbar spine is palpable in the ",
            " Hypertonicity is palpable in the ",
            " Hypertonicity is found in the ",
            " Lumbar spine palpation reveals increased muscle tone of the "        
        ]
        
        self.objective_trigger_lumbar = [
            " Palpatory examination of the lumbar musculature displays myofascial trigger points of the ",
            " Evaluation of the lumbar spinal areas indicates that trigger points are present in the ",
            " Palpation of the lumbar musculature reveals myofascial trigger points of the ",
            " Examination of the lumbar spine reveals myofascial trigger points of the ",
            " Palpation of the lumbar region indicates the presence of trigger points in the ",
            " Myofascial trigger points are palpated in the ",
            " Myofascial trigger points are present in the "
        ]
        
        self.objective_rom_lumbar = [
            " Examination of the lumbar spine revealed ROM has decreased.",
            " Lumbar spine evaluation shows that range of motion has decreased.",
            " Lumbar spine evaluation shows that ROM has deteriorated.",
            " Ranges of motion in the lumbar region have lowered.",
            " Lumbar range of motion has decreased.",
            " Lumbar region ROM has worsened."
        ]   
        
        self.objective_test_pain = [
            " The patient complained of pain during testing.",
            " The patient reported pain during the performance of this test.",
            " The patient indicated that they felt discomfort and pain during the performance of this exam.",
            " The patient experienced pain during the execution of this test.",
            " The patient experienced discomfort during the execution of this test.",
            " Pain was elicited while performing this test."
        ]
        
        # ASSESSMENT sentence bank
        # TODO: if patient status got worse, prompt user to give a reason (else give vague, generated reasoning)
        self.assessment_status = [""]
        self.assessment_starter = [
            " Their ",
            " The patient's ",
        ]
        
        # PLAN sentence bank
        self.plan_sentences = [
            f"{self.patient.get_first_name()} should proceed with therapies as directed.",
            "Proceed with therapies as directed.",
            "Therapy will continue as directed.",
            "Proceed with therapies as stated earlier.",
            "Continue with therapies as directed.",
            f"Today's visit indicates that {self.patient.get_first_name()} should proceed with therapy as directed."
        ]

    # current_val = 8    # Starting point
    # target_val = 3     # The goal we want to trend toward
    # steps = 20          # Number of iterations

    # # target should ALWAYS be less than the current val (overall downwards trend is goal)
    # # only used for partial and full fill options
    # self._get_guaranteed_staircase_path(current_val, target_val, steps)
        
    # def _generate_ratings(self) -> dict[str, int]:
    #     # use a random function to generate believable ratings for each complaint
    #     # - we read the previous rating then use that as a starting point for random deviations
    #     # - target is guaranteed to be reached by the end of the last run
    #     # - overall health + pain will be measured based on no. complaints + severity of each complaint
        
    #     # for each complaint, generate a rating given start and end values
        
    #     return
    
    def _get_complaint_list(self) -> str:
        global target_ratings
        counter = 1    
        complaint_sentence = ""
        
        # check null
        if not target_ratings:
            raise ValueError("Target ratings is None")
        
        for complaint, rating in target_ratings.items():
            if complaint != "pain" and complaint != "health":
                complaint_sentence += f"{complaint} as a {rating}"
                
                # add comma, period or 'and' at the end
                if counter < len(target_ratings) - 3:
                    complaint_sentence += ", "
                elif counter == len(target_ratings) - 3:
                    complaint_sentence += " and "
                elif counter == len(target_ratings) - 2:
                    complaint_sentence += "."
                
                counter+=1
                
        return complaint_sentence


    def _convert_list_to_plain(self, input_list: list, has_period: bool) -> str:
        sentence = ""
        counter = 1    
        
        # check null
        if not input_list:
            raise ValueError("input_list is None")
        
        for element in input_list:
            sentence += f"{element}"
            
            # add comma, period or 'and' at the end
            if counter < len(input_list) - 1:
                sentence += ", "
            elif counter == len(input_list) - 1:
                sentence += " and "
            elif (counter == len(input_list) and has_period):
                sentence += "."
            
            counter+=1
                
        return sentence        
        
    
    def get_target_ratings(self) -> dict[str, int]:
        ratings_copy = self.patient.get_ratings().copy()
        total_pain = 0
        for complaint, rating in ratings_copy.items():
            getting_input = True
            if complaint != "pain" and complaint != "health":
                while getting_input:
                    user_input = input(f"Please enter a target rating for {complaint}, starting at {rating}: ")
                    if not re.fullmatch(r'[0-9]', user_input):
                        print("Invalid input, please enter a number in the range 0-9. Try again.")
                    else:
                        ratings_copy[complaint] = int(user_input)
                        
                        # higher pain ratings contribute more to the overall pain value
                        # can tweak this so that age/gender affects perceived pain values
                        bonus_pain_value = 0
                        if int(user_input) > 4 and len(ratings_copy) > 4:
                            bonus_pain_value += (len(ratings_copy)-4)
                        
                        total_pain += int(user_input) + bonus_pain_value # add up pain
                        getting_input = False
                
        # calculate pain and health and
        avg_pain = min(round(total_pain / (len(ratings_copy)-2)) + random.randint(0, 1), 10)
        health = max((RATING_CEILING - avg_pain) + random.randint(-1, 1), 0)
        
        ratings_copy["pain"] = avg_pain
        ratings_copy["health"] = health
        
        return ratings_copy
    
    
    def get_paragraph(self, section: int) -> str:
        global target_ratings, improving_complaints, unchanged_complaints, worsening_complaints
        
        # check for null
        if not target_ratings:
            raise ValueError("target_ratings is None")
        
        paragraph = ""
        if section == Sections.SUBJECTIVE.value:
            # append intro sentences
            paragraph += self.subjective_intro[random.randint(0, len(self.subjective_intro)-1)]
            paragraph += self.subjective_pain_intro[random.randint(0, len(self.subjective_pain_intro)-1)]
            
            # append overall pain rating from patient
            paragraph += self.subjective_overall_pain[random.randint(0, len(self.subjective_overall_pain)-1)]
            paragraph += f"{target_ratings['pain']}."
            
            # append health rating from patient
            paragraph += self.subjective_health[random.randint(0, len(self.subjective_health)-1)]
            paragraph += f"{target_ratings['health']}."
            
            # add improving, unchanged, worsening complaint sentence(s)
            # make lists to sort complaints based on whether it is improving/unchanged/worsening
            # compare starting and target ratings
            # - if difference is negative (starting < target), it is worsening
            # - if difference is equal (starting == target), it is unchanged
            # - if difference is positive (starting > target), it is improving
            for complaint, start_rating in self.patient.get_ratings().items():
                if complaint != "pain" and complaint != "health": 
                    target_rating = target_ratings[complaint] # get target rating
                    
                    # compare and sort
                    if start_rating > target_rating:
                        improving_complaints.append(complaint)
                    elif start_rating == target_rating:
                        unchanged_complaints.append(complaint)
                    else:
                        worsening_complaints.append(complaint)
        
            if improving_complaints:
                paragraph += self.subjective_assessment_improving[random.randint(0, len(self.subjective_assessment_improving)-1)]
                paragraph += self._convert_list_to_plain(improving_complaints, has_period=True)            
            
            if unchanged_complaints:
                paragraph += self.subjective_assessment_unchanged[random.randint(0, len(self.subjective_assessment_unchanged)-1)]
                paragraph += self._convert_list_to_plain(unchanged_complaints, has_period=True)            
            
            if worsening_complaints:
                paragraph += self.subjective_assessment_worsening[random.randint(0, len(self.subjective_assessment_worsening)-1)]
                paragraph += self._convert_list_to_plain(worsening_complaints, has_period=True)
            
            # append ratings from patient
            paragraph += self.subjective_ratings[random.randint(0, len(self.subjective_ratings)-1)]
            paragraph += self._get_complaint_list()
            
            return paragraph
        
        elif section == Sections.OBJECTIVE.value:
            # index 0 -> tone, 1 -> trigger, 2 -> rom, 3 -> pain
            
            # cervical region
            if self.sorted_sentences["sorted_cervical"][0]:
                
                # starting sentence
                paragraph += self.objective_tender_cervical[random.randint(0, len(self.objective_tender_cervical)-1)]
                paragraph += self._convert_list_to_plain(self.sorted_sentences["tender_cervical"], has_period=True)                
                paragraph += self.objective_tone_cervical[random.randint(0, len(self.objective_tone_cervical)-1)]
                
                # extract the list of affected areas, then append
                parts = re.split(r"\s+of the\s+|\s+in the\s+", self.sorted_sentences["sorted_cervical"][0], flags=re.IGNORECASE)
                affected_areas = parts[len(parts) - 1]
                paragraph += f"{affected_areas}."
                
            if self.sorted_sentences["sorted_cervical"][1]:
                paragraph += self.objective_trigger_cervical[random.randint(0, len(self.objective_trigger_cervical)-1)]
                parts = re.split(r"\s+of the\s+|\s+in the\s+", self.sorted_sentences["sorted_cervical"][1], flags=re.IGNORECASE)
                affected_areas = parts[len(parts) - 1]
                paragraph += f"{affected_areas}."
            if self.sorted_sentences["sorted_cervical"][2]:
                paragraph += self.objective_rom_cervical[random.randint(0, len(self.objective_rom_cervical)-1)]
            if self.sorted_sentences["sorted_cervical"][3]:
                paragraph += self.objective_test_pain[random.randint(0, len(self.objective_test_pain)-1)]    
                
            # thoracic region
            if self.sorted_sentences["sorted_thoracic"][0]:
                paragraph += self.objective_tender_thoracic[random.randint(0, len(self.objective_tender_thoracic)-1)]
                paragraph += self._convert_list_to_plain(self.sorted_sentences["tender_thoracic"], has_period=True)                
                paragraph += self.objective_tone_thoracic[random.randint(0, len(self.objective_tone_thoracic)-1)]
                parts = re.split(r"\s+of the\s+|\s+in the\s+", self.sorted_sentences["sorted_thoracic"][0], flags=re.IGNORECASE)
                affected_areas = parts[len(parts) - 1]
                paragraph += f"{affected_areas}."
            if self.sorted_sentences["sorted_thoracic"][1]:
                paragraph += self.objective_trigger_thoracic[random.randint(0, len(self.objective_trigger_thoracic)-1)]
                parts = re.split(r"\s+of the\s+|\s+in the\s+", self.sorted_sentences["sorted_thoracic"][1], flags=re.IGNORECASE)
                affected_areas = parts[len(parts) - 1]
                paragraph += f"{affected_areas}."
            if self.sorted_sentences["sorted_thoracic"][2]:
                paragraph += self.objective_rom_thoracic[random.randint(0, len(self.objective_rom_thoracic)-1)]
            if self.sorted_sentences["sorted_thoracic"][3]:
                paragraph += self.objective_test_pain[random.randint(0, len(self.objective_test_pain)-1)]
            
            # lumbar region
            if self.sorted_sentences["sorted_lumbar"][0]:
                paragraph += self.objective_tender_lumbar[random.randint(0, len(self.objective_tender_lumbar)-1)]
                paragraph += self._convert_list_to_plain(self.sorted_sentences["tender_lumbar"], has_period=True)                     
                paragraph += self.objective_tone_lumbar[random.randint(0, len(self.objective_tone_lumbar)-1)]
                parts = re.split(r"\s+of the\s+|\s+in the\s+", self.sorted_sentences["sorted_lumbar"][0], flags=re.IGNORECASE)
                affected_areas = parts[len(parts) - 1]
                paragraph += f"{affected_areas}."
            if self.sorted_sentences["sorted_lumbar"][1]:
                paragraph += self.objective_trigger_lumbar[random.randint(0, len(self.objective_trigger_lumbar)-1)]
                parts = re.split(r"\s+of the\s+|\s+in the\s+", self.sorted_sentences["sorted_lumbar"][1], flags=re.IGNORECASE)
                affected_areas = parts[len(parts) - 1]
                paragraph += f"{affected_areas}."
            if self.sorted_sentences["sorted_lumbar"][2]:
                paragraph += self.objective_rom_lumbar[random.randint(0, len(self.objective_rom_lumbar)-1)]
            if self.sorted_sentences["sorted_lumbar"][3]:
                paragraph += self.objective_test_pain[random.randint(0, len(self.objective_test_pain)-1)]                
            
            return paragraph
        
        elif section == Sections.ASSESSMENT.value:
            global overall_assessment
            start_rating = self.patient.get_ratings()["health"]
            target_rating = target_ratings["health"] # get target rating
            
            if abs(start_rating - target_rating) > 1:
                overall_assessment += "has moderately "
            elif abs(start_rating - target_rating) == 1:
                overall_assessment += "has mildly "
            
            # compare ratings
            if start_rating > target_rating: # getting worse
                overall_assessment += "worsened"
            elif start_rating == target_rating: # unchanged
                overall_assessment += "is unchanged"
            else: # getting better
                overall_assessment += "improved"
                
            # this is messy, definitely rework this later
            self.assessment_status = [
                f"The patient's overall status {overall_assessment} since the last visit.",
                f"Overall assessment of the patient's condition {overall_assessment} since the last visit.",
                f"Overall, the patient's condition {overall_assessment} since the last visit.",
                f"The patient's overall condition {overall_assessment} since the last visit.",
                f"The patient's condition {overall_assessment} since their last visit."
            ] 
                        
            paragraph += self.assessment_status[random.randint(0, len(self.assessment_status)-1)]
            if improving_complaints:
                paragraph += f"{self.assessment_starter[random.randint(0, len(self.assessment_starter)-1)]}{self._convert_list_to_plain(improving_complaints, has_period=False)} is determined to have improved."
            if unchanged_complaints:
                paragraph += f"{self.assessment_starter[random.randint(0, len(self.assessment_starter)-1)]}{self._convert_list_to_plain(unchanged_complaints, has_period=False)} is determined to be unchanged."
            if worsening_complaints:
                paragraph += f"{self.assessment_starter[random.randint(0, len(self.assessment_starter)-1)]}{self._convert_list_to_plain(worsening_complaints, has_period=False)} is determined to have worsened."
            
            return paragraph
        
        elif section == Sections.PLAN.value:
            paragraph += self.plan_sentences[random.randint(0, len(self.plan_sentences)-1)]
            return paragraph
        
        raise ValueError(f"'{section}' is not a valid section id")