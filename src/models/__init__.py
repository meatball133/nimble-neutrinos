from config.db import get_session
from .content import Content
from .tags import Tag
from sqlalchemy import select
from typing import List, NoReturn

class Model:
    def __init__(self):
        self.session = get_session()

    def get_content(self) -> List[Content]:
        stmt = select(Content)
        return self.session.scalars(stmt)
    
    def get_content_by_id(self, id: int) -> Content :
        stmt = select(Content).where(Content.id == id)
        return self.session.scalars(stmt).one()
    
    def create_content(self, content: str, name: str, tags: List[Tag]) -> int:
        new_content = Content(content=content, name=name, tags=tags)
        self.session.add(new_content)
        self.session.commit()
        return new_content.id

    def update_content(self, id: int, content: str, name: str, tags: List[Tag]) -> NoReturn:
        stmt = select(Content).where(Content.id == id)
        content = self.session.scalar(stmt)
        content.content = content
        content.name = name
        content.tags = tags
        self.session.commit()

    def delete_content(self, id: int) -> NoReturn:
        stmt = select(Content).where(Content.id == id)
        content = self.session.scalar(stmt)
        self.session.delete(content)
        self.session.commit()
   
    def get_tags(self) -> List[Tag]:
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
