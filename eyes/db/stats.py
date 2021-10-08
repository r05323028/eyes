'''Eyes stats db module
'''
import enum

import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy_utils.types import ChoiceType

from eyes.db import Base, Timestamp
from eyes.type import SourceType


class MonthlySummary(Base, Timestamp):
    '''Monthly summary ORM model
    '''
    __tablename__ = 'stats_monthly_summaries'
    __table_args__ = (UniqueConstraint(
        'source',
        'year',
        'month',
        name='date_key',
    ), )

    id = sa.Column(
        sa.Integer,
        autoincrement=True,
        primary_key=True,
    )
    source = sa.Column(
        ChoiceType(
            SourceType,
            impl=sa.Integer(),
        ),
        nullable=False,
    )
    total_posts = sa.Column(
        sa.Integer,
        nullable=False,
    )
    total_comments = sa.Column(
        sa.Integer,
        nullable=False,
    )
    year = sa.Column(
        sa.Integer,
        nullable=False,
    )
    month = sa.Column(
        sa.Integer,
        nullable=False,
    )


class DailySummary(Base, Timestamp):
    '''Daily summary ORM model
    '''
    __tablename__ = 'stats_daily_summaries'
    __table_args__ = (UniqueConstraint(
        'source',
        'year',
        'month',
        'day',
        name='date_key',
    ), )

    id = sa.Column(
        sa.Integer,
        autoincrement=True,
        primary_key=True,
    )
    source = sa.Column(
        ChoiceType(
            SourceType,
            impl=sa.Integer(),
        ),
        nullable=False,
    )
    total_posts = sa.Column(
        sa.Integer,
        nullable=False,
    )
    year = sa.Column(
        sa.Integer,
        nullable=False,
    )
    month = sa.Column(
        sa.Integer,
        nullable=False,
    )
    day = sa.Column(
        sa.Integer,
        nullable=False,
    )


class EntitySummary(Base, Timestamp):
    '''Entity summary ORM model
    '''
    __tablename__ = 'stats_entity_summaries'
    __table_args__ = (UniqueConstraint(
        'name',
        'year',
        'month',
        name='uniq_key',
    ), )

    id = sa.Column(
        sa.Integer,
        autoincrement=True,
        primary_key=True,
    )
    name = sa.Column(
        sa.String(128),
        nullable=False,
    )
    count = sa.Column(
        sa.Integer,
        nullable=False,
    )
    board_stats = sa.Column(
        sa.JSON,
        nullable=False,
    )
    link_stats = sa.Column(
        sa.JSON,
        nullable=False,
    )
    posts = sa.Column(
        sa.JSON,
        nullable=False,
    )
    year = sa.Column(
        sa.Integer,
        nullable=False,
    )
    month = sa.Column(
        sa.Integer,
        nullable=False,
    )
