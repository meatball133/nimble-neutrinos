import discord
from discord import app_commands
from discord.ext import commands

from discord.ui import View

from src.bot.main import CordPicsBot
import src.bot.config
from src import models


class Image:
    user: discord.User
    tags: list[str]
    src: str

    def __init__(self, user: discord.User, tags: list[str], src: str) -> None:
        self.user = user
        self.tags = tags
        self.src = src

    def get_embed(self) -> discord.Embed:
        embed = discord.Embed(color=discord.Color.blurple())

        embed.set_author(name=self.user.name)
        embed.add_field(name="Tags", value=f"*{", ".join(self.tags)}*")
        embed.set_image(url=self.src)

        return embed


class ImageSwitcher(discord.ui.View):
    cur_image: int = 0
    image_count: int
    interaction: discord.Interaction
    images: list[Image]

    def __init__(self, images: list[Image], ctx: commands.Context, timeout: float = 300.0):
        self.images = images
        self.image_count = len(images)
        self.interaction = ctx.interaction
        super().__init__(timeout=timeout)

    async def send_message(self):
        await self.interaction.response.send_message(
            embed=self.images[self.cur_image].get_embed(),
            view=self,
        )

    async def _edit_message(self):
        await self.interaction.edit_original_response(
            embed=self.images[self.cur_image].get_embed(),
            view=self,
        )

    @discord.ui.button(label="Back", style=discord.ButtonStyle.blurple)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.cur_image = (self.cur_image - 1) % self.image_count
        await self._edit_message()
        await interaction.response.defer()

    @discord.ui.button(label="Forward", style=discord.ButtonStyle.blurple)
    async def forward(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.cur_image = (self.cur_image + 1) % self.image_count
        await self._edit_message()
        await interaction.response.defer()


class ImageCommands(commands.Cog):
    db: models.Model = models.Model()
    bot: CordPicsBot

    def __init__(self, bot: CordPicsBot):
        self.bot = bot

    async def _get_last_image(self, ctx: commands.Context) -> discord.Message | None:
        messages = ctx.channel.history(limit=50)
        message: discord.Message | None = None
        attachments: list[discord.Attachment] = []
        only_images: bool = False

        i: int = 0
        while i < len(messages) and not (len(attachments) > 0 and only_images and message.author.id == ctx.author.id):
            message = await messages.__anext__()
            attachments = message.attachments

            only_images = True
            for attachment in attachments:
                if not attachment.content_type.startswith("image"):
                    only_images = False

            i += 1

        return None if i == len(messages) else message

    def _post_tags(self, ctx: commands.Context, message: discord.Message, tags: list[str]):
        tag_objects: list[models.Tag] = []

        for tag in tags:
            new_tag: models.Tag
            result: models.Tag | None = self.db.get_tag_by_name(tag)

            if result is None:
                tag_id = self.db.create_tag(tag)
                new_tag = self.db.get_tag_by_id(tag_id)
            else:
                new_tag = result

            tag_objects.append(new_tag)

        db_message: models.Message = self.db.get_message_by_discord_id(message.id)

        self.db.update_message(
            id=db_message.id,
            discord_id=db_message.discord_id,
            channel_id=db_message.channel_id,
            user_id=db_message.user_id,
            tags=tag_objects,
            favorite=db_message.favorite,
        )

    @app_commands.command(
        name="addtags",
        description="Add tags to the last image sent by you in this channel. (Max. 50 messages ago)",
    )
    @app_commands.describe(tags="Space separated list of tags")
    async def add_tags(self, ctx: commands.Context, tags: str):
        image_message: discord.Message | None = await self._get_last_image(ctx)

        if image_message is None:
            embed = discord.Embed(
                title="No Image Found",
                description="Has the image been posted over 50 messages ago / in another channel?",
                color=discord.Color.red(),
            )
            await ctx.reply(embed=embed)
            return

        tag_list = [tag.lower() for tag in tags.split()]

        embed: discord.Embed

        try:
            self._post_tags(ctx, image_message, tag_list)

            embed = discord.Embed(
                title="Image(s) Added!",
                description=f"Tags: *{", ".join(tag_list)}*",
                color=discord.Color.blurple(),
            )
            image_url = image_message.attachments[0].url
            embed.set_image(url=image_url)

        except Exception:
            embed = discord.Embed(
                title="Error",
                description="Request failed, please try again later",
                color=discord.Color.red(),
            )

        await ctx.reply(embed=embed)

    async def _get_images_with_tags(self, ctx: commands.Context, str_tags: str) -> list[Image]:
        tags = [self.db.get_tag_by_name(tag.lower()) for tag in str_tags]

        messages: list[models.Message] = self.db.get_messages_with_tags(tags, ctx.channel.id)
        images: list[Image] = []

        for message in messages:
            discord_message = await ctx.fetch_message(message.discord_id)

            images += [
                Image(
                    user=discord_message.author,
                    tags=[tag.name for tag in message.tags],
                    src=attachment.url,
                )
                for attachment in discord_message.attachments
                if attachment.content_type.startswith("image")
            ]

        return images

    @app_commands.command(
        name="search",
        description="Search for image using tags (searches through current channel).",
    )
    @app_commands.describe(
        tags="Space separated list of tags to search for",
    )
    async def search(self, ctx: commands.Context, tags: str):
        tag_list = tags.split()
        images: list[Image] = await self._get_images_with_tags(ctx, tag_list)

        view = ImageSwitcher(images, ctx)
        await view.send_message()

    @app_commands.command(name="pics", description="View this channel's images on the cordpics website")
    async def pics(self, ctx: commands.Context):
        db_channel = self.db.get_channel_by_discord_id(ctx.channel.id)
        link = f"{getenv("HOME_URL")}/view?channel_id={db_channel.id}"

        embed = discord.Embed(
            color=discord.Color.green(),
            title="View channel in cordpics",
            description=link,
        )

        ctx.reply(embed=embed)


async def setup(bot: CordPicsBot):
    await bot.add_cog(ImageCommands(bot))
