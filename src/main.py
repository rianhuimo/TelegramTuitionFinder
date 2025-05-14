import re
from classes.TuitionJob import TuitionJob
from utils.tuition_utils import match_tutors
from telethon import TelegramClient, events, types

tuition_finder_chat = "🏫 Rian's Tuition Assignments"

# My own Telegram Client
api_id = 20415981
api_hash = '2f54f55601712caa17fb333ba45d5808'
client = TelegramClient('rian', api_id, api_hash).start()

# @TuitionFinderBot
bot_token = "6695966335:AAHhwNPe0K5hk7fTyWoo9RcZXz4BUpc1TOY"
bot = TelegramClient('TuitionFinderBot', api_id, api_hash).start(bot_token=bot_token)
event_latch = None

@client.on(events.NewMessage)
async def my_event_handler(event):
    # print(event.message.stringify())
    # getting info about the channel for dev purpose
    chat = await event.get_chat()

    if (
        type(chat) == types.Channel and
        re.findall(r"tutor|tuition",chat.title.lower())
        ):
        
        message = event.message.message

        # (1)-A retrieve tuition job info
        job = TuitionJob(message=message,channel_name=chat.title)

        print("\n\n===============🏫🗺️👩🏼‍🏫===============")
        print(f"Tuition channel message intercepted: [{chat.title}]")
        print(f"Address: {job.address}")

        # (2)-A match suitable tutors
        match_tutors(job)

        # (3)-A Output the final TuitionJob object to the bot!
        if (len(job.suitable_tutors) > 0):
            # for suitable_tutor in job.suitable_tutors:
            #     print(f"\n✅ This job is suitable for: {suitable_tutor[0].telegram_handle}, with a fastest commute of {suitable_tutor[1]["text"]}")

            await send_to_chat(job)
        else:
            print("\n😑 This job isn't suitable for anyone...")

        print("\n\n===============📚📚📚===============")
        print(f"Here's the full message:")
        print(event.message.message)

    else:
        print("\n===============📨📨📨===============")
        print(f"Not a tuition channel.")
        # print(f"Type: {type(chat)}")
        # if (type(chat) == types.Channel):
        #     print(f"It's from [{chat.title}]")
        # elif (type(chat) == types.User):
        #     print(f"It's from [{chat.username}]")

async def send_to_chat(job:TuitionJob):
    print("🤖 Bot is printing message:")

    message = ""
    for suitable_tutor in job.suitable_tutors:
        message += f"\n✅ This job is suitable for: {suitable_tutor[0].telegram_handle}"
        message += f"\n🗺️ Fastest commute: {suitable_tutor[1]["text"]}"
        message += f"\n📚 Subject matches: {suitable_tutor[2]}"
        message += f"\n🏫 Experience matches: {suitable_tutor[3]}"
        message += "\n"

    message += f"\n\n📨 Full message 📨\n{job.message}"
    message += f"\nPosted on {job.tuition_channel.channel_link}"

    global event_latch
    if (event_latch):
        await event_latch.respond(message)
    else:
        print("⚠️ No event found, cannot send message. Please try to initiate using /begin")
    # await bot.send_message(message=json.dumps(tuition_job,indent=2),entity=tuition_finder_chat)

@bot.on(events.NewMessage(pattern='/start'))
async def begin(event):

    # Idea: save this event as a global variable...then just...keep replying to it...
    global event_latch
    event_latch = event
    print(type(event_latch))
    
    print("🤖 Bot started. Saving event (hopefully)")
    await event_latch.reply("🐙 TuitionFinder started! Detecting tuition jobs... 🔍")

@bot.on(events.NewMessage(pattern='/test'))
async def begin(event):
    # This should reference the original "/start" message
    global event_latch
    await event_latch.reply("(This is a test) Replying to /start")

async def start_tuition_bot():
    await client.send_message(tuition_finder_chat,"/start")

async def main():
    await start_tuition_bot()
    await client.run_until_disconnected()
    await bot.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())

# if __name__ == '__main__':
#     main()
    