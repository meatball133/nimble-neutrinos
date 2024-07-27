import asyncio
from aiohttp import ClientSession
import config
import discord
from discord.ext import commands
from src.models import Model

import cogs


class CordPicsBot(commands.Bot):
    """A single-line docstring giving a brief description of the bot"""

    def __init__(
        self,
        *args,
        db: Model,
        session: ClientSession,
        **kwargs,
    ):
        intents = discord.Intents(
            guilds=True,
            messages=True,
            message_content=True,
        )
        super().__init__(
            *args,
            **kwargs,
            command_prefix="!",
            intents=intents,
            owner_ids=config.OWNER_IDS,
        )

        self.db = db
        self.session = session

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")

    async def setup_hook(self) -> None:
        results = await asyncio.gather(
            *(self.load_extension(ext) for ext in cogs.INITIAL_EXTENSIONS),
            return_exceptions=True,
        )
        for ext, result in zip(cogs.INITIAL_EXTENSIONS, results):
            if isinstance(result, Exception):
                print(f"Failed to load extension `{ext}`: {result}")


async def main():
    model = Model()
    session = ClientSession()
    bot = CordPicsBot(
        db=model,
        session=session,
    )

    async with session, model, bot:
        if config.TESTING_MODE is True:
            await bot.start(config.TESTING_BOT_TOKEN)
        else:
            await bot.start(config.BOT_TOKEN)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
