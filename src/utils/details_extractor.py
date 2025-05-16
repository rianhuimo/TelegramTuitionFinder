import re
from classes.TuitionChannel import TUITION_CHANNEL_LIST, TuitionChannel
from classes.TuitionJob import *
from classes import Tutor


def create_tuition_job(message:str, channel_name:str) -> TuitionJob:
        # using the name of the tuition channel that this message was from, 
        # get the TuitionChannel object, and use that as regex reference when extracting the details of the job.
        tuition_channel:TuitionChannel = None
        for channel in TUITION_CHANNEL_LIST:
            if channel_name == channel.channel_name:
                tuition_channel = channel
                break
        if tuition_channel != None:
            # extract details with given regex. each detail extracted uses a specific function from the details_extractor.py tools file
            print(f"\nFound tuition channel: {tuition_channel.channel_name}")

            # Address
            address:str = extract_address(message,tuition_channel.address_regex).strip()
            
            # Subjects
            subjects:list[str] = extract_subjects(message,tuition_channel.subjects_regex)

            # Subject levels
            subject_levels:list[str] = extract_subject_levels(message,tuition_channel.subject_levels_regex)

            # Experience 
            # Note that some messages might match in multiple areas. Requires joining into a string?
            experience:list[int] = extract_experience(message,tuition_channel.experience_regex)

            # Gender Preference
            gender_preference:str = extract_gender_preference(message,tuition_channel.gender_preference_regex)

            
        else:
            print("⚠️ Error: No tuition channel found for this message.")
        pass

def extract_address(message:str,address_regex:str) -> str:
    address = None
    try:
        # extract address
        address:str = " ".join(re.findall(address_regex,message)).strip()
        if "online" in address:
            print("🌐 Job is Online")
            address = Tutor.ONLINE_TUITION
        elif address == "":
            print(f"⚠️ No address was found: {address}")
            address = None
        else:
            print(f"Address extracted: {address}")
            # TODO: Use LLM Extraction as backup?
        return address
    except Exception as e:
        print(f"Error occured while extracting address: {e}")
        return address

def extract_subjects(message:str,subjects_regex:str) -> list[str]:
    subjects = None
    try:
        subjects:list[str] = re.findall(subjects_regex,message)
        if len(subjects) > 0:
            print(f"Subjects found: {[subject for subject in subjects]}")
        else:
            print(f"⚠️ No subjects found: {subjects}")
            # TODO: Use LLM Extraction as backup?
        return subjects
    except Exception as e:
        print(f"Error occured while extracting subjects: {e}")
        return subjects
    
def extract_subject_levels(message:str,subject_levels_regex:str):
    pass

def extract_experience(message:str,experience_regex:str):
    pass

def extract_gender_preference(message:str,gender_preference_regex:str):
    pass

if __name__ == "__main__":
    print(f"Hello from {__package__}!")
    variable = None
    if (variable): print("yes")
    else: print("no")

    subjects = [Tutor.ENGLISH,Tutor.CHINESE,Tutor.SCIENCE]
    print(f"Subjects found: {[subject for subject in subjects]}")

