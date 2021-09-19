'''Eyes ptt data module
'''
from datetime import datetime
from typing import List

from pydantic import Field

from eyes.data import Board, Comment, Post
from eyes.db import ptt


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
