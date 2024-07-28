from os import getenv
import discord
from discord import app_commands
from discord.ext import commands

from asyncpg import Pool
from discord.ui import View

from main import NimbleNeutrinos
import models


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

    def __init__(self, images: list[Image], interaction: discord.Interaction, timeout: float = 300.0):
        self.images = images
        self.image_count = len(images)
        self.interaction = interaction
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
    bot: NimbleNeutrinos

    def __init__(self, bot: NimbleNeutrinos):
        self.bot = bot

    def _check_channel_enabled(self, interaction: discord.Interaction) -> bool:
        db_channel = self.db.get_channel_by_discord_id(interaction.channel_id)
        return db_channel.enabled

    def _channel_disabled_embed(self) -> discord.Embed:
        return discord.Embed(
            color=discord.Color.red(),
            title="This channel is disabled",
            description="Use the /enable command to enable CordPics in this channel",
        )

    async def _get_last_image(self, interaction: discord.Interaction) -> discord.Message | None:
        messages = interaction.channel.history(limit=50)
        message: discord.Message | None = None
        attachments: list[discord.Attachment] = []
        only_images: bool = False

        i: int = 0
        while i < len(messages) and not (
            len(attachments) > 0 and only_images and message.author.id == interaction.user.id
        ):
            message = await messages.__anext__()
            attachments = message.attachments

            only_images = True
            for attachment in attachments:
                if not attachment.content_type.startswith("image"):
                    only_images = False

            i += 1

        return None if i == len(messages) else message

    def _post_tags(self, message: discord.Message, tags: list[str]):
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

        for attachment in message.attachments:
            if attachment.content_type.startswith("image"):
                self.db.create_attachment(
                    discord_id=attachment.id,
                    message_id=db_message.id,
                )

    @app_commands.command(
        name="addtags",
        description="Add tags to the last image sent by you in this channel. (Max. 50 messages ago)",
    )
    @app_commands.describe(tags="Space separated list of tags")
    async def add_tags(self, interaction: discord.Interaction, tags: str):
        if not self._check_channel_enabled():
            interaction.response.send_message(embed=self._channel_disabled_embed(), ephemeral=True)
            return

        image_message: discord.Message | None = await self._get_last_image(interaction)

        if image_message is None:
            embed = discord.Embed(
                title="No Image Found",
                description="Has the image been posted over 50 messages ago / in another channel?",
                color=discord.Color.red(),
            )
            await interaction.response.send_message(embed=embed)
            return

        tag_list = [tag.lower() for tag in tags.split()]

        embed: discord.Embed

        try:
            self._post_tags(image_message, tag_list)

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

        await interaction.response.send_message(embed=embed)

    async def _get_images_with_tags(self, interaction: discord.Interaction, str_tags: str) -> list[Image]:
        tags = [self.db.get_tag_by_name(tag.lower()) for tag in str_tags]

        messages: list[models.Message] = self.db.get_messages_with_tags(tags, interaction.channel_id)
        images: list[Image] = []

        for message in messages:
            discord_message = await interaction.channel.fetch_message(message.discord_id)

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
    async def search(self, interaction: discord.Interaction, tags: str):
        if not self._check_channel_enabled():
            interaction.repsonse.send_message(embed=self._channel_disabled_embed(), ephemeral=True)
            return

        tag_list = tags.split()
        images: list[Image] = await self._get_images_with_tags(interaction, tag_list)

        view = ImageSwitcher(images, interaction)
        await view.send_message()

    @app_commands.command(name="pics", description="View this channel's images on the cordpics website")
    async def pics(self, interaction: discord.Interaction):
        if not self._check_channel_enabled():
            interaction.response.send_message(embed=self._channel_disabled_embed(), ephemeral=True)
            return

        db_channel = self.db.get_channel_by_discord_id(interaction.channel_id)
        link = f"{getenv("HOME_URL")}/view?channel_id={db_channel.id}"

        embed = discord.Embed(
            color=discord.Color.green(),
            title="View channel in cordpics",
            description=link,
        )

        interaction.response.send_message(embed=embed)

    def update_channel_enabled(self, interaction: discord.Interaction, *, enabled: bool):
        db_channel = self.db.get_channel_by_discord_id(interaction.channel_id)

        self.db.update_channel(
            id=db_channel.id,
            discord_id=db_channel.discord_id,
            enabled=enabled,
            server_id=db_channel.server_id,
        )

    @app_commands.command(name="enable", description="Enable CordPics in this channel")
    async def enable(self, interaction: discord.Interaction):
        self.update_channel_enabled(interaction, enabled=True)
        interaction.response.send_message("CordPics has been enabled in this channel", ephemeral=True)

    @app_commands.command(name="disable", description="Disable CordPics in this channel")
    async def disable(self, interaction: discord.Interaction):
        self.update_channel_enabled(interaction, enabled=False)
        interaction.response.send_message("CordPics has been disabled in this channel", ephemeral=True)


async def setup(bot: NimbleNeutrinos):
    await bot.add_cog(ImageCommands(bot))
