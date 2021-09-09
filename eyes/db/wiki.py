'''Eyes wiki db module
'''
import sqlalchemy as sa

from eyes.db import Base


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
    alias = sa.Column(
        sa.JSON,
        default=[],
    )
