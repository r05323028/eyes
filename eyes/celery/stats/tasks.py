'''Eyes celery stats tasks
'''
from datetime import datetime
from typing import Dict

import sqlalchemy as sa
from sqlalchemy import extract, func
from sqlalchemy.orm import scoped_session, sessionmaker

from celery import Task
from celery.utils.log import get_task_logger
from eyes.celery import app
from eyes.config import MySQLConfig
from eyes.data import stats
from eyes.db.ptt import PttComment, PttPost
from eyes.db.stats import DailySummary, MonthlySummary, SourceType

logger = get_task_logger(__name__)


class StatsTask(Task):
    '''Stats Base Task
    '''
    _sess = None

    def after_return(self, *args, **kwargs):
        '''Callback after finishing a job
        '''
        if self._sess is not None:
            self._sess.close()

    @property
    def sess(self):
        '''Returns SQLAlchemy Session
        '''
        if self._sess is None:
            db_config = MySQLConfig()
            engine = sa.create_engine(
                f'mysql://{db_config.user}:{db_config.password}@{db_config.host}:\
                    {db_config.port}/{db_config.database}?charset=utf8mb4')
            session_factory = sessionmaker(engine)
            self._sess = scoped_session(session_factory)()

        return self._sess


@app.task(
    bind=True,
    base=StatsTask,
)
def ptt_monthly_summary(
    self,
    year,
    month,
) -> Dict:
    '''PTT monthly summary

    Args:
        year (int): year
        month (int): month
    '''
    logger.info(
        'Get monthly summary: %s-%s',
        year,
        month,
    )

    # daily
    daily_summaries = self.sess.query(
        func.year(PttPost.created_at),
        func.month(PttPost.created_at),
        func.day(PttPost.created_at),
        func.count(PttPost.id),
    ).filter(
        func.year(PttPost.created_at) == year,
        func.month(PttPost.created_at) == month,
    ).group_by(
        func.year(PttPost.created_at),
        func.month(PttPost.created_at),
        func.day(PttPost.created_at),
    ).all()

    for year_idx, month_idx, day_idx, num_posts in daily_summaries:
        exist_row = self.sess.query(DailySummary).filter(
            DailySummary.source == SourceType.PTT,
            DailySummary.day == day_idx,
            DailySummary.month == month_idx,
            DailySummary.year == year_idx,
        ).first()

        daily_sum = stats.DailySummary(
            source=SourceType.PTT,
            total_posts=num_posts,
            year=year_idx,
            month=month_idx,
            day=day_idx,
        )

        if exist_row:
            exist_row.total_posts = daily_sum.total_posts
            exist_row.updated_at = datetime.utcnow()
            self.sess.merge(exist_row)
            self.sess.commit()
        else:
            row = DailySummary(
                source=SourceType.PTT,
                total_posts=daily_sum.total_posts,
                year=daily_sum.year,
                month=daily_sum.month,
                day=daily_sum.day,
            )
            self.sess.add(row)
            self.sess.commit()

    # monthly
    total_posts = self.sess.query(PttPost).filter(
        extract('year', PttPost.created_at) == int(year),
        extract('month', PttPost.created_at) == int(month),
    ).count()
    total_comments = self.sess.query(PttComment).filter(
        extract('year', PttComment.created_at) == int(year),
        extract('month', PttComment.created_at) == int(month),
    ).count()

    monthly_sum = stats.MonthlySummary(
        source=SourceType.PTT,
        total_posts=total_posts,
        total_comments=total_comments,
        year=year,
        month=month,
    )

    exist_row = self.sess.query(MonthlySummary).filter(
        MonthlySummary.source == SourceType.PTT,
        MonthlySummary.month == int(month),
        MonthlySummary.year == int(year),
    ).first()

    if exist_row:
        exist_row.total_posts = total_posts
        exist_row.total_comments = total_comments
        exist_row.updated_at = datetime.utcnow()
        self.sess.merge(exist_row)
        self.sess.commit()

    else:
        row = MonthlySummary(
            source=SourceType.PTT,
            total_posts=monthly_sum.total_posts,
            total_comments=monthly_sum.total_comments,
            year=monthly_sum.year,
            month=monthly_sum.month,
        )
        self.sess.add(row)
        self.sess.commit()

    return {
        'year': monthly_sum.year,
        'month': monthly_sum.month,
        'total_posts': monthly_sum.total_posts,
        'total_comments': monthly_sum.total_comments,
    }
