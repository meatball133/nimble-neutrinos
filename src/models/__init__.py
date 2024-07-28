from typing import NoReturn

from sqlalchemy import select, ScalarResult, Select

from src.config.db import get_session
from src.models.attachment import Attachment
from src.models.channel import Channel
from src.models.message import Message
from src.models.server import Server
from src.models.tags import Tag
from src.models.user import User



class Model:
    def __init__(self):
        self.session = get_session()

    def close(self) -> NoReturn:
        self.session.close()

    def delete(self) -> NoReturn:
        self.session.query(User).delete()
        self.session.commit()
        self.session.query(Tag).delete()
        self.session.commit()
        self.session.query(Message).delete()
        self.session.commit()
        self.session.query(Attachment).delete()
        self.session.commit()
        self.session.query(Channel).delete()
        self.session.commit()
        self.session.query(Server).delete()
        self.session.commit()

    def get_tags(self) -> list[Tag]:
        """
        Get all tags from the database.

        Returns:
            list[Tag]: A list of all tags.
        """

        stmt = select(Tag)
        return self.session.scalars(stmt)

    def get_tag_by_id(self, id: int) -> Tag:
        """
        Get a tag by its id.

        Args:
            id (int): The id of the tag.

        Returns:
            Tag: The tag with the given id.
        """

        stmt = select(Tag).where(Tag.id == id)
        return self.session.scalars(stmt).one()

    def get_tag_by_name(self, name: str) -> Tag | None:
        """
        Get a tag by its name.

        Args:
            name (str): The name of the tag.

        Returns:
            Tag | None: The tag with the given name or None if it does not exist
        """

        stmt = select(Tag).where(Tag.name == name)
        result = self.session.scalars(stmt)

        return result.one_or_none()

    def create_tag(self, name: str) -> int:
        """
        Create a new tag.

        Args:
            name (str): The name of the tag.

        Returns:
            int: The id of the new tag.
        """

        new_tag = Tag(name=name)
        self.session.add(new_tag)
        self.session.commit()
        return new_tag.id

    def update_tag(self, id: int, name: str) -> NoReturn:
        """
        Update a tag.

        Args:
            id (int): The id of the tag.
            name (str): The new name of the tag.
        """

        stmt = select(Tag).where(Tag.id == id)
        tag = self.session.scalar(stmt)
        tag.name = name
        self.session.commit()

    def delete_tag(self, id: int) -> NoReturn:
        """
        Delete a tag.

        Args:
            id (int): The id of the tag.
        """

        stmt = select(Tag).where(Tag.id == id)
        tag = self.session.scalar(stmt)
        self.session.delete(tag)
        self.session.commit()

    def get_users(self) -> list[User]:
        """
        Get all users from the database.

        Returns:
            list[User]: A list of all users.
        """
        stmt = select(User)
        return self.session.scalars(stmt)

    def get_user_by_discord_id(self, discord_id: int) -> User:
        stmt = select(User).where(User.discord_id == discord_id)
        return self.session.scalars(stmt).one_or_none()

    def get_user_by_id(self, id: int) -> User:
        """
        Get a user by its id.

        Args:
            id (int): The id of the user.

        Returns:
            User: The user with the given id.
        """

        stmt = select(User).where(User.id == id)
        return self.session.scalars(stmt).one()

    def create_user(self, discord_id: int, access_token: str, refresh_token: str) -> User:
        """
        Create a new user.

        Args:
            discord_id (int): The discord id of the user.
            access_token (str): The access token of the user.
            refresh_token (str): The refresh token of the user.

        Returns:
            int: The id of the new user
        """

        new_user = User(discord_id=discord_id, access_token=access_token, refresh_token=refresh_token)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def update_user(self, id: int, discord_id: int, access_token: str, refresh_token: str) -> NoReturn:
        """
        Update a user.

        Args:
            id (int): The id of the user.
            discord_id (int): The discord id of the user.
            access_token (str): The access token of the user.
            refresh_token (str): The refresh token of the user.
        """

        stmt = select(User).where(User.id == id)
        user = self.session.scalar(stmt)
        user.discord_id = discord_id
        user.access_token = access_token
        user.refresh_token = refresh_token
        self.session.commit()

    def delete_user(self, id: int) -> NoReturn:
        """
        Delete a user.

        Args:
            id (int): The id of the user.
        """

        stmt = select(User).where(User.id == id)
        user = self.session.scalar(stmt)
        self.session.delete(user)
        self.session.commit()

    def get_messages(self) -> list[Message]:
        """
        Get all messages from the database.

        Returns:
            list[Message]: A list of all messages.
        """

        stmt = select(Message)
        return self.session.scalars(stmt)

    def get_message_by_id(self, id: int) -> Message:
        """
        Get a message by its id.

        Args:
            id (int): The id of the message.

        Returns:
            Message: The message with the given id.
        """

        stmt = select(Message).where(Message.id == id)
        return self.session.scalars(stmt).one()

    def get_message_by_discord_id(self, discord_id: int) -> Message:
        stmt = select(Message).where(Message.discord_id == discord_id)
        return self.session.scalars(stmt).one_or_none()

    def get_messages_from_channels(self, channel_ids: list[int], count: int, page: int, author_id: int | None = None) -> list[
        Message]:
        stmt: Select = select(Message).filter(Message.channel_id.in_(channel_ids))
        if author_id is not None:
            stmt = stmt.where(Message.user_id == author_id)
        stmt = stmt.offset(page*count).limit(count)
        return self.session.scalars(stmt).all()

    def get_messages_by_tags(self, tags: list[Tag], channel_id: int) -> list[Message]:
        """
        Get messages that contain one or more of the given tags.

        Args:
            tags (list[Tag]): The tags being searched for.
            channel_id (int): The id of the channel being searched.

        Returns:
            list[Message]: The messages with one or more of the given tags.
        """

        tag_ids = [tag.id for tag in tags]

        # Create a statement to select messages
        stmt = (
            select(Message)
            .distinct()
            .select_from(Tag)
            .filter(Tag.id.in_(tag_ids), Message.channel_id == channel_id)
        )

        return list(self.session.scalars(stmt))

    def create_message(self, discord_id: int, channel_id: int, user_id: int, tags: list[Tag], favorite: bool = False) -> Message:
        """
        Create a new message.

        Args:
            discord_id (int): The discord id of the message.
            channel_id (int): The channel id of the message.
            user_id (int): The author of the message.
            tags (list[Tag]): The tags of the message.

        Returns:
            int: The id of the new message
        """

        new_message = Message(discord_id=discord_id, channel_id=channel_id, user_id=user_id, tags=tags, favorite=favorite)

        self.session.add(new_message)
        self.session.commit()
        return new_message

    def update_message(self, id: int, discord_id: int, channel_id: int, user_id: int, tags: list[Tag], favorite : bool = False) -> NoReturn:
        """
        Update a message.

        Args:
            id (int): The id of the message.
            discord_id (int): The discord id of the message.
            channel_id (int): The channel id of the message.
            user_id (int): The author of the message.
            tags (list[Tag]): The tags of the message.
        """

        stmt = select(Message).where(Message.id == id)
        message = self.session.scalar(stmt)
        message.discord_id = discord_id
        message.channel_id = channel_id
        message.user_id = user_id
        message.tags = tags
        message.favorite = favorite
        self.session.commit()

    def delete_message(self, id: int) -> NoReturn:
        """
        Delete a message.

        Args:
            id (int): The id of the message.
        """

        stmt = select(Message).where(Message.id == id)
        message = self.session.scalar(stmt)
        self.session.delete(message)
        self.session.commit()

    def get_attachments(self) -> list[Attachment]:
        """
        Get all attachments from the database.

        Returns:
            list[Attachment]: A list of all attachments.
        """

        stmt = select(Attachment)
        return self.session.scalars(stmt)

    def get_attachment_by_id(self, id: int) -> Attachment:
        """
        Get an attachment by its id.

        Args:
            id (int): The id of the attachment.

        Returns:
            Attachment: The attachment with the given id.
        """

        stmt = select(Attachment).where(Attachment.id == id)
        return self.session.scalars(stmt).one()

    def get_attachments_from_message(self, message_id: int) -> list[Attachment]:
        stmt = select(Attachment).where(Attachment.message_id == message_id)
        return self.session.scalars(stmt).all()

    def create_attachment(self, discord_id: int, message_id: int) -> int:
        """
        Create a new attachment.

        Args:
            discord_id (int): The discord id of the attachment.
            message_id (int): The message id of the attachment.

        Returns:
            int: The id of the new attachment
        """

        new_attachment = Attachment(discord_id=discord_id, message_id=message_id)
        self.session.add(new_attachment)
        self.session.commit()
        return new_attachment.id

    def update_attachment(self, id: int, discord_id: int, message_id: int) -> NoReturn:
        """
        Update an attachment.

        Args:
            id (int): The id of the attachment.
            discord_id (int): The discord id of the attachment.
            message_id (int): The message id of the attachment.
        """

        stmt = select(Attachment).where(Attachment.id == id)
        attachment = self.session.scalar(stmt)
        attachment.discord_id = discord_id
        attachment.message_id = message_id
        self.session.commit()

    def delete_attachment(self, id: int) -> NoReturn:
        """
        Delete an attachment.

        Args:
            id (int): The id of the attachment.
        """

        stmt = select(Attachment).where(Attachment.id == id)
        attachment = self.session.scalar(stmt)
        self.session.delete(attachment)
        self.session.commit()

    def get_channels(self) -> ScalarResult[Channel]:
        """
        Get all channels from the database.

        Returns:
            list[Channel]: A list of all channels.
        """

        stmt = select(Channel)
        return self.session.scalars(stmt)

    def get_channels_in_server(self, server_id: int) -> ScalarResult[Channel]:
        stmt = select(Channel).where(Channel.server_id == server_id)
        return self.session.scalars(stmt)

    def get_channel_by_id(self, id: int) -> Channel:
        """
        Get a channel by its id.

        Args:
            id (int): The id of the channel.

        Returns:
            Channel: The channel with the given id.
        """

        stmt = select(Channel).where(Channel.id == id)
        return self.session.scalars(stmt).one()

    def get_channel_by_discord_id(self, discord_id: int) -> Channel:
        stmt = select(Channel).where(Channel.discord_id == discord_id)
        return self.session.scalars(stmt).one_or_none()

    def create_channel(self, discord_id: int, enabled: bool, server_id: int) -> Channel:
        """
        Create a new server.

        Args:
            discord_id (int): The discord id of the channel.
            enabled (bool): Whether the channel should be checked for messages.
            server_id (int): The server id of the channel.

        Returns:
            int: The id of the new server.
        """
        new_channel = Channel(discord_id=discord_id, enabled=enabled, server_id=server_id)
        self.session.add(new_channel)
        self.session.commit()
        return new_channel

    def update_channel(self, id: int, discord_id: int, enabled: bool, server_id: int) -> NoReturn:
        """
        Update a channel.

        Args:
            id (int): The id of the channel.
            discord_id (int): The discord id of the channel.
            enabled (bool): Whether the channel should be checked for messages.
            server_id (int): The server id of the channel.
        """

        stmt = select(Channel).where(Channel.id == id)
        channel = self.session.scalar(stmt)
        channel.discord_id = discord_id
        channel.enabled = enabled
        channel.server_id = server_id
        self.session.commit()

    def delete_channel(self, id: int) -> NoReturn:
        """
        Delete a channel.

        Args:
            id (int): The id of the channel.
        """

        stmt = select(Channel).where(Channel.id == id)
        channel = self.session.scalar(stmt)
        self.session.delete(channel)
        self.session.commit()

    def get_servers(self) -> list[Server]:
        """
        Get all servers from the database.

        Returns:
            list[Server]: A list of all servers.
        """

        stmt = select(Server)
        return self.session.scalars(stmt)

    def get_server_by_id(self, id: int) -> Server:
        """
        Get a server by its id.

        Args:
            id (int): The id of the server.

        Returns:
            Server: The server with the given id.
        """

        stmt = select(Server).where(Server.id == id)
        return self.session.scalars(stmt).one()

    def get_server_by_discord_id(self, discord_id: int) -> Server:
        stmt = select(Server).where(Server.discord_id == discord_id)
        return self.session.scalars(stmt).one_or_none()

    def create_server(self, discord_id: int) -> Server:
        """
        Create a new server.

        Args:
            discord_id (int): The discord id of the server.

        Returns:
            int: The id of the new server.
        """
        new_server = Server(discord_id=discord_id)
        self.session.add(new_server)
        self.session.commit()
        return new_server

    def update_server(self, id: int, discord_id: int) -> NoReturn:
        """
        Update a server.

        Args:
            id (int): The id of the server.
            discord_id (int): The discord id of the server.
        """

        stmt = select(Server).where(Server.id == id)
        server = self.session.scalar(stmt)
        server.discord_id = discord_id
        self.session.commit()

    def delete_server(self, id: int) -> NoReturn:
        """
        Delete a server.

        Args:
            id (int): The id of the server.
        """

        stmt = select(Server).where(Server.id == id)
        server = self.session.scalar(stmt)
        self.session.delete(server)
        self.session.commit()

