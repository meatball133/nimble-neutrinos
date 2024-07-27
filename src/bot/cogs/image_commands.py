from asyncpg.connection import asyncpg
import discord
from discord import app_commands
from discord.ext import commands

from asyncpg import Pool

from cogs import ALL_MODULES
from main import NimbleNeutrinos

import config


class ImageCommands(commands.Cog):
    bot: NimbleNeutrinos
    db_pool: Pool

    def __init__(self, bot: NimbleNeutrinos):
        self.bot = bot
        self.db_pool = bot.pool

    async def _get_last_image(self, ctx: commands.Context):
        messages = ctx.channel.history(limit=50)
        message: discord.Message | None = None
        attachments: list[discord.Attachment] = []

        while not (
            attachments
            and len(attachments == 1)
            and attachments[0].content_type.startswith("image")
            and message.author.id == ctx.author.id
        ):
            message = await messages.__anext__()
            attachments = message.attachments

        return attachments[0]

    # TODO: Make the SQL request work (insert image with tags into database) and return appropriate boolean
    async def _post_data(self, ctx: commands.Context, url: str, tag: list[str]):
        db_response = await self.db_pool.execute(f"""
            INSERT INTO {config.DB().DATABASE}
        """)

        return bool(db_response)

    @app_commands.command(
        name="addtags",
        description="Add tags to the last image sent by you in this channel. (Max. 50 messages ago)",
    )
    @app_commands.describe(tags="Space separated list of tags")
    async def add_tags(self, ctx: commands.Context, tags: str):
        image: discord.Attachment = await self._get_last_image(ctx)
        tag_list = tags.split()

        post_data_result = await self._post_data(ctx, image.url, tag_list)
        embed: discord.Embed

        if post_data_result:
            embed = discord.Embed(
                title="Image Added!",
                description=f"Tags: *{", ".join(tag_list)}*",
                color=discord.Color.blurple(),
            )
            embed.set_image(url=image.url)
        else:
            embed = discord.Embed(
                title="Error",
                description="Request failed, please try again later",
                color=discord.Color.red(),
            )

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(ImageCommands(bot), bot.pool)
