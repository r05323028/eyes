'''Eyes db models
'''
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.schema import UniqueConstraint

Base = declarative_base()


class Timestamp:
    '''Timestamp model mixin
    '''
    created_at = sa.Column(
        sa.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at = sa.Column(
        sa.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


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
