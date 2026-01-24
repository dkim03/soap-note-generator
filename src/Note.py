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
from enum import Enum
from Patient import Patient

class Sections(Enum):
    SUBJECTIVE = 0
    OBJECTIVE = 1
    ASSESSMENT = 2

class Note:
    def __init__(self, patient: Patient):
        self.patient = patient    
        
        # SUBJECTIVE
        # 1st sentence
        self.subjective_intro = [
            f"{self.patient.get_formal_name()} was evaluated today to determine progress and response to the current treatment plan.",
            f"{self.patient.get_formal_name()} was evaluated today to assess {self.patient.get_pronoun_possessive()} response to care.",
            f"{self.patient.get_formal_name()} was evaluated today for progress and response to treatment.",
            f"{self.patient.get_formal_name()} was checked for {self.patient.get_pronoun_possessive()} responsiveness to the treatment plan.",
            f"{self.patient.get_formal_name()} was assessed today for progress and response to the plan of care.",
            f"{self.patient.get_formal_name()} was examined today to determine progress with the current treatment plan.",
            f"{self.patient.get_formal_name()}'s overall response to the treatment plan was evaluated today."
        ]

        # 2nd sentence
        self.subjective_pain_intro = [
            f" The following are the patient's subjective response to questions regarding {self.patient.get_pronoun_possessive()} pain levels: ",
            " The patient's subjective response to a question regarding pain levels: ",
            f" The patient was asked about {self.patient.get_pronoun_possessive()} pain levels which {self.patient.get_pronoun()} rated as follows: ",
            " The patient's subjective responses to questions are as follows in regards to pain levels: ",
            f" The patient rated {self.patient.get_pronoun_possessive()} overall pain level today on a scale of 0 (no pain) to 10 (excruciating pain). ",
            f" The patient was questioned about {self.patient.get_pronoun_possessive()} pain scale: ",
            f" The patient was asked subjective questions regarding {self.patient.get_pronoun_possessive()} pain levels: "
        ]
        
        # 3rd sentence
        self.subjective_overall_pain = [
            " Overall pain level today on a scale of 0 (no pain) to 10 (excruciating pain) is considered a ",
            " Current pain level today on a scale of 0 (no pain) to 10 (unbearable pain) is considered a ",
            f" {self.patient.get_pronoun_possessive()} pain level today on a scale of 0 (no pain) to 10 (unbearable pain) is reported to be ",
            f" The patient rated {self.patient.get_pronoun_possessive()} overall pain level today on a scale of 0 (no pain) to 10 (excruciating pain). The patient said {self.patient.get_pronoun_possessive()} pain level can be considered a ",
            f" General pain level today, on a scale of 0 (no pain) to 10 (unbearable pain), is evaluated as "
        ]
        
        # 4th sentence
        self.subjective_health = [
            f" The patient rated {self.patient.get_pronoun_possessive()} overall health on a scale of 1 to 10 as a ",
            f" The patient reported that {self.patient.get_pronoun_possessive()} overall health on a scale of 1 to 10 is rated as a ",
            " The patient's general health was rated on a scale of 1 to 10 is as ",
            " Overall health on a scale of 1 to 10 is rated as ",
            " Current health on a scale of 1 to 10 is rated a "
        ]
        
        # optional sentence(s)
        # - improving, unchanging, worsening complaints (this depends on generated ratings)
        
        # 5th sentence
        self.subjective_ratings = [
            f" On a scale of 0 to 10 with 10 being the worst, {self.patient.get_pronoun()} rated {self.patient.get_pronoun_possessive()} "
        ]
        
        # OBJECTIVE
        # 1st sentence
        self.objective_tender_cervical = [
            "Palpation of the cervical spine displayed tenderness in the spinous process at: ",
            "Palpation of the cervical spine revealed tenderness at the following levels: ",
            "Examination of the cervical region indicated discomfort and pain in the spinous process at: ",
            "Evaluation of the cervical spinal areas showed discomfort to be present in the spinous process at: ",
            "Examination of the cervical region indicated discomfort and pain in the spinous process at: ",
            "There is tenderness of the following cervical spinous levels: ",
            "Cervical spine tenderness was noted in the spinous process region at: ",
            "Cervical spine palpation elicited tenderness of spinous process at "
        ]
        
        # 2nd sentence
        self.objective_tone_cervical = [
            " Palpation of the cervical musculature demonstrates hypertonicity in the ",
            " Examination of the cervical spine region indicates the presence of increased tonus in the ",
            " Evaluation of the cervical spinal area shows hypertonicity in the ",
            " There is hypertonicity of the ",
            " Hypertonicity is palpable in the ",
            " Hypertonicity is found in the ",
            " Cervical spine palpation reveals increased muscle tone of the "
        ]
        
        # 3rd sentence
        self.objective_trigger_cervical = [
            " Palpatory examination of the cervical musculature displays myofascial trigger points of the ",
            " Palpation of the cervical musculature reveals myofascial trigger points of the ",
            " Examination of the cervical spine reveals myofascial trigger points of the ",
            " Palpation of the cervical region indicates the presence of trigger points in the ",
            " Myofascial trigger points are palpated in the ",
            " Myofascial trigger points are present in the "
        ]
        
        # 4th sentence
        self.objective_rom_cervical = [
            " Examination of the cervical spine revealed the ROM has ",
            " Cervical spine evaluation shows that the range of motion has ",
            " Cervical spine evaluation shows that the ROM has ",
            " Ranges of motion in the cervical region have ",
            " Cervical range of motion has ",
            " Cervical spine ROM has "
        ]
        
        # optional sentence
        # test pain
        self.objective_cervical_test_pain = [
            " The patient complained of pain during testing.",
            " The patient reported pain during the performance of this test.",
            " The patient experienced pain during the execution of this test.",
            " The patient indicated that they felt discomfort and pain during the performance of this exam.",
            " The patient experienced discomfort during the execution of this test.",
            " Pain was elicited while performing this test."
        ]
        
        # 5th sentence
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
        
        # 6th sentence
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
        
        # 7th sentence
        self.objective_trigger_lumbar = [
            " Palpatory examination of the lumbar musculature displays myofascial trigger points of the ",
            " Evaluation of the lumbar spinal areas indicates that trigger points are present in the ",
            " Palpation of the lumbar musculature reveals myofascial trigger points of the ",
            " Examination of the lumbar spine reveals myofascial trigger points of the ",
            " Palpation of the lumbar region indicates the presence of trigger points in the ",
            " Myofascial trigger points are palpated in the ",
            " Myofascial trigger points are present in the "
        ]
        
        # 8th sentence
        self.objective_rom_lumbar = [
            " Examination of the lumbar spine revealed the ROM has ",
            " Lumbar spine evaluation shows that the range of motion has ",
            " Lumbar spine evaluation shows that the ROM has ",
            " Ranges of motion in the lumbar region have ",
            " Lumbar range of motion has ",
            " Lumbar region ROM has "
        ]   
        
        # optional sentence
        # test pain
        self.objective_lumbar_test_pain = [
            " The patient complained of pain during testing.",
            " The patient reported pain during the performance of this test.",
            " The patient experienced pain during the execution of this test.",
            " The patient indicated that they felt discomfort and pain during the performance of this exam.",
            " The patient experienced discomfort during the execution of this test.",
            " Pain was elicited while performing this test."
        ]
        
        # ASSESSMENT
        # 1st sentence
        # if patient status got worse, prompt user to give a reason (else give vague, generated reasoning)
        self.assessment_status = [
            "The patient's overall status has mildly improved since the last visit.",
            "Overall assessment of the patient's condition is considered to be mildly improved since the last visit.",
            "Overall the patient's condition is mildly improved since the last visit.",
            "The patient's overall condition is considered to be mildly improved since the last visit.",
            "The patient's condition has gotten moderately worse since their last visit."
        ] 
        
        # 2nd sentence
        # - improving, unchanging, worsening complaints (this depends on generated ratings)
        
    
    def get_paragraph(self, section: int) -> str:
        paragraph = ""
        if section is Sections.SUBJECTIVE.value:
            # return subjective paragraph
            # # add section header
            # r.par(f"Subjective Complaint", style="s28")
            # r.par(f"This is the first sentence.", style="s21")
            
            # append intro sentences
            paragraph += self.subjective_intro[random.randint(0, len(self.subjective_intro)-1)]
            paragraph += self.subjective_pain_intro[random.randint(0, len(self.subjective_pain_intro)-1)]
            
            # append overall pain rating from patient
            paragraph += self.subjective_overall_pain[random.randint(0, len(self.subjective_overall_pain)-1)]
            paragraph += f"{self.patient.ratings.get_ratings()['pain']}."
            
            # append health rating from patient
            paragraph += self.subjective_health[random.randint(0, len(self.subjective_health)-1)]
            paragraph += f"{self.patient.ratings.get_ratings()['health']}."
            
            # add improving, unchanging, worsening complaint sentence(s) here...
            
            # append ratings from patient
            paragraph += self.subjective_ratings[random.randint(0, len(self.subjective_ratings)-1)]
            
            return paragraph
        elif section is Sections.OBJECTIVE.value:
            # return objective paragraph
            return ""
        elif section is Sections.ASSESSMENT.value:
            # return assessment paragraph
            return ""
        
        raise ValueError(f"'{section}' is not a valid section id")