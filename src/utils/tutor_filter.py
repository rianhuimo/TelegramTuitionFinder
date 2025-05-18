from classes.tuition_job import TuitionJob
import classes.tutor as Tutor
from classes.suitable_tutor import SuitableTutor
from utils.directions_api import get_directions

def find_suitable_tutors(job:TuitionJob) -> list[SuitableTutor]:

    # Strategy: If the tutor passes all the checks, it will get to the end of the for loop where it will be added to the list
    suitable_tutors:list[SuitableTutor] = []

    for tutor in Tutor.TUTOR_LIST:
        print(f"\nEvaluating job for {tutor.telegram_handle}:")
        # Calculate commute
        if job.address == Tutor.ONLINE_TUITION: # If the job is online, return an appropriate fastest_commute value of 0 mins
            fastest_commute = { "text": "0 mins", "value": 0 }
            print(f"✅ Job is online")
        elif job.address is None: continue # This usually occurs for compilation-style tuition job messages. For the purpose of this program, I will not be broadcasting them.
        else    : # if the job has a physical address
            if tutor.address == Tutor.ONLINE_TUITION: 
                print(f"❌ Tutor is online only, but job has physical address")
                continue # if the tutor is online only, skip this tutor entirely as it is incompatible.

            fastest_commute:dict = get_directions(
                job_address=job.address,
                tutor_address=tutor.address,
                commute_method=tutor.commute_method)[0]["legs"][0]["duration"]
            
            if fastest_commute['value'] > tutor.max_commute_time*60: 
                print(f"❌ Fastest commute from {tutor.telegram_handle}'s house: {fastest_commute['text']}. Exceeds tutor's max commute of {tutor.max_commute_time} mins")
                # If commute time exceeds tutor's maximum, skip it. Max commute time is given in minutes
                continue
            print(f"✅ Fastest commute from {tutor.telegram_handle}'s house: {fastest_commute['text']}. Within tutor's max commute of {tutor.max_commute_time} mins")
        # Commute check passed

        # Match subjects - subset
        subject_match:bool = job.subjects.issubset(tutor.subjects)
        if subject_match:
            print(f"✅ Subjects matched with tutor: {job.subjects}. Tutor's teachable subjects: {tutor.subjects}")
        else:
            print(f"❌ No match for subjects: {job.subjects}. Tutor's teachable subjects: {tutor.subjects}")
            continue

        # Match subject levels - subset
        subject_levels_match:bool = job.subject_levels.issubset(tutor.subject_levels)
        if subject_levels_match:
            print(f"✅ Subject level matched with tutor: {job.subject_levels}. Tutor's teachable subject levels: {tutor.subject_levels}")
        else:
            print(f"❌ No match for subject level: {job.subject_levels}. Tutor's teachable subject levels: {tutor.subject_levels}")
            continue

        # Match experience - intersection
        experience_match:set = job.experience.intersection(tutor.experience)
        if len(experience_match) > 0:
            print(f"✅ Experience matched with tutor's experience: {job.experience}. Tutor's teaching experience: {tutor.experience}")
        else:
            print(f"❌ No match for experience required: {job.experience}. Tutor's teaching experience: {tutor.experience}")
            continue

        # Match gender - but it will not be a stored variable in SuitableTutor, as it inherits Tutor and already has it's value
        gender_match:set = job.gender_preference.intersection(tutor.gender)
        if len(gender_match) > 0:
            print(f"✅ Gender preferences align with tutor's gender: {gender_match}. Tutor's gender: {tutor.gender}")
        else:
            print(f"❌ Gender preferences do not align with tutor's gender: {job.gender_preference}. Tutor's gender: {tutor.gender}")
            continue

        suitable_tutor = SuitableTutor(tutor=tutor,subjects_match=job.subjects,
            subject_levels_match=job.subject_levels,experience_match=experience_match,fastest_commute=fastest_commute)

        # Tutor is deemed suitable. Add them to the list
        suitable_tutors.append(suitable_tutor)

    return suitable_tutors