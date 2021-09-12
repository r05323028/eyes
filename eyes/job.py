'''Eyes job
'''
import enum
import logging
from typing import Callable, Dict, Optional

import pydantic
import sqlalchemy as sa
from rich.logging import RichHandler
from sqlalchemy.orm import scoped_session, sessionmaker

from eyes.celery.crawler.tasks import (
    crawl_dcard_board_list,
    crawl_dcard_post,
    crawl_ptt_board_list,
    crawl_ptt_post,
    crawl_wiki_entity,
)
from eyes.celery.stats.tasks import ptt_monthly_summary
from eyes.config import MySQLConfig
from eyes.crawler.dcard import crawl_post_ids
from eyes.crawler.entity import crawl_wiki_entity_urls
from eyes.crawler.ptt import crawl_post_urls
from eyes.db.ptt import PttBoard

logger = logging.getLogger(__name__)
logger.addHandler(RichHandler(rich_tracebacks=True))


class JobType(enum.Enum):
    '''Eyes job type
    '''
    # crawler jobs
    CRAWL_PTT_LATEST_POSTS = enum.auto()
    CRAWL_PTT_BOARD_LIST = enum.auto()
    CRAWL_PTT_TOP_BOARD_POSTS = enum.auto()
    CRAWL_DCARD_LATEST_POSTS = enum.auto()
    CRAWL_DCARD_BOARD_LIST = enum.auto()
    CRAWL_WIKI_ENTITIES = enum.auto()

    # stats jobs
    PTT_MONTHLY_SUMMARY = enum.auto()


class Job(pydantic.BaseModel):
    job_type: JobType
    payload: Optional[Dict]

    @pydantic.validator('payload')
    def crawler_payload(
        cls,
        v,
        values,
        **kwargs,
    ):
        '''Crawler payload validate function
        '''
        if not v:
            raise Exception("payload is required")

        if values['job_type'] == JobType.CRAWL_PTT_LATEST_POSTS:
            for key in ['board']:
                if key not in v:
                    raise Exception(f'{key} is required in payload')

        if values['job_type'] == JobType.CRAWL_PTT_BOARD_LIST:
            for key in ['top_n']:
                if key not in v:
                    raise Exception(f'{key} is required in payload')

        if values['job_type'] == JobType.CRAWL_WIKI_ENTITIES:
            for key in ['category_url']:
                if key not in v:
                    raise Exception(f'{key} is required in payload')

        if values['job_type'] == JobType.PTT_MONTHLY_SUMMARY:
            for key in ['year', 'month']:
                if key not in v:
                    raise Exception(f'{key} is required in payload')

        if values['job_type'] == JobType.CRAWL_PTT_TOP_BOARD_POSTS:
            for key in ['n_days']:
                if key not in v:
                    raise Exception(f'{key} is required in payload')

        return v


class Jobs:
    '''Job dispatcher class
    '''
    def __init__(self):
        config = MySQLConfig()
        engine = sa.create_engine(
            f'mysql://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}?charset=utf8mb4'
        )
        session_factory = sessionmaker(engine)
        Session = scoped_session(session_factory)
        self.sess = Session()

    def __del__(self):
        self.sess.close()

    @property
    def job_map(self) -> Dict[JobType, Callable]:
        '''Return job map
        '''
        return {
            JobType.CRAWL_PTT_LATEST_POSTS: self.crawl_ptt_latest_posts,
            JobType.CRAWL_PTT_BOARD_LIST: self.crawl_ptt_board_list,
            JobType.CRAWL_PTT_TOP_BOARD_POSTS: self.crawl_ptt_top_board_posts,
            JobType.CRAWL_DCARD_LATEST_POSTS: self.crawl_dcard_latest_posts,
            JobType.CRAWL_DCARD_BOARD_LIST: self.crawl_dcard_board_list,
            JobType.CRAWL_WIKI_ENTITIES: self.crawl_wiki_entities,
            JobType.PTT_MONTHLY_SUMMARY: self.ptt_monthly_summary,
        }

    def crawl_ptt_latest_posts(
        self,
        job: Job,
    ):
        '''Crawl latest ptt posts

        Args:
            job (Job): crawler job
        '''
        urls = crawl_post_urls(
            job.payload['board'],
            job.payload.get('n_days', None),
        )

        for url in urls:
            crawl_ptt_post.apply_async(args=[url, job.payload['board']])

    def crawl_ptt_board_list(
        self,
        job: Job,
    ):
        '''Crawl ptt board list

        Args:
            job (Job): crawler job
        '''
        crawl_ptt_board_list.apply_async(args=[job.payload['top_n']])

    def crawl_ptt_top_board_posts(
        self,
        job: Job,
    ):
        '''Crawl ptt top board posts

        Args:
            job (Job): crawler job
        '''
        boards = self.sess.query(PttBoard).all()

        for board in boards:
            for url in crawl_post_urls(
                    board.name,
                    job.payload.get('n_days', None),
            ):
                try:
                    crawl_ptt_post.apply_async(args=[url, board.name])
                except IndexError as err:
                    logger.warning('Cookie over18 needed: %s', board)
                    continue

    def crawl_dcard_latest_posts(
        self,
        job: Job,
    ):
        '''Crawl dcard latest posts

        Args:
            job (Job): crawler job
        '''
        post_ids = crawl_post_ids(job.payload['forum_id'])

        for post_id in post_ids:
            crawl_dcard_post.delay(post_id)

    def crawl_dcard_board_list(
        self,
        job: Job,
    ):
        '''Crawl dcard board list

        Args:
            job (Job): crawler job
        '''
        crawl_dcard_board_list.apply_async(args=[job.payload['top_n']])

    def crawl_wiki_entities(
        self,
        job: Job,
    ):
        '''Crawl entities from wikipedia

        Args:
            job (job): crawler job
        '''
        urls = crawl_wiki_entity_urls(job.payload['category_url'])

        for url in urls:
            crawl_wiki_entity.apply_async(args=[url])

    def ptt_monthly_summary(
        self,
        job: Job,
    ):
        '''Summary ptt statistics

        Args:
            job (Job): stats job
        '''
        ptt_monthly_summary.apply_async(args=[
            job.payload['year'],
            job.payload['month'],
        ])

    def dispatch(
        self,
        job: Job,
    ):
        '''Dispatch job

        Args:
            job (Job): Eyes job
        '''
        func = self.job_map[job.job_type]
        func(job)
