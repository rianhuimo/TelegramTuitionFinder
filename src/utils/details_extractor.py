import re
from classes.tuition_channel import TUITION_CHANNEL_LIST, TuitionChannel
from classes.tuition_job import *
from classes.tutor import *


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
        address:str = extract_address(message,tuition_channel.address_regex)
        if address != None: address = address.strip()
        
        # Subjects
        subjects:set[str] = extract_subjects(message,tuition_channel.subjects_regex)

        # Subject levels
        subject_levels:set[str] = extract_subject_levels(message,tuition_channel.subject_levels_regex)

        # Experience
        # Note that some messages might match in multiple areas. Requires joining into a string?
        experience:set[str] = extract_experience(message,tuition_channel.experience_regex)

        # Gender Preference
        gender_preference:set[str] = extract_gender_preference(message,tuition_channel.gender_preference_regex)

        job = TuitionJob(
            message=message,
            address=address,
            subjects=subjects,
            subject_levels=subject_levels,
            experience=experience,
            gender_preference=gender_preference,
            suitable_tutors=[],
            tuition_channel=tuition_channel,
        )

        return job
    else:
        print("⛔ Error: No tuition channel found for this message.")
        return None

def extract_address(message:str,address_regex:str) -> str:
    address = None
    try:
        # extract address
        address:str = " ".join(re.findall(address_regex,message,flags=re.IGNORECASE)).strip()
        if "online" in address.lower():
            print("🌐 Job is Online")
            address = ONLINE_TUITION.regex_pattern
        elif address == "":
            print(f"⚠️ No address was found: {address}. Regex output: {re.findall(address_regex,message,flags=re.IGNORECASE)}")
            address = None
        else:
            print(f"👁️ Address extracted: {address}")
            # TODO: Use LLM Extraction as backup?
        return address
    except Exception as e:
        print(f"⛔ Error occured while extracting address: {e}. Error on line {e.__traceback__.tb_lineno}")
        return address

def extract_subjects(message:str,subjects_regex:str) -> set[str]:
    subjects:set[str] = set()
    try:
        # extract the part of the message that contains the subject. this is NOT the end result thought, as it is just the raw message
        raw_extracted_string:list[str] = " ".join("".join(match) for match in re.findall(subjects_regex,message,flags=re.IGNORECASE)).lower()

        # check this stream of words against EVERY subject's regex pattern. Find a match, or even, multiple matches of a subject.
        for subject in ALL_SUBJECTS:
            subject_match = re.findall(subject.regex_pattern,raw_extracted_string,flags=re.IGNORECASE)
            if len(subject_match) > 0:
                subjects.add(subject.regex_pattern)

        if len(subjects) > 0:
            print(f"👁️ Subjects found: {subjects}. Raw string: {raw_extracted_string}")
        else:
            print(f"⚠️ No subjects found: {subjects}. Raw string: {raw_extracted_string}")
            # TODO: Use LLM Extraction as backup?
        return subjects
    except Exception as e:
        print(f"⛔ Error occured while extracting subjects: {e}. Error on line {e.__traceback__.tb_lineno}")
        return set([subject.regex_pattern for subject in ALL_SUBJECTS]) # Return a false positive 
    
def extract_subject_levels(message:str,subject_levels_regex:str) -> set[str]:
    subject_levels:set[str] = set()
    try:
        # extract the part of the message that contains the subject levels. this is NOT the end result thought, as it is just the raw message
        raw_extracted_string = " ".join("".join(match) for match in re.findall(subject_levels_regex,message,flags=re.IGNORECASE)).lower()

        # Iterate through all the subject levels possible, and find matches within the raw string.
        # If found simply add the level to the set
        for level in ALL_SUBJECT_LEVELS:
            # I have to use regex as the subject levels are often loosely typed
            level_match = re.findall(level.regex_pattern,raw_extracted_string,flags=re.IGNORECASE)
            if len(level_match) > 0: 
                subject_levels.add(level.regex_pattern) # easy and compact implemmentation? wew...
                # print(f"Found a level: {level_match}")

        if len(subject_levels) > 0:
            print(f"👁️ Subjects levels found: {subject_levels}. Raw string: {raw_extracted_string}")
        else:
            print(f"⚠️ No subjects levels found: {subject_levels}. Raw string: {raw_extracted_string}")
            # TODO: Use LLM Extraction as backup?
        return subject_levels

    except Exception as e:
        print(f"⛔ Error occured while extracting subject levels: {e}. Error on line {e.__traceback__.tb_lineno}")
        return set([level.regex_pattern for level in ALL_SUBJECT_LEVELS]) # Return a false positive 
    
def extract_experience(message:str,experience_regex:str) -> set[str]:
    # special function I'm coding: accommodate for scenarios where the requirement says "xx position and ABOVE"
    # E.g. Full-time and ABOVE -> Experience >= 2 -> EXPERIENCE[1:]
    experience_required:set[str] = set()
    try:
        # Extract the part of the message where the tutor's experience is stated. Join the regex matches together into a single lowercased string
        raw_extracted_string = " ".join("".join(match) for match in re.findall(experience_regex,message,flags=re.IGNORECASE)).lower()

        # Parse the contents of the string to get the experience levels specified
        for experience_constant in ALL_TUTOR_EXPERIENCES_RANKED:
            found_experience = re.findall(experience_constant.regex_pattern,raw_extracted_string,flags=re.IGNORECASE)
            if len(found_experience) > 0:
                print(f"Extracted experience from raw message: {found_experience}. Adding \"{experience_constant.regex_pattern}\" to the list.")
                experience_required.add(experience_constant.regex_pattern)

        # Additionally, if the message specifies the word "above", using the highest experience level extracted as reference, 
        # include all experience levels that are higher than level
        # E.g. "Full time and above" -> [GRADUATE_OR_FULL_TIME] -> (add in the levels above it) -> [GRADUATE_OR_FULL_TIME,EX_CURRENT_MOE]
        # E.g. "Student tutor and above" -> [STUDENT_OR_PART_TIME] -> [STUDENT_OR_PART_TIME,GRADUATE_OR_FULL_TIME,EX_CURRENT_MOE]
        if "above" in raw_extracted_string.lower():
            # of course, I can only do this if an experience level is extracted
            if len(experience_required) > 0:
                # start from the highest rank, and work my way down to the lowest.
                highest_level_index = len(ALL_TUTOR_EXPERIENCES_RANKED) - 1
                for experience in experience_required:
                    print(f"ex is {experience}")
                    index = [x.regex_pattern for x in ALL_TUTOR_EXPERIENCES_RANKED].index(experience)
                    highest_level_index = min(highest_level_index, index)
                # Add in all levels above to the set.
                experience_required.update([experience.regex_pattern for experience in ALL_TUTOR_EXPERIENCES_RANKED[highest_level_index:]])

        if (len(experience_required) > 0): 
            print(f"👁️ Extracted these experience levels: {experience_required}. Raw string: {raw_extracted_string}")
        else: 
            print(f"⚠️ No experience levels were extracted. Raw string: {raw_extracted_string}")
            experience_required = set([experience.regex_pattern for experience in ALL_TUTOR_EXPERIENCES_RANKED]) # just give back everything then
        return experience_required
    except Exception as e:
        print(f'⛔ Error occured while extracting experience: {e}. Error on line {e.__traceback__.tb_lineno}')
        return set([experience.regex_pattern for experience in ALL_TUTOR_EXPERIENCES_RANKED]) # Provide a false positive

def extract_gender_preference(message:str,gender_preference_regex:str) -> set[str]:
    # default gender preference is EVERYTHING (if no preference is stated)
    gender_preference = set()
    try:
        raw_extracted_string = "No gender_preference_regex provided" if gender_preference_regex is None else "this value should be overwritten"
        if gender_preference_regex is not None:
            # Extract the part of the message where the tutor's gender is stated. Join the regex matches together into a single lowercased string
            raw_extracted_string = " ".join("".join(match) for match in re.findall(gender_preference_regex,message,flags=re.IGNORECASE)).lower()
            gender_match = re.findall("|".join([gender.regex_pattern for gender in ALL_GENDERS]),raw_extracted_string)
            if len(gender_match) > 0:
                for gender in ALL_GENDERS:
                    if gender.regex_pattern in gender_match: gender_preference.add(gender.regex_pattern)

        if len(gender_preference) > 0: 
            print(f"👁️ Extracted a gender preference: {gender_preference}. Raw string: {raw_extracted_string}")
            return gender_preference
        print(f"🚻 No preference indicated. Returning all genders: {set([gender.regex_pattern for gender in ALL_GENDERS])}. Raw string: {raw_extracted_string}")
        return set([gender.regex_pattern for gender in ALL_GENDERS])
    except Exception as e:
        print(f'⛔ Error occured while extracting gender preference: {e}. Error on line {e.__traceback__.tb_lineno}')
        return set([gender.regex_pattern for gender in ALL_GENDERS]) # Provide a false positive

if __name__ == "__main__":
    print(f"Hello from {__package__}!")
    variable = None
    if (variable): 
        print("yes")
    else: 
        print("no")

    subjects = [Tutor.ENGLISH,Tutor.CHINESE,Tutor.SCIENCE]
    print(f"Subjects found: {[subject for subject in subjects]}")
    


