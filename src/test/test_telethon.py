from telethon import TelegramClient

# Remember to use your own values from my.telegram.org!
api_id = 20415981
api_hash = '2f54f55601712caa17fb333ba45d5808'
client = TelegramClient('rian', api_id, api_hash)

async def main():
    # Getting information about yourself
    me = await client.get_me()

    # "me" is a user object. You can pretty-print
    # any Telegram object with the "stringify" method:
    # print(me.stringify())

    # send a message to aakhirah haha
    # await client.send_message("@xymusibrahim","Hello from my telegram python script! ~hell yeah")

    # send a message to riona
    # await client.send_message("+6588628956","Hello from my telegram python script! ~hell yeah")

    # You can print all the dialogs/conversations that you are part of:
    # async for dialog in client.iter_dialogs():
    #     print(dialog.name, 'has ID', dialog.id)

    # You can, of course, use markdown in your messages:
    message = await client.send_message(
        'me',
        'This message has **bold**, `code`, __italics__ and '
        'a [nice website](https://example.com)!',
        link_preview=False
    )

    # You can reply to messages directly if you have a message object
    # await message.reply('Cool!')

    # Sending a message returns the sent message object, which you can use
    # print(message.raw_text)

    # You can print the message history of any chat:
    async for message in client.iter_messages('me', limit=10, reverse=True):
        print(message.id, message.text)




with client:
    client.loop.run_until_complete(main())