'''Eyes spacy ORM model
'''
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import LONGBLOB, MEDIUMBLOB
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint

from eyes.db import Base, Timestamp


class SpacyPttPost(Base, Timestamp):
    '''Spacy ptt post ORM model
    '''
    __tablename__ = 'spacy_ptt_posts'
    id = sa.Column(
        sa.String(128),
        primary_key=True,
    )
    title = sa.Column(
        MEDIUMBLOB,
        nullable=False,
    )
    content = sa.Column(
        LONGBLOB,
        nullable=False,
    )
    comments = relationship(
        'SpacyPttComment',
        back_populates='post',
        uselist=True,
        lazy='joined',
    )


class SpacyPttComment(Base, Timestamp):
    '''Spacy ptt comment ORM model
    '''
    __tablename__ = 'spacy_ptt_comments'
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
        sa.ForeignKey('spacy_ptt_posts.id'),
        nullable=False,
    )
    post = relationship(
        'SpacyPttPost',
        back_populates='comments',
    )
    content = sa.Column(
        MEDIUMBLOB,
        nullable=False,
    )
