import os
import re
from classes.tuition_job import TuitionJob
from utils.tutor_filter import find_suitable_tutors
from utils.details_extractor import create_tuition_job
from telethon import Button, TelegramClient, events, types, tl
from dotenv import load_dotenv

load_dotenv()
tuition_finder_chat = os.getenv('TUITION_FINDER_CHAT')

# My own Telegram Client
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
client = TelegramClient('rian', api_id, api_hash).start()

# @TuitionFinderBot
bot_token = os.getenv('BOT_TOKEN')
bot = TelegramClient('TuitionFinderBot', api_id, api_hash).start(bot_token=bot_token)
event_latch = None

@client.on(events.NewMessage)
async def my_event_handler(event):
    # print(event.message.stringify())
    # getting info about the channel for dev purpose
    chat = await event.get_chat()

    if (
        type(chat) == types.Channel and
        re.findall(r"tutor|tuition",chat.title.lower()) and
        not ("rian's tuition" in chat.title.lower())
        ):
        
        message = event.message.message

        print("\n\n===============🏫🗺️👩🏼‍🏫===============")
        print(f"Tuition channel message intercepted: [{chat.title}]")

        # (1)-2.0
        job = create_tuition_job(message=message,channel_name=chat.title)
        print(job.to_string())

        # (2)-2.0 match suitable tutors
        job.suitable_tutors = find_suitable_tutors(job)

        # (3)-2.0 Output the final TuitionJob object to the bot!
        if (len(job.suitable_tutors) > 0):
            await broadcast_to_tutors(job)
        else:
            print("\n😑 This job isn't suitable for anyone...")

        print("\n\n===============📚📚📚===============")
        print(f"Here's the full message:")
        print(event.message.message)

    else:
        print("\n===============📪📪📪===============")
        print(f"Not a tuition channel.")

async def broadcast_to_tutors(job:TuitionJob):
    print(f"📣 Broadcasting job to suitable tutors: {[tutor.telegram_handle for tutor in job.suitable_tutors]}")

    for suitable_tutor in job.suitable_tutors:
        print(f"📨 Sending to: {suitable_tutor.telegram_handle}")
        # Craft the message
        message = ""
        message += f"\n✅ This job is suitable for: {suitable_tutor.telegram_handle}"
        message += f"\n🗺️ Fastest commute: {suitable_tutor.fastest_commute}"
        message += f"\n📚 Subject matches: {suitable_tutor.subjects_match}"
        message += f"\n🏫 Subject level matches: {suitable_tutor.subject_levels_match}"
        message += f"\n💼 Experience matches: {suitable_tutor.experience_match}"

        message += f"\n\n📨 Full message 📨\n{job.message}"
        message += f"\nPosted on {job.tuition_channel.channel_link}"

        # Send message to tutor
        try:
            # ‼️ Important! Make sure that the tutor has initiated a chat before the bot is able to send them a private message
            await bot.send_message(suitable_tutor.telegram_handle,message=message)
        except Exception as e:
            print(f"⛔ Error occured when trying to forward job to {suitable_tutor.telegram_handle}: {e}")

# Entry command to CRUD operations via button navigation
@bot.on(events.callbackquery.CallbackQuery(data="start"))
async def start(event:events.newmessage.NewMessage.Event):
    message:tl.patched.Message = event.message
    chat = await event.get_chat()
    if type(chat) == types.User:
        user:types.User = chat
        telegram_handle = f"@{user.username}"
        try:
            # user.username is equivalent to Tutor.telegram_handle
            await message.respond(f"🔍 Searching for your tutor details (@{telegram_handle})...")
            # I can use this instead of the shorthand function "event.respond()" as it no longer gives me parameter hints. Use this as a baseline
            await bot.send_message(
                entity=chat,
                message="this message should contain your tutor details (if any)",
                buttons=[
                    Button.inline(text="Edit my details",data=f"edit/{telegram_handle}"),
                ])
        except Exception as e:
            print(f"⛔ Error occured while sending messages: {e}. Error on line {e.__traceback__.tb_lineno}")
    raise events.StopPropagation

# Edit tutor details. I'm providing a regex pattern in this context.
@bot.on(events.callbackquery.CallbackQuery(data=re.compile(r"edit/")))
async def edit(event:events.newmessage.NewMessage.Event):
    chat = await event.get_chat()
    if type(chat) == types.User:
        user:types.User = chat
        telegram_handle = f"@{user.username}"
        event.respond("Edit request received.")

# The default response for any unrecognized message received from the bot
# Introduces itself and provides the possible ways to interact with it
# I think this has to be the LAST function I put in this script
@bot.on(events.NewMessage)
async def default(event):
    # print(event.message.stringify())
    print("📬 Received a message")
    chat = await event.get_chat()
    try:
        if type(chat) == types.User:
                # I can use this instead of the shorthand function "event.respond()" as it no longer gives me parameter hints. Use this as a baseline
                await bot.send_message(
                    entity=chat,
                    message="🐙 Hello! I'm TuitionFinder. 🤖" + 
                    "\n🏫 I scour all Singapore Telegram Tuition Channels to help tutors connect with the right students. 🧑🏼‍🎓" +
                    "\n\nInteract with me by texting /start",
                    buttons=[
                        Button.url(text="Link to cool music", url="https://open.spotify.com/album/0ErRTuEFNp7E7Yp8iWLSkw?flow_ctx=01b42b72-3a04-4a21-8985-9664f2d2a259%253A17"),
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

async def main():
    await client.run_until_disconnected()
    await bot.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())

# if __name__ == '__main__':
#     main()
    