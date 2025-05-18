import json
from telethon import Button, TelegramClient, events, types, tl

from bot.crud import search, seed_data

# contains all interactions between bot and user
BUTTONS_NO_PROFILE = [Button.inline(text="Create profile",data="create")]
BUTTONS_EXISTING_PROFILE = [
        Button.inline(text="View profile",data="read"),
        Button.inline(text="Update profile",data="update"),
        Button.inline(text="Delete profile",data="delete")]

async def default_message(event:events.newmessage.NewMessage.Event,tuition_finder_bot):
    print("📬 Received a message")
    chat = await event.get_chat()
    try:
        if type(chat) == types.User:
                # I can use this instead of the shorthand function "event.respond()" as it no longer gives me parameter hints. Use this as a baseline
                await tuition_finder_bot.send_message(
                    entity=chat,
                    message="🐙 Hello! I'm TuitionFinder. 🤖" + 
                    "\n🏫 I scour all Singapore Telegram Tuition Channels to help tutors connect with the right students. 🧑🏼‍🎓" +
                    "\n\nInteract with me by texting /start",
                    buttons=[
                        Button.url(text="Link to cool music", url="https://open.spotify.com/album/0ErRTuEFNp7E7Yp8iWLSkw?flow_ctx=01b42b72-3a04-4a21-8985-9664f2d2a259%253A17"),
                        Button.url(text="Bandcamp!!!!", url="https://dusqk.bandcamp.com/album/sanctuary-os"),
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
    message:tl.patched.Message = event.message
    chat = await event.get_chat()
    if type(chat) == types.User:
        user:types.User = chat
        if user.username is not None:
            # case in point, my own sister doensn't have a telegram handle...
            telegram_handle = f"@{user.username}"
            try:
                # user.username is equivalent to Tutor.telegram_handle

                # query the database and check whether tutor profile exists with me yet.
                result = search(telegram_handle)
                profile_found = len(result) > 0

                message_no_profile = f"🚧 Profile not found for {telegram_handle}"
                message_existing_profile = f"✅ Found an existing profile for {telegram_handle}"

                # I can use this instead of the shorthand function "event.respond()" as it no longer gives me parameter hints. Use this as a baseline
                await tuition_finder_bot.send_message(
                    entity=chat,
                    message=f"🔍 Searching for your tutor details ({telegram_handle})...\n" +
                        f"{message_existing_profile if profile_found else message_no_profile}",
                    buttons=BUTTONS_EXISTING_PROFILE if profile_found else BUTTONS_NO_PROFILE)
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
        result = search(telegram_handle)
        tutor_obj = result[0]

        await event.edit(
            f"🏫 Showing profile for {telegram_handle}:\n{json.dumps(tutor_obj,indent=2)}",
            buttons=BUTTONS_EXISTING_PROFILE)

async def update(event:events.callbackquery.CallbackQuery.Event,tuition_finder_bot:TelegramClient):
    print(type(tuition_finder_bot))
    print(type(event))
    chat = await event.get_chat()
    if type(chat) == types.User:
        telegram_handle = f"@{chat.username}"
        await event.edit(
            "hey you clicked update",
            buttons=BUTTONS_EXISTING_PROFILE)