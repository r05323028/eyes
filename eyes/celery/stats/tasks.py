'''Eyes celery stats tasks
'''
from datetime import datetime
from typing import Dict

import sqlalchemy as sa
from sqlalchemy import extract
from sqlalchemy.orm import scoped_session, sessionmaker

import eyes.data as data
from celery import Task
from eyes.celery import app
from eyes.config import MySQLConfig
from eyes.db.ptt import PttComment, PttPost
from eyes.db.stats import MonthlySummary, SourceType


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
    total_posts = self.sess.query(PttPost).filter(
        extract('year', PttPost.created_at) == int(year),
        extract('month', PttPost.created_at) == int(month),
    ).count()
    total_comments = self.sess.query(PttComment).filter(
        extract('year', PttComment.created_at) == int(year),
        extract('month', PttComment.created_at) == int(month),
    ).count()

    summary = data.MonthlySummary(
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
            total_posts=summary.total_posts,
            total_comments=summary.total_comments,
            year=summary.year,
            month=summary.month,
        )
        self.sess.add(row)
        self.sess.commit()

    return {
        'year': summary.year,
        'month': summary.month,
        'total_posts': summary.total_posts,
        'total_comments': summary.total_comments,
    }
