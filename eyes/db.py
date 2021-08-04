'''Eyes db models
'''
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.models import Timestamp

Base = declarative_base()


class PttPost(Base, Timestamp):
    '''Ptt post ORM model
    '''
    __tablename__ = 'ptt_posts'

    id = sa.Column(
        sa.String(64),
        primary_key=True,
    )


class PttComment(Base, Timestamp):
    '''Ptt comment ORM model
    '''
    __tablename__ = 'ptt_comments'

    id = sa.Column(sa.String(64), primary_key=True)


class DcardPost(Base, Timestamp):
    '''Dcard post ORM model
    '''
    __tablename__ = 'dcard_posts'

    id = sa.Column(
        sa.String(64),
        primary_key=True,
    )


class DcardComment(Base, Timestamp):
    '''Dcard comment ORM model
    '''
    __tablename__ = 'dcard_comments'

    id = sa.Column(
        sa.String(64),
        primary_key=True,
    )