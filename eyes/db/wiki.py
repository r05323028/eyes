'''Eyes wiki db module
'''
import sqlalchemy as sa
from sqlalchemy_utils.types import ChoiceType

from eyes.db import Base
from eyes.type import Label


class WikiEntity(Base):
    '''Wiki entities
    '''
    __tablename__ = 'wiki_entities'

    id = sa.Column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    name = sa.Column(
        sa.String(32),
        unique=True,
        nullable=False,
    )
    type = sa.Column(sa.String(32))
    label = sa.Column(ChoiceType(
        Label,
        impl=sa.Integer(),
    ))
    alias = sa.Column(
        sa.JSON,
        default=[],
    )
