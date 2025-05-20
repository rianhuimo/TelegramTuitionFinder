import os
from telethon import TelegramClient, events, types
from dotenv import load_dotenv
load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')

# @TuitionFinderBot
bot_token = os.getenv('BOT_TOKEN')
tuition_finder_bot = TelegramClient('TuitionFinderBot', api_id, api_hash).start(bot_token=bot_token)

async def main():
    # RianTutorChannel = await bot.get_entity("https://t.me/+TrY9lhBoincxYTU1")
    await tuition_finder_bot.send_message("@xymusibrahim", 'Damn...')

with tuition_finder_bot:
    tuition_finder_bot.loop.run_until_complete(main())