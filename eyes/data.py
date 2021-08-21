'''Eyes data containers
'''
from datetime import datetime
from typing import List, Optional, Dict

from pydantic import BaseModel, Field


class DcardReaction(BaseModel):
    '''Dcard reaction Base Model
    '''
    post_id: str
    reaction_id: str
    count: int


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
        comment_id (int): comment id
        post_id (str): post id
        reaction (str): comment reaction
        author (str): comment author
        content (str): comment content
    '''
    comment_id: int
    post_id: str
    reaction: str
    author: str
    content: str


class DcardComment(Comment):
    '''Dcard Post Comment Model
    '''
    id: str
    post_id: str
    anonymous: bool
    with_nickname: bool
    floor: int
    content: str
    gender: str
    school: Optional[str]
    host: bool
    like_count: int


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
    id: int
    forum_id: str
    forum_name: str
    title: str
    content: str
    school: Optional[str]
    gender: str
    topics: List[str]
    like_count: int
    reactions: List[DcardReaction] = Field([])
    with_nickname: bool
    anonymous_school: bool
    anonymous_department: bool
    media: List[Dict] = Field([])
    comments: List[DcardComment] = Field([])


class Board(BaseModel):
    '''Board base model

    Attributes:
        name (str): board name
    '''
    name: str


class PttBoard(Board):
    '''PTT Board

    Attributes:
        url (str): board url
    '''
    url: str


class DcardBoard(Board):
    '''Dcard Board

    Attributes:
        id (str): forum id
        alias (str): forum alias
        description (str): forum description
        is_school (bool): whether this forum is school board
        created_at (datetime): forum created time
        updated_at (datetime): forum updated time
    '''
    id: str
    alias: str
    description: str
    is_school: bool
    created_at: datetime
    updated_at: datetime
