import discord
from discord import app_commands
from discord.ext import commands

from asyncpg import Pool

from main import NimbleNeutrinos
import config
import models


class Image:
    id: str
    user: discord.User
    tags: list[str]
    src: str

    def __init__(self, id: str, user: discord.User, tags: list[str], src: str) -> None:
        self.id = id
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

    @discord.ui.button(label="View on Web", style=discord.ButtonStyle.green)
    async def web_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass  # This function should redirect the user to the web page of the image

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

        return message

    def _post_data(self, ctx: commands.Context, message: discord.Message, tags: list[str]):
        all_tags: list[models.Tag] = self.db.get_tags()
        tag_objects: list[models.Tag] = []

        for tag in tags:
            tag_index = -1
            for i in range(len(all_tags)):
                if tag == all_tags[i].name:
                    tag_index = i
                    break

            new_tag: models.Tag
            if tag_index == -1:
                tag_id = self.db.create_tag(tag)
                new_tag = self.db.get_tag_by_id(tag_id)
            else:
                new_tag = all_tags[i]

            tag_objects.append(new_tag)

        message_id = self.db.create_message(
            discord_id=message.id,
            channel_id=ctx.channel.id,
            user_id=ctx.author.id,
            tags=tag_objects,
        )

        for attachment in message.attachments:
            if attachment.content_type.startswith("image"):
                self.model.create_attachment(
                    discord_id=attachment.id,
                    message_id=message_id,
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
            self._post_data(ctx, image_message, tag_list)

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

    # TODO: Use model functions to search for images with matching tags/user
    # Will happen when the appropriate model functions are integrated
    async def _query_images(self, user: str | None, tags: str | None) -> list[Image]:
        return []

    @app_commands.command(
        name="search",
        description="Search for image using tags (searches through current channel).",
    )
    @app_commands.describe(
        tags="Space separated list of tags to search for (optional)",
        user="Username of the poster of the image (optional)",
    )
    async def search(self, ctx: commands.Context, tags: str | None, user: str | None = None):
        tag_list = (tags if tags else "").split()
        tag_list = [tag.lower() for tag in tag_list]
        images: list[Image] = await self._query_images(user, tags)

        view = ImageSwitcher(images, ctx)
        await view.send_message()


async def setup(bot: NimbleNeutrinos):
    await bot.add_cog(ImageCommands(bot))
