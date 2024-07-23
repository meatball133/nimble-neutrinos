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
        stmt = select(Tag)
        return self.session.scalars(stmt)
    
    def get_tag_by_id(self, id: int) -> Tag:
        stmt = select(Tag).where(Tag.id == id)
        return self.session.scalars(stmt).one()
    
    def create_tag(self, name: str) -> int:
        new_tag = Tag(name=name)
        self.session.add(new_tag)
        self.session.commit()
        return new_tag.id
    
    def update_tag(self, id: int, name: str) -> NoReturn:
        stmt = select(Tag).where(Tag.id == id)
        tag = self.session.scalar(stmt)
        tag.name = name
        self.session.commit()

    def delete_tag(self, id: int) -> NoReturn:
        stmt = select(Tag).where(Tag.id == id)
        tag = self.session.scalar(stmt)
        self.session.delete(tag)
        self.session.commit()

    def get_users(self) -> list[User]:
        stmt = select(User)
        return self.session.scalars(stmt)
    
    def get_user_by_id(self, id: int) -> User:
        stmt = select(User).where(User.id == id)
        return self.session.scalars(stmt).one()
    
    def create_user(self, discord_id: int, access_token: str, refresh_token: str) -> int:
        new_user = User(discord_id=discord_id, access_token=access_token, refresh_token=refresh_token)
        self.session.add(new_user)
        self.session.commit()
        return new_user.id
    
    def update_user(self, id: int, discord_id: int, access_token: str, refresh_token: str) -> NoReturn:
        stmt = select(User).where(User.id == id)
        user = self.session.scalar(stmt)
        user.discord_id = discord_id
        user.access_token = access_token
        user.refresh_token = refresh_token
        self.session.commit()

    def delete_user(self, id: int) -> NoReturn:
        stmt = select(User).where(User.id == id)
        user = self.session.scalar(stmt)
        self.session.delete(user)
        self.session.commit()

    def get_messages(self) -> list[Message]:
        stmt = select(Message)
        return self.session.scalars(stmt)
    
    def get_message_by_id(self, id: int) -> Message:
        stmt = select(Message).where(Message.id == id)
        return self.session.scalars(stmt).one()
    
    def create_message(self, discord_id: int, channel_id: int, author: int, tags: list[int]) -> int:
        new_message = Message(discord_id=discord_id, channel_id=channel_id, author=author, tags=tags)
        self.session.add(new_message)
        self.session.commit()
        return new_message.id
    
    def update_message(self, id: int, discord_id: int, channel_id: int, author: int, tags: list[int]) -> NoReturn:
        stmt = select(Message).where(Message.id == id)
        message = self.session.scalar(stmt)
        message.discord_id = discord_id
        message.channel_id = channel_id
        message.author = author
        message.tags = tags
        self.session.commit()

    def delete_message(self, id: int) -> NoReturn:
        stmt = select(Message).where(Message.id == id)
        message = self.session.scalar(stmt)
        self.session.delete(message)
        self.session.commit()

    def get_attachments(self) -> list[Attachment]:
        stmt = select(Attachment)
        return self.session.scalars(stmt)
    
    def get_attachment_by_id(self, id: int) -> Attachment:
        stmt = select(Attachment).where(Attachment.id == id)
        return self.session.scalars(stmt).one()
    
    def create_attachment(self, discord_id: int, message_id: int) -> int:
        new_attachment = Attachment(discord_id=discord_id, message_id=message_id)
        self.session.add(new_attachment)
        self.session.commit()
        return new_attachment.id
    
    def update_attachment(self, id: int, discord_id: int, message_id: int) -> NoReturn:
        stmt = select(Attachment).where(Attachment.id == id)
        attachment = self.session.scalar(stmt)
        attachment.discord_id = discord_id
        attachment.message_id = message_id
        self.session.commit()

    def delete_attachment(self, id: int) -> NoReturn:
        stmt = select(Attachment).where(Attachment.id == id)
        attachment = self.session.scalar(stmt)
        self.session.delete(attachment)
        self.session.commit()

    def get_channels(self) -> list[Channel]:
        stmt = select(Channel)
        return self.session.scalars(stmt)
    
    def get_channel_by_id(self, id: int) -> Channel:
        stmt = select(Channel).where(Channel.id == id)
        return self.session.scalars(stmt).one()
    
    def create_channel(self, discord_id: int, enabled: bool, server_id: int) -> int:
        new_channel = Channel(discord_id=discord_id, enabled=enabled, server_id=server_id)
        self.session.add(new_channel)
        self.session.commit()
        return new_channel.id
    
    def update_channel(self, id: int, discord_id: int, enabled: bool, server_id: int) -> NoReturn:
        stmt = select(Channel).where(Channel.id == id)
        channel = self.session.scalar(stmt)
        channel.discord_id = discord_id
        channel.enabled = enabled
        channel.server_id = server_id
        self.session.commit()

    def delete_channel(self, id: int) -> NoReturn:
        stmt = select(Channel).where(Channel.id == id)
        channel = self.session.scalar(stmt)
        self.session.delete(channel)
        self.session.commit()

    def get_servers(self) -> list[Server]:
        stmt = select(Server)
        return self.session.scalars(stmt)

    def get_server_by_id(self, id: int) -> Server:
        stmt = select(Server).where(Server.id == id)
        return self.session.scalars(stmt).one()
    
    def create_server(self, discord_id: int) -> int:
        new_server = Server(discord_id=discord_id)
        self.session.add(new_server)
        self.session.commit()
        return new_server.id
    
    def update_server(self, id: int, discord_id: int) -> NoReturn:
        stmt = select(Server).where(Server.id == id)
        server = self.session.scalar(stmt)
        server.discord_id = discord_id
        self.session.commit()

    def delete_server(self, id: int) -> NoReturn:
        stmt = select(Server).where(Server.id == id)
        server = self.session.scalar(stmt)
        self.session.delete(server)
        self.session.commit()
