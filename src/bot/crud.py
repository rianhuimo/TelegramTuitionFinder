from pysondb import db
from telethon import Button, TelegramClient, events, types, tl
from classes.tutor import * # get all those juicy constants

# Contains all CRUD functions that the bot performs
def search(telegram_handle:str):
    database = db.getDb("tutors.json")
    result = database.getBy({"telegram_handle": "@rianhuii"})
    return result

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

