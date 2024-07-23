from config.db import get_session
from .message import Message
from .tags import Tag
from .user import User
from .attachment import Attachment
from .channel import Channel
from .server import Server

from sqlalchemy import select
from typing import List, NoReturn

class Model:
    def __init__(self):
        self.session = get_session()
   
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
    
    def create_user(self, discord_id: int, access_token: str, refresh_token: str) -> int:
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
        return new_user.id
    
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
    
    def create_message(self, discord_id: int, channel_id: int, author: int, tags: list[int]) -> int:
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

        new_message = Message(discord_id=discord_id, channel_id=channel_id, author=author, tags=tags)
        self.session.add(new_message)
        self.session.commit()
        return new_message.id
    
    def update_message(self, id: int, discord_id: int, channel_id: int, author: int, tags: list[int]) -> NoReturn:
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
        message.author = author
        message.tags = tags
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

    def get_channels(self) -> list[Channel]:
        """
        Get all channels from the database.
        
        Returns:
            list[Channel]: A list of all channels.
        """

        stmt = select(Channel)
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
    
    def create_channel(self, discord_id: int, enabled: bool, server_id: int) -> int:
        """
        Create a new channel.

        Args:
            discord_id (int): The discord id of the channel.
            enabled (bool): Whether the channel should be checked for messages.
            server_id (int): The server id of the channel.
        
        Returns:
            int: The id of the new channel
        """

        new_channel = Channel(discord_id=discord_id, enabled=enabled, server_id=server_id)
        self.session.add(new_channel)
        self.session.commit()
        return new_channel.id
    
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
    
    def create_server(self, discord_id: int) -> int:
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
        return new_server.id
    
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
