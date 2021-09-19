'''Eyes dcard data module
'''
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from eyes.data import Board, Comment, Post
from eyes.db import dcard


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
