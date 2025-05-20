import json
from telethon import Button, TelegramClient, events, types, tl

import bot.crud as crud
from classes.tutor import ALL_SUBJECTS, ALL_SUBJECT_LEVELS, ALL_TUTOR_EXPERIENCES_RANKED, ALL_GENDERS

# contains all interactions between bot and user
BUTTON_CREATE = [Button.inline(text="Create profile",data="create")]
BUTTON_READ = Button.inline(text="View profile",data="read")
BUTTON_UPDATE = Button.inline(text="Update profile",data="create")
BUTTON_DELETE = Button.inline(text="Delete profile",data="delete")
BUTTON_HOME = Button.inline(text="🏡 Home",data="home")

PROFILE_QUESTIONS = [
    "💬 What is your name?",
    "📚 What subjects do you teach?",
    "🏫 What subject levels do you teach?" + f"\nLevels registered with TuitionFinder are: {[level.name for level in ALL_SUBJECT_LEVELS]}",
    "🧑🏽‍🏫 What is your tutoring experience?" + f"\nTutor expertise options are: {[experience.name for experience in ALL_TUTOR_EXPERIENCES_RANKED]}",
    "🗺️ Where do you live? (An approximate location would suffice but you can be as precise as you want)",
    "🏳️‍⚧️ What is your gender? (Some tuition jobs have a gender preference)" + f"\nExamples: {[gender.name for gender in ALL_GENDERS]}",
    "🚂 What is your commuting method?\n🚌 Transit / 🚗 Driving",
    "⌚ What is your maximum commute time? Please provide your answer in minutes."
]
# Has to be in the same order as profile questions.
PROFILE_PROPERTIES = [
    "name",
    "subjects",
    "subject_levels",
    "experience",
    "address",
    "gender",
    "commute_method",
    "max_commute_time",
]

# keep track of user interactions within the program.
user_sessions:list[dict] = []

async def default_message(event:events.newmessage.NewMessage.Event,tuition_finder_bot):
    print("📬 Received a message")
    chat = await event.get_chat()
    try:
        if type(chat) == types.User:
            telegram_handle = f"@{chat.username}"
            # Find a current session with the user. If not found, return default message.
            session:object = await crud.get_session(telegram_handle)
            
            # If session is found, jump to the create profile function
            if session is not None:
                print("⛲⛲⛲ session is found. Redirecting to create_profile.py: ")
                await create_profile(event=event,tuition_finder_bot=tuition_finder_bot)
            else:
                # I can use this instead of the shorthand function "event.respond()" as it no longer gives me parameter hints. Use this as a baseline
                await tuition_finder_bot.send_message(
                    entity=chat,
                    message="🐙 Hello! I'm TuitionFinder. 🤖" + 
                    "\n🏫 I scour all Singapore Telegram Tuition Channels to help tutors connect with the right students. 🧑🏼‍🎓" +
                    "\n\nInteract with me by texting /start",
                    buttons=[
                        Button.url(text="🪴 This project is on GitHub!", url="https://github.com/rianhuimo/TelegramTuitionFinder"),
                    ])
        else:
            await event.respond(
                message="🐙 Hello! I'm TuitionFinder. 🤖" + 
                    "\n🏫 I scour all Singapore Telegram Tuition Channels to help tutors connect with the right students. 🧑🏼‍🎓" +
                    "\n\n Interact with me through a direct message!",
                buttons=[
                    Button.url(text="📨 Message Bot", url="https://t.me/TuitionFinderBot"),
                ])
    except Exception as e:
        print(f"⛔ Error occured while sending messages: {e}. Error on line {e.__traceback__.tb_lineno}")

async def start(event:events.newmessage.NewMessage.Event,tuition_finder_bot):
    chat = await event.get_chat()
    if type(chat) == types.User:
        user:types.User = chat
        if user.username is not None:
            # case in point, my own sister doensn't have a telegram handle...
            telegram_handle = f"@{user.username}"
            try:
                # user.username is equivalent to Tutor.telegram_handle

                # query the database and check whether tutor profile exists with me yet.
                result = crud.search(telegram_handle)
                profile_found = result is not None

                message_no_profile = f"🚧 Profile not found for {telegram_handle}"
                message_existing_profile = f"✅ Found an existing profile for {telegram_handle}"

                # I can use this instead of the shorthand function "event.respond()" as it no longer gives me parameter hints. Use this as a baseline
                await tuition_finder_bot.send_message(
                    entity=chat,
                    message=f"🔍 Searching for your tutor details...\n" +
                        f"{message_existing_profile if profile_found else message_no_profile}",
                    buttons=[BUTTON_READ,BUTTON_UPDATE,BUTTON_DELETE] if profile_found else BUTTON_CREATE)
            except Exception as e:
                print(f"⛔ Error occured while sending messages: {e}. Error on line {e.__traceback__.tb_lineno}")
        else:
            await tuition_finder_bot.send_message(
                entity=chat,
                message="⚠️ I've detected that you don't possess telegram username.\n" +
                "TuitionFinder keeps track of tutor profiles by storing tutor's usernames, so unfortunately this bot won't work without one.")
            await tuition_finder_bot.send_file(
                entity=chat,
                file=open("assets/no_username.png","rb")
            )
    raise events.StopPropagation

async def read(event:events.callbackquery.CallbackQuery.Event,tuition_finder_bot:TelegramClient):
    chat = await event.get_chat()
    if type(chat) == types.User:
        telegram_handle = f"@{chat.username}"
        # this is already assuming that it exists, by verifying it during the '/start' command. Else this button would not appear
        result:object = crud.search(telegram_handle)

        await event.edit(
            f"🏫 Showing profile for {telegram_handle}:\n{json.dumps(result,indent=2)}",
            buttons=[BUTTON_HOME,BUTTON_UPDATE,BUTTON_DELETE])
       
async def delete(event:events.callbackquery.CallbackQuery.Event,tuition_finder_bot:TelegramClient):
    chat = await event.get_chat()
    if type(chat) == types.User:
        telegram_handle = f"@{chat.username}"
        await event.edit(
            "⚠️‼️ Confirm profile deletion ‼️⚠️\n\nThis action will completely remove your tutor profile stored within me",
            buttons=[
                Button.inline(text="🗑️ Confirm deletion",data="confirm_delete"),
                Button.inline(text="Cancel",data="home"),])
        
async def confirm_delete(event:events.callbackquery.CallbackQuery.Event,tuition_finder_bot:TelegramClient):
    chat = await event.get_chat()
    if type(chat) == types.User:
        telegram_handle = f"@{chat.username}"

        # crud delete
        crud.delete(telegram_handle=telegram_handle)

        # display message
        await event.answer("🍃 Profile deleted")
        await event.delete()
        # go back to start
        await start(event=event,tuition_finder_bot=tuition_finder_bot)

async def create_profile(event:events.callbackquery.CallbackQuery.Event|events.newmessage.NewMessage.Event,tuition_finder_bot:TelegramClient):
    chat = await event.get_chat()
    if type(chat) == types.User:
        telegram_handle = f"@{chat.username}"

        if type(event) == events.callbackquery.CallbackQuery.Event:
            print("🔧 create_profile was triggered by an inline button, updating session object...")
            # parse query data
            query_data = event.data.decode("utf-8") # Turns a byte string back into a normal string
            print(f"Query data received: {query_data}")
            query_data = query_data.split("?") # Take the parameters, it's always the second item on the list.

            if len(query_data) > 1: # If the list is only one item long, that means there are no query strings attached to the url
                print("👁️ Queries detected. Parsing and updating session object...")
                queries:str = query_data[-1] # progress=1
                queries = queries.split("&") # ["progress=1","name=Pebble Meow"]

                await crud.update_session(telegram_handle,queries,profile_properties=PROFILE_PROPERTIES)

        elif type(event) == events.newmessage.NewMessage.Event:
            print("🗨️ create_profile was triggered by a user response, updating session object...")

            # Pass in the message of the user
            await crud.update_tutor_details_via_message(event.message.message,telegram_handle,profile_properties=PROFILE_PROPERTIES)

        # 🪴 Session has been updated. Get the session state of the user
        session:object = await crud.get_session(telegram_handle)
        # print(f"Received the following object: {json.dumps(session,indent=2)}")

        # create one if not found (this code should run on the very first entry to this functions)
        if session is None:
            await crud.create_session(telegram_handle=telegram_handle)
            session:object = await crud.get_session(telegram_handle)

        # Input buttons based on question asked
        input_buttons = []
        match session["progress"]:
            case 1: # subjects
                # I can only append lists of buttons, not individual buttons. This means I have to make a matrix of some sort.
                all_subjects_buttons = []
                # Get the current list of items
                subjects:list[str] = session[PROFILE_PROPERTIES[session["progress"]]]
                for experience in ALL_SUBJECTS:
                    # for each subject, check to see if my current session's subject list has it.
                    if experience.regex_pattern in subjects:
                        all_subjects_buttons.append(Button.inline(
                            text=f"✅ {experience.name}" ,
                            data=f"create?data={experience.name}"))
                    else:
                        all_subjects_buttons.append(Button.inline(
                            text=f"{experience.name}" ,
                            data=f"create?data={experience.name}"))
                columns = 4
                rows = len(ALL_SUBJECTS)//columns
                # ...not me doing division math 😩😩😩😩
                remainder_index = (rows*columns) # it is simply the next index after the last grid item!

                # Credit to this link for this one-liner: https://www.geeksforgeeks.org/python-program-to-construct-nm-matrix-from-list/
                input_buttons = [all_subjects_buttons[i:i + columns] for i in range(0, rows * columns, columns)]
                input_buttons.append(all_subjects_buttons[remainder_index:])
            case 2: # subject_levels
                all_subject_level_buttons = []
                # Get the current list of items
                subject_levels:list[str] = session[PROFILE_PROPERTIES[session["progress"]]]
                for experience in ALL_SUBJECT_LEVELS:
                    # for each subject, check to see if my current session's subject list has it.
                    if experience.regex_pattern in subject_levels:
                        all_subject_level_buttons.append(Button.inline(
                            text=f"✅ {experience.name}" ,
                            data=f"create?data={experience.name}"))
                    else:
                        all_subject_level_buttons.append(Button.inline(
                            text=f"{experience.name}" ,
                            data=f"create?data={experience.name}"))
                columns = 2
                rows = len(ALL_SUBJECT_LEVELS)//columns
                remainder_index = (rows*columns)
                input_buttons = [all_subject_level_buttons[i:i + columns] for i in range(0, rows * columns, columns)]
                input_buttons.append(all_subject_level_buttons[remainder_index:])
            case 3: # experience
                all_experiences_buttons = []
                experiences:list[str] = session[PROFILE_PROPERTIES[session["progress"]]]
                for experience in ALL_TUTOR_EXPERIENCES_RANKED:
                    # for each subject, check to see if my current session's subject list has it.
                    if experience.regex_pattern in experiences:
                        all_experiences_buttons.append(Button.inline(
                            text=f"✅ {experience.name}" ,
                            data=f"create?data={experience.name}"))
                    else:
                        all_experiences_buttons.append(Button.inline(
                            text=f"{experience.name}" ,
                            data=f"create?data={experience.name}"))
                columns = 2
                rows = len(ALL_SUBJECT_LEVELS)//columns
                remainder_index = (rows*columns)
                input_buttons = [all_experiences_buttons[i:i + columns] for i in range(0, rows * columns, columns)]
                input_buttons.append(all_experiences_buttons[remainder_index:])
            case 5: # gender
                all_genders_buttons = []
                genders:list[str] = session[PROFILE_PROPERTIES[session["progress"]]]
                for gender in ALL_GENDERS:
                    if gender.regex_pattern in genders:
                        all_genders_buttons.append(Button.inline(
                            text=f"✅ {gender.name}" ,
                            data=f"create?data={gender.name}"))
                    else:
                        all_genders_buttons.append(Button.inline(
                            text=f"{gender.name}" ,
                            data=f"create?data={gender.name}"))
                columns = 2
                rows = len(ALL_GENDERS)//columns
                remainder_index = (rows*columns)
                input_buttons = [all_genders_buttons[i:i + columns] for i in range(0, rows * columns, columns)]
                input_buttons.append(all_genders_buttons[remainder_index:])
            case 6: # commute method
                commute:str = session[PROFILE_PROPERTIES[session["progress"]]]
                if commute == "driving":
                    input_buttons.append([Button.inline(
                            text=f"✅ Driving / Public Transport" ,
                            data=f"create?data={commute}")])
                else:
                    input_buttons.append([Button.inline(
                            text=f"Driving / Public Transport ✅" ,
                            data=f"create?data={commute}")])

        # Navigation buttons
        if (session["progress"] == 0):
            nav_buttons = [Button.inline(text="Next ▶️",data=f"create?progress={session["progress"] + 1}")]
        elif (session["progress"] < (len(PROFILE_QUESTIONS) - 1)):
            nav_buttons = [
                Button.inline(text="◀️ Previous",data=f"create?progress={session["progress"] - 1}"),
                Button.inline(text="Next ▶️",data=f"create?progress={session["progress"] + 1}")
            ]
        elif (session["progress"] == (len(PROFILE_QUESTIONS) - 1)):
            nav_buttons = [
                Button.inline(text="◀️ Previous",data=f"create?progress={session["progress"] - 1}")
            ]
        else:
            nav_buttons = [Button.inline(text="🤖 An error occured. Let's try this again.",data="cancel")]

        input_buttons.append(nav_buttons)

        # Cancel and confirm buttons
        input_buttons.append([
            Button.inline(text="Cancel",data="cancel"),
            Button.inline(text="✅ Submit profile",data=f"submit_profile")])
        
        # print(f"Buttons: {input_buttons}")

        if type(event) == events.callbackquery.CallbackQuery.Event:
            await event.edit(
                f"🏗️ Building your profile:\n\n" +
                # "Session progress: {session["progress"]}\n" +
                f"{PROFILE_QUESTIONS[session['progress']]}\n\n" +
                "⌨️ Type your details below ⬇️\n\n" +
                "💾 Currently saved response:\n" +
                f"{json.dumps(session[PROFILE_PROPERTIES[session["progress"]]],indent=2,ensure_ascii=True)}",
                buttons=input_buttons
            )
        elif type(event) == events.newmessage.NewMessage.Event:
            await event.respond(
                f"🏗️ Building your profile:\n\n" +
                f"{PROFILE_QUESTIONS[session['progress']]}\n\n" +
                "⌨️ Type your details below ⬇️\n\n" +
                "💾 Currently saved response:\n" +
                f"{session[PROFILE_PROPERTIES[session["progress"]]]}",
                buttons=[
                    nav_buttons,
                    [
                        Button.inline(text="Cancel",data="cancel"),
                        Button.inline(text="✅ Submit profile",data=f"submit_profile")
                    ],
                ]
            )

async def submit_profile(event:events.callbackquery.CallbackQuery.Event,tuition_finder_bot):
    chat = await event.get_chat()
    if type(chat) == types.User:
        telegram_handle = f"@{chat.username}"

        # submit profile!

        # check if tutor exists
        result = crud.search(telegram_handle)
        profile_found = result is not None

        # if the profile exists, create the session with its properties
        if profile_found:
            await crud.update(telegram_handle=telegram_handle,tutor_id=result["id"])
            await event.answer("💾 Tutor profile saved successfully!")
            await event.edit("💾 Tutor profile saved successfully.\n🤖 TuitionFinder will now forward you relevent tuition jobs.\n\n🐙 We wish you all the best in finding your students!",
                            buttons=[Button.inline(text="🏡 Back to home",data="cancel")])
        else:
            # Create new profile
            await crud.create(telegram_handle=telegram_handle)
            await event.answer("✅ Tutor profile created successfully!")
            await event.edit("✅ Tutor profile created successfully.\n🤖 TuitionFinder will now forward you relevent tuition jobs.\n\n🐙 We wish you all the best in finding your students!",
                            buttons=[Button.inline(text="🏡 Back to home",data="cancel")])


async def cancel(event:events.callbackquery.CallbackQuery.Event,tuition_finder_bot):
    chat = await event.get_chat()
    if type(chat) == types.User:
        telegram_handle = f"@{chat.username}"

        # delete the session with the user
        crud.delete_session(telegram_handle=telegram_handle)
        print('🗑️ Session deleted')

        # display message
        await event.answer("🍥 Returning home...")
        await event.delete()

        # return to start
        await start(event=event,tuition_finder_bot=tuition_finder_bot)