'''Eyes job
'''
import enum
import logging
import os
import time
from operator import itemgetter
from typing import Callable, Dict, Optional

import pydantic
import sqlalchemy as sa
from rich.logging import RichHandler
from sqlalchemy import exists, extract
from sqlalchemy.orm import scoped_session, sessionmaker

from celery import group
from eyes.celery.crawler.tasks import (
    crawl_dcard_board_list,
    crawl_dcard_post,
    crawl_ptt_board_list,
    crawl_ptt_post,
    crawl_wiki_entity,
)
from eyes.celery.ml.tasks import transform_ptt_post_to_spacy_post
from eyes.celery.stats.tasks import ptt_monthly_summary, stats_entity_summary
from eyes.config import EyesConfig, MySQLConfig
from eyes.crawler.dcard import crawl_post_ids
from eyes.crawler.entity import crawl_wiki_entity_urls
from eyes.crawler.ptt import crawl_post_urls
from eyes.db.ptt import PttBoard, PttPost
from eyes.db.spacy import SpacyPttPost
from eyes.type import Label

logger = logging.getLogger(__name__)
logger.addHandler(RichHandler(rich_tracebacks=True))
logger.setLevel(logging.INFO)

SLEEP_INTERVAL = 1


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
    ENTITY_MONTHLY_SUMMARY = enum.auto()

    # ml jobs
    PTT_SPACY_PIPELINE = enum.auto()


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

        if values['job_type'] in [
                JobType.PTT_MONTHLY_SUMMARY,
                JobType.PTT_SPACY_PIPELINE,
        ]:
            for key in ['year', 'month', 'overwrite']:
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

        self.config = EyesConfig.from_yaml(
            os.environ.get("EYES_CONFIG_PATH", './config/eyes.yaml'))

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
            JobType.ENTITY_MONTHLY_SUMMARY: self.entity_monthly_summary,
            JobType.PTT_SPACY_PIPELINE: self.ptt_spacy_pipeline,
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

        # for url in urls:
        #     crawl_ptt_post.apply_async(args=[url, job.payload['board']])

        grp = group(
            [crawl_ptt_post.s(url, job.payload['board']) for url in urls])
        res_group = grp.apply_async()
        while not res_group.ready():
            time.sleep(SLEEP_INTERVAL)

    def crawl_ptt_board_list(
        self,
        job: Job,
    ):
        '''Crawl ptt board list

        Args:
            job (Job): crawler job
        '''
        res = crawl_ptt_board_list.delay(job.payload['top_n'])
        res.get()

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
            grp = group([
                crawl_ptt_post.s(url, board.name) for url in crawl_post_urls(
                    board.name,
                    job.payload.get('n_days', None),
                )
            ])
            res_grp = grp.apply_async()
            while not res_grp.ready():
                time.sleep(SLEEP_INTERVAL)

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
        res = crawl_dcard_board_list.delay(job.payload['top_n'])
        res.get()

    def crawl_wiki_entities(
        self,
        job: Job,
    ):
        '''Crawl entities from wikipedia

        Args:
            job (job): crawler job
        '''
        categories = self.config.wiki['categories']

        for category in categories:
            logger.info(category['urls'])
            c_type = Label[category['type']]
            c_urls = category['urls']
            for c_url in c_urls:
                logger.info(
                    "Crawl urls: %s",
                    c_url,
                )
                entity_urls = crawl_wiki_entity_urls(c_url)
                grp = group(
                    crawl_wiki_entity.s(url, c_type.value)
                    for url in entity_urls)
                res_grp = grp.apply_async()
                while not res_grp.ready():
                    time.sleep(SLEEP_INTERVAL)

    def ptt_monthly_summary(
        self,
        job: Job,
    ):
        '''Summary ptt statistics

        Args:
            job (Job): stats job
        '''
        res = ptt_monthly_summary.delay(
            job.payload['year'],
            job.payload['month'],
        )
        res.get()

    def entity_monthly_summary(
        self,
        job: Job,
    ):
        '''Summary entity statistics

        Args:
            job (Job): stats job
        '''
        year, month = itemgetter('year', 'month')(job.payload)
        res = stats_entity_summary.delay(year, month)
        res.get()

    def ptt_spacy_pipeline(
        self,
        job: Job,
    ):
        '''Run ptt post to spacy doc transforming

        Args:
            job (Job): ml job
        '''
        year, month, overwrite = itemgetter('year', 'month',
                                            'overwrite')(job.payload)
        stmt = self.sess.query(PttPost.id).filter(
            extract('year', PttPost.created_at) == year,
            extract('month', PttPost.created_at) == month,
        )
        if not overwrite:
            stmt = stmt.filter(~exists().where(PttPost.id == SpacyPttPost.id))
        rows = stmt.all()
        grp = group(transform_ptt_post_to_spacy_post.s(row[0]) for row in rows)
        res_grp = grp.apply_async()
        while not res_grp.ready():
            time.sleep(SLEEP_INTERVAL)

    def dispatch(
        self,
        job: Job,
    ):
        '''Dispatch job

        Args:
            job (Job): Eyes job
        '''
        start = time.time()
        func = self.job_map[job.job_type]
        func(job)
        end = time.time()
        logger.info(
            '%s: All tasks were ready. Cost %s s',
            job.job_type,
            round(end - start, 3),
        )
