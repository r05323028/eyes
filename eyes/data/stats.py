'''Eyes stats data module
'''
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from eyes.db import stats


class MonthlySummary(BaseModel):
    '''Monthly summary data container
    '''
    source: stats.SourceType
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
    source: stats.SourceType
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
