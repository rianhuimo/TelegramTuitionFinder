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
        print(f"Results from searching for session: {json.dumps(session,indent=2)}")
        # If session exists, return that session
        if len(session) > 0:
            print(f"📲 Found existing session with {telegram_handle}, returning object...")
            return session[0] # The first object. There should only be one anyway.
        else: 
            return None
        
    except Exception as e:
        print(f"⛔ Error occured while trying to retrieve session: {e}. Error on line {e.__traceback__.tb_lineno}")
        
# update the session object based on the queries given. This is assuming that 
async def update_session(telegram_handle:str,queries:list[str]):

    db_session = db.getDb("sessions.json")
    # retrieve the current session object
    session = await get_session(telegram_handle=telegram_handle)

    # Update the session with the new values
    for query in queries:
        key = query.split("=")[0]
        value:str = query.split("=")[1]
        if value.isnumeric():
            value = int(value) # to account for number variables. wonder if there's a better way to do this....
        session[key] = value

    # Update the object within the database
    db_session.updateById(session["id"],session)
    print("🆗 Session variable updated succesfully")

async def update_tutor_details(message:str,telegram_handle:str,profile_properties:list[str]):
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
            for subject in ALL_SUBJECTS:
                subject_match = re.findall(subject,message,flags=re.IGNORECASE)
                if len(subject_match) > 0:
                    subjects.append(subject)
            session[profile_properties[progress]] = subjects
            db_session.updateById(session["id"],session)
        
        case 2: # subject_levels
            subject_levels = []
            for level in ALL_SUBJECT_LEVELS:
            # I have to use regex as the subject levels are often loosely typed
                level_match = re.findall(level,message,flags=re.IGNORECASE)
                if len(level_match) > 0: 
                    subject_levels.append(level)
            session[profile_properties[progress]] = subject_levels
            db_session.updateById(session["id"],session)
        
        case 3: # experience
            experience_required = []
            for experience_constant in ALL_TUTOR_EXPERIENCES_RANKED:
                found_experience = re.findall(experience_constant,message,flags=re.IGNORECASE)
                if len(found_experience) > 0:
                    experience_required.append(experience_constant)
            session[profile_properties[progress]] = experience_required
            db_session.updateById(session["id"],session)
        
        case 4: # address
            session[profile_properties[progress]] = message
            db_session.updateById(session["id"],session)
        
        case 5: # gender
            gender_preference = []
            gender_match = re.findall("|".join(ALL_GENDERS),message)
            if len(gender_match) > 0:
                for gender in ALL_GENDERS:
                    if gender in gender_match: gender_preference.append(gender)
            session[profile_properties[progress]] = gender_preference
            db_session.updateById(session["id"],session)
        
        case 6: # commute_method
            commute_match = re.findall("|".join([PUBLIC_TRANSPORT,DRIVING]),message,flags=re.IGNORECASE)
            session[profile_properties[progress]] = commute_match
            db_session.updateById(session["id"],session)
        
        case 7: # max_commute_time
            session[profile_properties[progress]] = int(message) if message.isnumeric() else 60
            db_session.updateById(session["id"],session)


def delete_session(telegram_handle:str):
    db_session = db.getDb("sessions.json")
    session:object = db_session.getBy({"telegram_handle": telegram_handle})[0]
    db_session.deleteById(session["id"])