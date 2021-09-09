'''Eyes dcard db module
'''
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint

from eyes.db import Base, Timestamp


class DcardPost(Base, Timestamp):
    '''Dcard post ORM model
    '''
    __tablename__ = 'dcard_posts'

    id = sa.Column(
        sa.Integer,
        primary_key=True,
    )
    forum_id = sa.Column(
        sa.String(64),
        nullable=False,
    )
    forum_name = sa.Column(
        sa.String(64),
        nullable=False,
    )
    title = sa.Column(
        sa.String(
            64,
            collation='utf8mb4_unicode_ci',
        ),
        nullable=False,
    )
    content = sa.Column(
        MEDIUMTEXT(
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
        ),
        nullable=False,
    )
    school = sa.Column(sa.String(64))
    gender = sa.Column(sa.String(10))
    topics = sa.Column(
        sa.JSON,
        default=[],
    )
    like_count = sa.Column(
        sa.Integer,
        nullable=False,
    )
    reactions = relationship(
        'DcardReaction',
        back_populates='post',
        uselist=True,
        lazy='joined',
    )
    with_nickname = sa.Column(
        sa.Boolean,
        nullable=False,
    )
    anonymous_school = sa.Column(
        sa.Boolean,
        nullable=False,
    )
    anonymous_department = sa.Column(
        sa.Boolean,
        nullable=False,
    )
    media = sa.Column(
        sa.JSON,
        default=[],
    )
    comments = relationship(
        'DcardComment',
        back_populates='post',
        uselist=True,
        lazy='joined',
    )


class DcardReaction(Base, Timestamp):
    '''Dcard reaction ORM model
    '''
    __tablename__ = 'dcard_reactions'
    __table_args__ = (UniqueConstraint(
        'post_id',
        'reaction_id',
        name='pair_key',
    ), )

    id = sa.Column(
        sa.Integer,
        autoincrement=True,
        primary_key=True,
    )
    post_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('dcard_posts.id'),
        nullable=False,
    )
    post = relationship(
        'DcardPost',
        back_populates='reactions',
    )
    reaction_id = sa.Column(
        sa.String(64),
        nullable=False,
    )
    count = sa.Column(
        sa.Integer,
        nullable=False,
    )


class DcardComment(Base, Timestamp):
    '''Dcard comment ORM model
    '''
    __tablename__ = 'dcard_comments'
    __table_args__ = (UniqueConstraint(
        'id',
        'post_id',
        name='pair_key',
    ), )

    id = sa.Column(
        sa.String(64),
        primary_key=True,
    )
    post_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('dcard_posts.id'),
        nullable=False,
    )
    post = relationship(
        'DcardPost',
        back_populates='comments',
    )
    anonymous = sa.Column(
        sa.Boolean,
        nullable=False,
    )
    with_nickname = sa.Column(
        sa.Boolean,
        nullable=False,
    )
    floor = sa.Column(
        sa.Integer,
        nullable=False,
    )
    content = sa.Column(
        MEDIUMTEXT(
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
        ))
    gender = sa.Column(
        sa.String(10),
        nullable=False,
    )
    school = sa.Column(
        sa.String(64),
        nullable=False,
    )
    host = sa.Column(
        sa.Boolean,
        nullable=False,
    )
    like_count = sa.Column(
        sa.Integer,
        nullable=False,
    )


class DcardBoard(Base, Timestamp):
    '''Dcard board ORM model
    '''
    __tablename__ = 'dcard_boards'

    id = sa.Column(
        sa.String(64),
        primary_key=True,
    )
    name = sa.Column(
        sa.String(32),
        nullable=False,
    )
    alias = sa.Column(sa.String(32))
    description = sa.Column(MEDIUMTEXT)
    is_school = sa.Column(sa.Boolean)
