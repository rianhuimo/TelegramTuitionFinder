from telethon import TelegramClient, events, types

api_id = 20415981
api_hash = '2f54f55601712caa17fb333ba45d5808'

# @TuitionFinderBot
bot_token = "6695966335:AAHhwNPe0K5hk7fTyWoo9RcZXz4BUpc1TOY"
bot = TelegramClient('TuitionFinderBot', api_id, api_hash).start(bot_token=bot_token)

async def main():
    # RianTutorChannel = await bot.get_entity("https://t.me/+TrY9lhBoincxYTU1")
    await bot.send_message("https://t.me/+TrY9lhBoincxYTU1", 'Testing Telethon!')

with bot:
    bot.loop.run_until_complete(main())