import os
import re
from classes.tuition_job import TuitionJob
from utils.tutor_filter import find_suitable_tutors
from utils.details_extractor import create_tuition_job
from telethon import Button, TelegramClient, events, types, tl
from dotenv import load_dotenv

from bot import interactions, crud

load_dotenv()
tuition_finder_chat = os.getenv('TUITION_FINDER_CHAT')

# My own Telegram Client
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
client = TelegramClient('rian', api_id, api_hash).start()

# @TuitionFinderBot
bot_token = os.getenv('BOT_TOKEN')
tuition_finder_bot = TelegramClient('TuitionFinderBot', api_id, api_hash).start(bot_token=bot_token)

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
            await tuition_finder_bot.send_message(suitable_tutor.telegram_handle,message=message)
        except Exception as e:
            print(f"⛔ Error occured when trying to forward job to {suitable_tutor.telegram_handle}: {e}")

# ===== Commands =====

# Entry command to CRUD operations via button navigation
@tuition_finder_bot.on(events.newmessage.NewMessage(pattern="/start",incoming=True))
async def start(event:events.newmessage.NewMessage.Event):
    await interactions.start(event=event,tuition_finder_bot=tuition_finder_bot)

# Secret function to seed data into database...woahhhh
@tuition_finder_bot.on(events.newmessage.NewMessage(pattern="/seed",incoming=True))
async def start(event:events.newmessage.NewMessage.Event):
    await crud.seed_data(event=event,tuition_finder_bot=tuition_finder_bot)

# The default response for any unrecognized message received from the bot
# Introduces itself and provides the possible ways to interact with it
# I think this has to be the LAST function I put in this script
@tuition_finder_bot.on(events.NewMessage(incoming=True))
async def default(event:events.newmessage.NewMessage.Event):
    await interactions.default_message(event=event,tuition_finder_bot=tuition_finder_bot)

# ===== Callback Queries =====
@tuition_finder_bot.on(events.callbackquery.CallbackQuery(data="read"))
async def read(event:events.newmessage.NewMessage.Event):
    await interactions.read(event=event,tuition_finder_bot=tuition_finder_bot)

@tuition_finder_bot.on(events.callbackquery.CallbackQuery(data="update"))
async def update(event:events.newmessage.NewMessage.Event):
    await interactions.update(event=event,tuition_finder_bot=tuition_finder_bot)

@tuition_finder_bot.on(events.callbackquery.CallbackQuery(data="delete"))
async def delete(event):
    await interactions.delete(event=event,tuition_finder_bot=tuition_finder_bot)

async def main():
    await client.run_until_disconnected()
    await tuition_finder_bot.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())

# if __name__ == '__main__':
#     main()
    