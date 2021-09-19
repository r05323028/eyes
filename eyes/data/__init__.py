'''Eyes base data module
'''
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from eyes.db import wiki


class Post(BaseModel):
    '''Post Base Model

    Attributes:
        created_at (Optional[datetime])
        updated_at (Optional[datetime])
    '''
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class Comment(BaseModel):
    '''Comment Base Model

    Attributes:
        created_at (Optional[datetime])
        updated_at (Optional[datetime])
    '''
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class Board(BaseModel):
    '''Board base model

    Attributes:
        name (str): board name
    '''
    name: str


class Entity(BaseModel):
    '''Entity base model

    Attributes:
        name (str): name
        type (str): type
        alias (Optional[List[str]]): alias
    '''
    name: str
    type: str
    alias: Optional[List[str]]

    def to_wiki_entity_orm(self) -> wiki.WikiEntity:
        '''Transform to wiki entity ORM

        Returns:
            wiki.WikiEntity
        '''
        return wiki.WikiEntity(
            name=self.name,
            type=self.type,
            alias=self.alias,
        )
