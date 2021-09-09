'''Eyes data containers
'''
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from eyes.db import dcard, ptt, stats, wiki


class DcardReaction(BaseModel):
    '''Dcard reaction Base Model
    '''
    post_id: str
    reaction_id: str
    count: int

    def to_orm(self) -> dcard.DcardReaction:
        '''Transform to ORM model

        Returns:
            dcard.DcardReaction
        '''
        return dcard.DcardReaction(
            post_id=self.post_id,
            reaction_id=self.reaction_id,
            count=self.count,
        )


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

    def to_orm(self) -> ptt.PttComment:
        '''Transform to ORM model

        Returns:
            ptt.PttComment
        '''
        return ptt.PttComment(
            comment_id=self.comment_id,
            post_id=self.post_id,
            reaction=self.reaction,
            author=self.author,
            content=self.content,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )


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

    def to_orm(self) -> dcard.DcardComment:
        '''Transform to ORM model

        Returns:
            dcard.DcardComment
        '''
        return dcard.DcardComment(
            id=self.id,
            post_id=self.post_id,
            anonymous=self.anonymous,
            with_nickname=self.with_nickname,
            floor=self.floor,
            content=self.content,
            gender=self.gender,
            school=self.school,
            host=self.host,
            like_count=self.like_count,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


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

    def to_orm(self) -> ptt.PttPost:
        '''Transform to ORM model

        Returns:
            ptt.PttPost
        '''
        return ptt.PttPost(
            id=self.id,
            title=self.title,
            author=self.author,
            board=self.board,
            content=self.content,
            comments=[comment.to_orm() for comment in self.comments],
            url=self.url,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


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

    def to_orm(self) -> dcard.DcardPost:
        '''Transform to ORM model

        Returns:
            dcard.DcardPost
        '''
        return dcard.DcardPost(
            id=self.id,
            forum_id=self.forum_id,
            forum_name=self.forum_name,
            title=self.title,
            content=self.content,
            school=self.school,
            gender=self.gender,
            topics=self.topics,
            like_count=self.like_count,
            reactions=[react.to_orm() for react in self.reactions],
            with_nickname=self.with_nickname,
            anonymous_school=self.anonymous_school,
            anonymous_department=self.anonymous_department,
            media=self.media,
            comments=[comment.to_orm() for comment in self.comments],
        )


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

    def to_orm(self) -> ptt.PttBoard:
        '''Transform to ORM model

        Returns:
            ptt.PttBoard
        '''
        return ptt.PttBoard(
            url=self.url,
            name=self.name,
        )


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

    def to_orm(self) -> dcard.DcardBoard:
        '''Transform to ORM model

        Returns:
            dcard.DcardBoard
        '''
        return dcard.DcardBoard(
            id=self.id,
            name=self.name,
            alias=self.alias,
            is_school=self.is_school,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


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


class MonthlySummary(BaseModel):
    '''Monthly summary data container
    '''
    source: stats.SourceType
    total_posts: int
    total_comments: int
    year: int
    month: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_orm(self) -> stats.MonthlySummary:
        '''Transform to ORM model

        Returns:
            stats.MonthlySummary
        '''
        return stats.MonthlySummary(
            source=self.source,
            total_posts=self.total_posts,
            total_comments=self.total_comments,
            year=self.year,
            month=self.month,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
