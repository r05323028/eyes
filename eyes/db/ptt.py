'''Eyes ptt db module
'''
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint

from eyes.db import Base, Timestamp


class PttPost(Base, Timestamp):
    '''Ptt post ORM model
    '''
    __tablename__ = 'ptt_posts'

    id = sa.Column(
        sa.String(128),
        primary_key=True,
    )
    title = sa.Column(
        sa.String(
            64,
            collation='utf8mb4_unicode_ci',
        ),
        nullable=False,
    )
    author = sa.Column(
        sa.String(64),
        nullable=False,
    )
    board = sa.Column(
        sa.String(64),
        nullable=False,
    )
    content = sa.Column(
        MEDIUMTEXT(
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
        ),
        nullable=False,
    )
    comments = relationship(
        'PttComment',
        back_populates='post',
        uselist=True,
        lazy='joined',
    )
    url = sa.Column(
        sa.String(128),
        nullable=False,
    )

    @hybrid_property
    def num_comments(self) -> int:
        '''Get number of comments
        '''
        return len(self.comments)


class PttComment(Base, Timestamp):
    '''Ptt comment ORM model
    '''
    __tablename__ = 'ptt_comments'
    __table_args__ = (UniqueConstraint(
        'comment_id',
        'post_id',
        name='pair_key',
    ), )

    id = sa.Column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    comment_id = sa.Column(
        sa.Integer,
        nullable=False,
    )
    post_id = sa.Column(
        sa.String(64),
        sa.ForeignKey('ptt_posts.id'),
        nullable=False,
    )
    post = relationship('PttPost', back_populates='comments')
    reaction = sa.Column(
        sa.String(10),
        nullable=False,
    )
    author = sa.Column(
        sa.String(64),
        nullable=False,
    )
    content = sa.Column(
        MEDIUMTEXT(
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
        ),
        nullable=False,
    )


class PttBoard(Base, Timestamp):
    '''PTT board ORM model
    '''
    __tablename__ = 'ptt_boards'

    id = sa.Column(
        sa.Integer,
        autoincrement=True,
        primary_key=True,
    )
    name = sa.Column(
        sa.String(64),
        primary_key=True,
        nullable=False,
    )
    url = sa.Column(
        sa.String(256),
        nullable=True,
    )