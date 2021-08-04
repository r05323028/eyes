'''Eyes data containers
'''
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Post(BaseModel):
    '''Post Base Model

    Attributes:
        created_at (datetime)
        updated_at (datetime)
    '''
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class PttPost(Post):
    '''PTT Post Model
    '''


class DcardPost(Post):
    '''Dcard Post Model
    '''
