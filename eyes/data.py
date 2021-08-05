'''Eyes data containers
'''
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class Comment(BaseModel):
    '''Comment Base Model

    Attributes:
        created_at (Optional[datetime])
        updated_at (Optional[datetime])
    '''
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class PttComment(Comment):
    '''Ptt Post Comment Model
    '''
    reaction: str
    author: str
    content: str


class DcardComment(Comment):
    '''Dcard Post Comment Model
    '''


class Post(BaseModel):
    '''Post Base Model

    Attributes:
        created_at (Optional[datetime])
        updated_at (Optional[datetime])
    '''
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class PttPost(Post):
    '''PTT Post Model
    '''
    id: str
    title: str
    author: str
    board: str
    content: str
    comments: List[PttComment] = Field([])
    url: str


class DcardPost(Post):
    '''Dcard Post Model
    '''
    comments: List[DcardComment] = Field([])
