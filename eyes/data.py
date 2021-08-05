'''Eyes data containers
'''
from datetime import datetime
from typing import List, Optional

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

    Attributes:
        post_id (str): post id
        reaction (str): comment reaction
        author (str): comment author
        content (str): comment content
    '''
    post_id: str
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

    Attributes:
        id (str): post id
        title (str): post title
        author (str): post author
        board (str): board name
        content (str): post content
        comments (List[PttComment]): post comments
        url (str): post url
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
