import json
import re
from pysondb import db
from telethon import Button, TelegramClient, events, types, tl
from classes.tutor import * # get all those juicy constants

# Contains all CRUD functions that the bot performs
def search(telegram_handle:str) -> object:
    database = db.getDb("tutors.json")
    result = database.getBy({"telegram_handle": telegram_handle})
    if len(result) > 0:
        return result[0] # There should be only one object anyways
    else:
        return None # return None if the tutor is not found

def delete(telegram_handle:str):
    database = db.getDb("tutors.json")
    result = database.getBy({"telegram_handle": telegram_handle})
    if len(result) > 0:
        tutor = result[0]
        database.deleteById(tutor["id"])
    else:
        print(f"⛔ Error: Delete function called when {telegram_handle} does not exist in database.")

async def create(telegram_handle:str):
    tutors = db.getDb("tutors.json")
    session = await get_session(telegram_handle=telegram_handle)
    tutors.add({
            "name":session["name"],
            "telegram_handle":session["telegram_handle"],

            # Note: these sets have to be stored as an array of strings in json. 
            # When creating Tutor objects, I require converting them back into set variables (that's okay)
            "subjects":session["subjects"],
            "experience":session["experience"],
            "subject_levels":session["subject_levels"],

            "address":session["address"],
            "gender":session["gender"],
            "commute_method":session["commute_method"],
            "max_commute_time":session["max_commute_time"],
        })
    print(f"✅ {telegram_handle} added to tutor database.")

async def update(telegram_handle:str,tutor_id:int):
    tutors = db.getDb("tutors.json")
    session = await get_session(telegram_handle=telegram_handle)
    tutors.updateById(tutor_id,{
            "name":session["name"],
            "telegram_handle":session["telegram_handle"],

            # Note: these sets have to be stored as an array of strings in json. 
            # When creating Tutor objects, I require converting them back into set variables (that's okay)
            "subjects":session["subjects"],
            "experience":session["experience"],
            "subject_levels":session["subject_levels"],

            "address":session["address"],
            "gender":session["gender"],
            "commute_method":session["commute_method"],
            "max_commute_time":session["max_commute_time"],
        })
    print(f"✅ {telegram_handle} updated within tutor database.")
    
# I will get rid of this function as I would like to simply use the bot interaction - provided that i coded it properly and its working...
def seed_data(event:events.newmessage.NewMessage.Event,tuition_finder_bot):
    # Give my JSON database some initial data (i.e. me and my mum's info)
    tutors = db.getDb("tutors.json")
    message = ""

    # But first, check if mum and I already exist
    rian = tutors.reSearch("telegram_handle","@rianhuii")
    if len(rian) > 0:
        message += "@rianhuii already exists. Skipping...\n"
    else:
        tutors.add({
            "name":"Rian 🪴",
            "telegram_handle":"@rianhuii",

            # Note: these sets have to be stored as an array of strings in json. 
            # When creating Tutor objects, I require converting them back into set variables (that's okay)
            "subjects":[MATH,SCIENCE,PHYSICS,CHEMISTRY,COMPUTING],
            "experience":[GRADUATE_OR_FULL_TIME],
            "subject_levels":[SECONDARY_LEVEL,POLYTECHNIC_LEVEL],

            "address":"40B Margaret Drive",
            "gender":[MALE],
            "commute_method":PUBLIC_TRANSPORT,
            "max_commute_time":40,
        })
        message += "@rianhuii added to database\n"

    mum = tutors.reSearch("telegram_handle","@Nekotokuma")
    if len(mum) > 0:
        message += "@Nekotokuma already exists. Skipping...\n"
    else:
        tutors.add({
            "name":"Mum 🌸",
            "telegram_handle":"@Nekotokuma",

            # Note: these sets have to be stored as an array of strings in json. 
            # When creating Tutor objects, I require converting them back into set variables (that's okay)
            "subjects":[ENGLISH,SCIENCE],
            "experience":[EX_CURRENT_MOE],
            "subject_levels":[PRIMARY_LEVEL,SECONDARY_LEVEL],

            "address":"40B Margaret Drive",
            "gender":[FEMALE],
            "commute_method":PUBLIC_TRANSPORT,
            "max_commute_time":40,
        })
        message += "@Nekotokuma added to database\n"

async def create_session(telegram_handle:str):
    # If session does not exist, create a new one for that user
    print(f"📱 Session with {telegram_handle} does not exist yet. Creating one...")
    db_session = db.getDb("sessions.json")

    # check if tutor exists
    result = search(telegram_handle)
    profile_found = result is not None

    # if the profile exists, create the session with its properties
    if profile_found:
        session = {
            "name":result["name"],
            "telegram_handle":telegram_handle,
            "action":"create_profile",
            # This is a simple integer counter that increments as the user goes through the steps of profile creation
            "progress":0,

            # The rest of the tutor properties - filled in with the tutor's existing data
            "subjects": result["subjects"],
            "experience": result["experience"],
            "subject_levels": result["subject_levels"],
            "address": result["address"],
            "gender": result["gender"],
            "commute_method": result["commute_method"],
            "max_commute_time": result["max_commute_time"],
        }
    else:
        session = {
            "name":"tutor_name",
            "telegram_handle":telegram_handle,
            "action":"create_profile",
            # This is a simple integer counter that increments as the user goes through the steps of profile creation
            "progress":0,

            # The rest of the tutor properties - filled in with placeholders
            "subjects": [],
            "experience": [],
            "subject_levels": [],
            "address": "",
            "gender": [],
            "commute_method": "",
            "max_commute_time": 60,
        }

    db_session.add(session)
    # is it better to return the object created by the database instead of directly returning the created variable? Idk.
    # return db_session.getBy({"telegram_handle":telegram_handle})[0]
    return session

async def get_session(telegram_handle:str) -> object:
    db_session = db.getDb("sessions.json")

    try:
        session:list[object] = db_session.getBy({"telegram_handle": telegram_handle})
        # print(f"Results from searching for session: {json.dumps(session,indent=2)}")
        # If session exists, return that session
        if len(session) > 0:
            print(f"📲 Found existing session with {telegram_handle}, returning object...")
            return session[0] # The first object. There should only be one anyway.
        else: 
            return None
        
    except Exception as e:
        print(f"⛔ Error occured while trying to retrieve session: {e}. Error on line {e.__traceback__.tb_lineno}")
        
# update the session object based on the queries given. This is assuming that 
async def update_session(telegram_handle:str,queries:list[str],profile_properties:list[str]):

    db_session = db.getDb("sessions.json")
    # retrieve the current session object
    session = await get_session(telegram_handle=telegram_handle)

    # Update the session with the new values
    for query in queries:
        key = query.split("=")[0]
        value:str = query.split("=")[1]
        if value.isnumeric():
            value = int(value) # to account for number variables. wonder if there's a better way to do this....

        # TODO: Now, i have to be very careful for how I'm supposed to update the session variables.
        if key == "progress":
            print("⏯️ This is a progress update")
            session[key] = value

            # Update the object within the database
            db_session.updateById(session["id"],session)
            print("🆗 Session progress updated succesfully")
        else:
            # re-use update_tutor_details?
            print(f"😖 This is NOT a progress update. Key: {key}. Value: {value}. Updating tutor details from button pressed...")
            await update_tutor_details_via_button(value=value,telegram_handle=telegram_handle,profile_properties=profile_properties)

    

async def update_tutor_details_via_button(value:str,telegram_handle:str,profile_properties:list[str]):
    print(f"📍 Received an update query of value: {value}")
    # look at the current session's progress. what attribute of the profile is the user trying to update?
    db_session = db.getDb("sessions.json")
    session = await get_session(telegram_handle=telegram_handle)
    progress = session["progress"]
    print(f"👤 User is trying to update the property: {profile_properties[progress]}")

    match progress:
        case 1: # subjects
            # Get the current list of items
            subjects:list[str] = session[profile_properties[progress]]

            # From the name of the Constant, get the corresponding regex_pattern of that object
            regex_pattern = [subject.regex_pattern for subject in ALL_SUBJECTS if subject.name == value][0]
            print(f"Found the value's corresponding regex_pattern: {regex_pattern}")
            # If this particular regex_pattern exists already, REMOVE IT
            if regex_pattern in subjects:
                print("➖ The subject already exists! Removing...")
                subjects.remove(regex_pattern)
            # Else, ADD it (basically act as a toggle)
            else:
                print("➕ The subject does not exist. Adding...")
                subjects.append(regex_pattern)

            session[profile_properties[progress]] = subjects
            db_session.updateById(session["id"],session)
        case 2: # subject levels
            # Get the current list of items
            levels:list[str] = session[profile_properties[progress]]
            regex_pattern = [level.regex_pattern for level in ALL_SUBJECT_LEVELS if level.name == value][0]
            print(f"Found the value's corresponding regex_pattern: {regex_pattern}")
            
            if regex_pattern in levels:
                print("➖ The level already exists! Removing...")
                levels.remove(regex_pattern)
            # Else, ADD it (basically act as a toggle)
            else:
                print("➕ The level does not exist. Adding...")
                levels.append(regex_pattern)

            session[profile_properties[progress]] = levels
            db_session.updateById(session["id"],session)
        case 3: # experience
            # Get the current list of items
            experiences:list[str] = session[profile_properties[progress]]
            regex_pattern = [experience.regex_pattern for experience in ALL_TUTOR_EXPERIENCES_RANKED if experience.name == value][0]
            print(f"Found the value's corresponding regex_pattern: {regex_pattern}")
            if regex_pattern in experiences:
                print("➖ The experience already exists! Removing...")
                experiences.remove(regex_pattern)
            # Else, ADD it (basically act as a toggle)
            else:
                print("➕ The experience does not exist. Adding...")
                experiences.append(regex_pattern)

            session[profile_properties[progress]] = experiences
            db_session.updateById(session["id"],session)
        case 5: # gender
            # Get the current list of items
            genders:list[str] = session[profile_properties[progress]]
            regex_pattern = [gender.regex_pattern for gender in ALL_GENDERS if gender.name == value][0]
            print(f"Found the value's corresponding regex_pattern: {regex_pattern}")
            if regex_pattern in genders:
                print("➖ The gender already exists! Removing...")
                genders.remove(regex_pattern)
            # Else, ADD it (basically act as a toggle)
            else:
                print("➕ The gender does not exist. Adding...")
                genders.append(regex_pattern)

            session[profile_properties[progress]] = genders
            db_session.updateById(session["id"],session)
        case 6: # commute method
            commute:str = session[profile_properties[progress]]
            if commute == DRIVING.regex_pattern:
                session[profile_properties[progress]] = PUBLIC_TRANSPORT.regex_pattern
            else:
                session[profile_properties[progress]] = DRIVING.regex_pattern
            db_session.updateById(session["id"],session)

async def update_tutor_details_via_message(message:str,telegram_handle:str,profile_properties:list[str]):
    print(f"📬 Received response from user: {message}")
    
    # look at the current session's progress. what attribute of the profile is the user trying to update?
    db_session = db.getDb("sessions.json")
    session = await get_session(telegram_handle=telegram_handle)
    progress = session["progress"]
    print(f"👤 User is trying to update the property: {profile_properties[progress]}")

    # a list of functions?
    match progress:
        case 0: # name
            session[profile_properties[progress]] = message
            db_session.updateById(session["id"],session)

        case 1: # subjects
            subjects = []
            for subject in ALL_SUBJECTS: # TODO: verify
                subject_match = re.findall(subject.regex_pattern,message,flags=re.IGNORECASE) # TODO: verify
                if len(subject_match) > 0:
                    subjects.append(subject.regex_pattern) # TODO: verify
            session[profile_properties[progress]] = subjects
            db_session.updateById(session["id"],session)
        
        case 2: # subject_levels
            subject_levels = []
            for level in ALL_SUBJECT_LEVELS:
            # I have to use regex as the subject levels are often loosely typed
                level_match = re.findall(level.regex_pattern,message,flags=re.IGNORECASE) # TODO: verify
                if len(level_match) > 0: 
                    subject_levels.append(level.regex_pattern) # TODO: verify
            session[profile_properties[progress]] = subject_levels
            db_session.updateById(session["id"],session)
        
        case 3: # experience
            experience_required = []
            for experience_constant in ALL_TUTOR_EXPERIENCES_RANKED:
                found_experience = re.findall(experience_constant.regex_pattern,message,flags=re.IGNORECASE) # TODO: verify
                if len(found_experience) > 0:
                    experience_required.append(experience_constant.regex_pattern) # TODO: verify
            session[profile_properties[progress]] = experience_required
            db_session.updateById(session["id"],session)
        
        case 4: # address
            session[profile_properties[progress]] = message
            db_session.updateById(session["id"],session)
        
        case 5: # gender
            gender_preference = []
            gender_match = re.findall("|".join([gender.regex_pattern for gender in ALL_GENDERS]),message,flags=re.IGNORECASE) # TODO: verify
            if len(gender_match) > 0:
                for gender in ALL_GENDERS:
                    if gender.regex_pattern in gender_match: gender_preference.append(gender.regex_pattern) # TODO: verify
            session[profile_properties[progress]] = gender_preference
            db_session.updateById(session["id"],session)
        
        case 6: # commute_method
            commute_match = re.findall("|".join([PUBLIC_TRANSPORT.regex_pattern,DRIVING.regex_pattern]),message,flags=re.IGNORECASE) # TODO: verify
            if DRIVING.regex_pattern in commute_match:
                commute_match = DRIVING.regex_pattern
            else:
                commute_match = PUBLIC_TRANSPORT.regex_pattern
            session[profile_properties[progress]] = commute_match # string variable
            db_session.updateById(session["id"],session)
        
        case 7: # max_commute_time
            session[profile_properties[progress]] = int(message) if message.isnumeric() else 60
            db_session.updateById(session["id"],session)


def delete_session(telegram_handle:str):
    db_session = db.getDb("sessions.json")
    session:object = db_session.getBy({"telegram_handle": telegram_handle})[0]
    db_session.deleteById(session["id"])