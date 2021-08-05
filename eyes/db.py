'''Eyes db models
'''
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Timestamp:
    '''Timestamp model mixin
    '''
    created_at = sa.Column(
        sa.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at = sa.Column(sa.DateTime)


class PttPost(Base, Timestamp):
    '''Ptt post ORM model
    '''
    __tablename__ = 'ptt_posts'

    id = sa.Column(
        sa.String(64),
        primary_key=True,
    )
    title = sa.Column(
        sa.String(64),
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
        MEDIUMTEXT,
        nullable=False,
    )
    comments = relationship(
        'PttComment',
        backref='ptt_posts',
    )
    url = sa.Column(
        sa.String(128),
        nullable=False,
    )


class PttComment(Base, Timestamp):
    '''Ptt comment ORM model
    '''
    __tablename__ = 'ptt_comments'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    post_id = sa.Column(
        sa.String(64),
        sa.ForeignKey('ptt_posts.id'),
    )
    reaction = sa.Column(
        sa.String(10),
        nullable=False,
    )
    author = sa.Column(
        sa.String(64),
        nullable=False,
    )
    content = sa.Column(
        MEDIUMTEXT,
        nullable=False,
    )


class DcardPost(Base, Timestamp):
    '''Dcard post ORM model
    '''
    __tablename__ = 'dcard_posts'

    id = sa.Column(
        sa.String(64),
        primary_key=True,
    )
    comments = relationship('DcardComment')


class DcardComment(Base, Timestamp):
    '''Dcard comment ORM model
    '''
    __tablename__ = 'dcard_comments'

    id = sa.Column(
        sa.String(64),
        primary_key=True,
    )
    post_id = sa.Column(
        sa.String(64),
        sa.ForeignKey('dcard_posts.id'),
    )
