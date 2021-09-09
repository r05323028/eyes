'''Eyes db models
'''
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

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
