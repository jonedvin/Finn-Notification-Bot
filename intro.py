import asyncio
import telegram

TOKEN = "5417799349:AAEn8AYUDpEuHBCMkGy2bk1NLlrv7CWJ0sw"

jon_chat_id = "5535533982"

async def main():
    bot = telegram.Bot(TOKEN)
    async with bot:
        # print(await bot.get_me())
        # print((await bot.get_updates())[0])
        await bot.send_message(text="Hi Jon!", chat_id=jon_chat_id)


if __name__ == '__main__':
    asyncio.run(main())
