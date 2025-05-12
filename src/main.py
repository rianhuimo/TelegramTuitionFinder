import logging
import re

from tuition_utils import match_suitable_tutors, get_tuition_details

# logging.basicConfig(format='[%(levelname) %(asctime)s] %(name)s: %(message)s',level=logging.WARNING)

from telethon import TelegramClient, events, types

# wow...very secure...whatever. Shoot me.
google_maps_api_key = "AIzaSyAbVrHmKQ7GDkSJou8hcvkag2sW25i9mBA"
my_home_address = "40B Margaret Drive"

# Remember to use your own values from my.telegram.org!
api_id = 20415981
api_hash = '2f54f55601712caa17fb333ba45d5808'
client = TelegramClient('rian', api_id, api_hash)

tution_applications_dump = "🏫 Rian's Tuition Assignments"

home_address_coords = {
    "lat": 1.2972797597445798, 
    "lng": 103.80598786472773
}

@client.on(events.NewMessage)
async def my_event_handler(event):
    # print(event.message.stringify())
    # getting info about the channel for dev purpose
    chat = await event.get_chat()

    if (
        type(chat) == types.Channel and
        re.findall(r"tutor|tuition",chat.title.lower())
        ):
        print("\n\n===============📚📚📚===============")
        print(f"Tuition channel message intercepted: [{chat.title}]")
        print(event.message.message)

        message = event.message.message

        # retrieve tuition job info
        tuition_job = get_tuition_details(message=message,tuition_channel=chat.title)

        print("\n\n===============🏫🗺️👩🏼‍🏫===============")
        print(f"Subject: {tuition_job["subjects"]}")
        print(f"Address: {tuition_job["address"]}")
        print(f"Experience: {tuition_job["experience"]}")

        tuition_job = match_suitable_tutors(tuition_job=tuition_job)

        # Final output after filtering
        if (len(tuition_job["suitable_tutors"]) > 0):
            suitable_tutors = []
            for tutor in tuition_job["suitable_tutors"]:
                suitable_tutors.append(tutor["name"])
            print(f"\n✅ This job is suitable for: {suitable_tutors}")
        else:
            print("\n😑 This job isn't suitable for anyone...")

    else:
        print("\n\n===============📨📨📨===============")
        print(f"Not a tuition channel.")
        print(f"Type: {type(chat)}")
        if (type(chat) == types.Channel):
            print(f"It's from [{chat.title}]")
        elif (type(chat) == types.User):
            print(f"It's from [{chat.username}]")

client.start()
client.run_until_disconnected()

    