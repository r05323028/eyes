'''Eyes celery stats tasks
'''
from collections import defaultdict
from datetime import date, datetime
from itertools import groupby
from typing import Dict

import spacy
import sqlalchemy as sa
from sqlalchemy import extract, func
from sqlalchemy.orm import scoped_session, sessionmaker

from celery import Task
from celery.utils.log import get_task_logger
from eyes.celery import app
from eyes.config import MySQLConfig, SpacyConfig
from eyes.data import stats
from eyes.db.ptt import PttComment, PttPost
from eyes.db.spacy import SpacyPttPost
from eyes.db.stats import DailySummary, EntitySummary, MonthlySummary
from eyes.ml.spacy import binary_to_doc
from eyes.type import SourceType

logger = get_task_logger(__name__)


class StatsTask(Task):
    '''Stats Base Task
    '''
    _sess = None
    _nlp = None

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

    @property
    def nlp(self):
        '''Returns spacy language model
        '''
        if self._nlp is None:
            config = SpacyConfig()
            nlp = spacy.load(config.name)
            self._nlp = nlp

        return self._nlp


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
            try:
                self.sess.commit()
            except:
                logger.warning(
                    "Commit failed on %s, %s, will call session.rollback()",
                    year,
                    month,
                )
                self.sess.rollback()

        else:
            row = DailySummary(
                source=SourceType.PTT,
                total_posts=daily_sum.total_posts,
                year=daily_sum.year,
                month=daily_sum.month,
                day=daily_sum.day,
            )
            self.sess.add(row)
            try:
                self.sess.commit()
            except:
                logger.warning(
                    "Commit failed on %s, %s, will call session.rollback()",
                    year,
                    month,
                )
                self.sess.rollback()

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
        try:
            self.sess.commit()
        except:
            logger.warning(
                "Commit failed on %s, %s, will call session.rollback()",
                year,
                month,
            )
            self.sess.rollback()

    else:
        row = MonthlySummary(
            source=SourceType.PTT,
            total_posts=monthly_sum.total_posts,
            total_comments=monthly_sum.total_comments,
            year=monthly_sum.year,
            month=monthly_sum.month,
        )
        self.sess.add(row)
        try:
            self.sess.commit()
        except:
            logger.warning(
                "Commit failed on %s, %s, will call session.rollback()",
                year,
                month,
            )
            self.sess.rollback()

    return {
        'year': monthly_sum.year,
        'month': monthly_sum.month,
        'total_posts': monthly_sum.total_posts,
        'total_comments': monthly_sum.total_comments,
    }


@app.task(
    bind=True,
    base=StatsTask,
)
def stats_entity_summary(
    self,
    year,
    month,
    limit=None,
) -> Dict:
    '''Entity stats
    '''
    entities = set()
    count = defaultdict(int)
    board_stats = defaultdict(int)
    link_stats = defaultdict(dict)
    posts = defaultdict(set)

    query = self.sess.query(
        SpacyPttPost,
        PttPost.board,
    ).filter(
        PttPost.id == SpacyPttPost.id,
        func.year(SpacyPttPost.created_at) == year,
        func.month(SpacyPttPost.created_at) == month,
    ).order_by(PttPost.created_at.desc())
    if limit:
        logger.warning('Set limit %s', limit)
        query = query.limit(limit)

    for row in query:
        spacy_post, board = row
        row_date = spacy_post.created_at.date()
        title = binary_to_doc(spacy_post.title, self.nlp)
        content = binary_to_doc(spacy_post.content, self.nlp)
        comments = [
            binary_to_doc(com.content, self.nlp) for com in spacy_post.comments
        ]

        for i, ent in enumerate(title.ents):
            ent = ent.text.strip()
            if ent not in entities:
                entities.add(ent)

            # count stats
            count[ent] += 1

            # board stats
            board_stats[(ent, board, row_date)] += 1

            # link stats
            other_ents = [
                e.text.strip() for j, e in enumerate(title.ents) if i != j
            ]
            for other_ent in other_ents:
                if other_ent not in link_stats[ent]:
                    link_stats[ent][other_ent] = 1
                else:
                    link_stats[ent][other_ent] += 1

            # post stats
            posts[ent].add(spacy_post.id)

        for i, ent in enumerate(content.ents):
            ent = ent.text.strip()
            if ent not in entities:
                entities.add(ent)

            # count stats
            count[ent] += 1

            # board stats
            board_stats[(ent, board, row_date)] += 1

            # link stats
            other_ents = [
                e.text.strip() for j, e in enumerate(content.ents) if i != j
            ]
            for other_ent in other_ents:
                if other_ent not in link_stats[ent]:
                    link_stats[ent][other_ent] = 1
                else:
                    link_stats[ent][other_ent] += 1

            # post stats
            posts[ent].add(spacy_post.id)

        for comment in comments:
            for i, ent in enumerate(comment.ents):
                ent = ent.text.strip()
                if ent not in entities:
                    entities.add(ent)

                # count stats
                count[ent] += 1

                # board stats
                board_stats[(ent, board, row_date)] += 1

                # link stats
                other_ents = [
                    e.text.strip() for j, e in enumerate(comment.ents)
                    if i != j
                ]
                for other_ent in other_ents:
                    if other_ent not in link_stats[ent]:
                        link_stats[ent][other_ent] = 1
                    else:
                        link_stats[ent][other_ent] += 1

                # post stats
                posts[ent].add(spacy_post.id)

    # reshape board stats
    board_stats = dict(sorted(
        board_stats.items(),
        key=lambda x: x[0][0],
    ))
    ent_board_stats = defaultdict(list)
    for e_name, e_group in groupby(
            board_stats.items(),
            key=lambda x: x[0][0],
    ):
        ent_board_stats[e_name] = [{
            'source': SourceType.PTT.name,
            'board': key[1],
            'dt': key[2].strftime('%Y-%m-%d'),
            'count': value,
        } for key, value in e_group]

    # transform to orm and upsert
    for ent in entities:
        exist_row = self.sess.query(EntitySummary).filter(
            EntitySummary.name == ent,
            EntitySummary.year == year,
            EntitySummary.month == month,
        ).first()

        if exist_row:
            exist_row.count = count[ent]
            exist_row.board_stats = ent_board_stats[ent]
            exist_row.link_stats = [{
                'source': SourceType.PTT.name,
                'entity': ent_name,
                'count': ent_count,
            } for ent_name, ent_count in link_stats[ent].items()]
            exist_row.posts = list(posts[ent])
            exist_row.year = exist_row.created_at.year
            exist_row.month = exist_row.created_at.month
            exist_row.updated_at = datetime.utcnow()
            self.sess.merge(exist_row)
            try:
                self.sess.commit()
            except:
                logger.warning(
                    "Commit failed on %s, will call session.rollback()",
                    ent,
                )
                self.sess.rollback()
        else:
            self.sess.add(
                EntitySummary(
                    name=ent,
                    count=count[ent],
                    board_stats=ent_board_stats[ent],
                    link_stats=[{
                        'source': SourceType.PTT.name,
                        'entity': ent_name,
                        'count': ent_count,
                    } for ent_name, ent_count in link_stats[ent].items()],
                    posts=list(posts[ent]),
                    year=year,
                    month=month,
                ))
            try:
                self.sess.commit()
            except:
                logger.warning(
                    "Commit failed on %s, will call session.rollback()",
                    ent,
                )
                self.sess.rollback()

    return {
        'year': year,
        'month': month,
    }
