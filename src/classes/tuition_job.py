from .suitable_tutor import SuitableTutor
from .tuition_channel import TuitionChannel



class TuitionJob():

    # Basic constructor. Called by details_extractor.py
    def __init__(
            self, 
            message:str, 
            address:str, 

            subjects:set[str], # must have AT LEAST ONE subject
            subject_levels:set[str], 
            experience:set[str], # most jobs have multiple tutor experience levels for price ranges

            gender_preference:set[str], # Will default to all genders if none specified during detail extraction
            suitable_tutors:list[SuitableTutor],
            tuition_channel:TuitionChannel):
        
        self.message:str = message # store original message
        self.address:str = address
        self.subjects:set[str] = subjects
        self.subject_levels:set[str] = subject_levels
        self.experience:set[str] = experience
        self.gender_preference:set[str] = gender_preference

        self.suitable_tutors:list[SuitableTutor] = suitable_tutors
        self.tuition_channel:TuitionChannel = tuition_channel

    def to_string(self):
        print(f"Address: {self.address}")
        print(f"Subjects: {self.subjects}")
        print(f"Subject levels: {self.subject_levels}")
        print(f"Experience: {self.experience}")
        print(f"Gender preferences: {self.gender_preference}")
        print(f"Suitable tutors: {self.suitable_tutors}")
        print(f"Tuition Channel: {self.tuition_channel}")
        