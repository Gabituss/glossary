import asyncio

from bot import botlogging, mics, handlers, dialogs, database
from bot.mics import dp


async def main():
    await botlogging.setup()
    await handlers.setup(dp)
    await dialogs.setup(dp)
    await database.setup()

    await mics.setup()


if __name__ == '__main__':
    asyncio.run(main())
