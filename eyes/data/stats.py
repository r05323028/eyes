'''Eyes stats data module
'''
from datetime import date, datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from eyes.db import stats
from eyes.type import SourceType


class MonthlySummary(BaseModel):
    '''Monthly summary data container
    '''
    source: SourceType
    total_posts: int
    total_comments: int
    year: int
    month: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_orm(self) -> stats.MonthlySummary:
        '''Transform to ORM model

        Returns:
            stats.MonthlySummary
        '''
        return stats.MonthlySummary(
            source=self.source,
            total_posts=self.total_posts,
            total_comments=self.total_comments,
            year=self.year,
            month=self.month,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class DailySummary(BaseModel):
    '''Daily summary data container
    '''
    source: SourceType
    total_posts: int
    year: int
    month: int
    day: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_orm(self) -> stats.DailySummary:
        '''Transform to ORM model

        Returns:
            stats.DailySummary
        '''
        return stats.DailySummary(
            source=self.source,
            total_posts=self.total_posts,
            year=self.year,
            month=self.month,
            day=self.day,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class EntitySummary(BaseModel):
    '''Entity summary data container
    '''
    name: str
    count: int
    board_stats: List[Dict] = Field([])
    link_stats: List[Dict] = Field([])
    posts: List[Dict] = Field([])
    year: int
    month: int
    created_at: datetime
    updated_at: datetime

    class Config:
        '''Pydantic config
        '''
        orm_mode = True

    def to_orm(self) -> stats.EntitySummary:
        '''Transform to ORM model

        Returns:
            stats.EntitySummary
        '''
        return stats.EntitySummary(
            name=self.name,
            count=self.count,
            board_stats=self.board_stats,
            link_stats=self.link_stats,
            posts=self.posts,
            year=self.year,
            month=self.month,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
