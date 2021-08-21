'''Eyes job
'''
import enum
import time
import random
from typing import Callable, Dict, Optional

import pydantic

from eyes.crawler.ptt import crawl_post_urls
from eyes.crawler.dcard import crawl_post_ids
from eyes.tasks import crawl_dcard_board_list, crawl_dcard_post, crawl_ptt_post, crawl_ptt_board_list


class JobType(enum.Enum):
    '''Eyes job type
    '''
    # crawler jobs
    CRAWL_PTT_LATEST_POSTS = enum.auto()
    CRAWL_PTT_BOARD_LIST = enum.auto()
    CRAWL_DCARD_LATEST_POSTS = enum.auto()
    CRAWL_DCARD_BOARD_LIST = enum.auto()


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
        if values['job_type'] == JobType.CRAWL_PTT_LATEST_POSTS:
            if not v:
                raise Exception("payload is required")

            for key in ['board']:
                if key not in v:
                    raise Exception(f'{key} is required in payload')

        if values['job_type'] == JobType.CRAWL_PTT_BOARD_LIST:
            if not v:
                raise Exception("payload is required")

            for key in ['top_n']:
                if key not in v:
                    raise Exception(f'{key} is required in payload')
        return v


class Jobs:
    '''Job dispatcher class
    '''
    @property
    def job_map(self) -> Dict[JobType, Callable]:
        '''Return job map
        '''
        return {
            JobType.CRAWL_PTT_LATEST_POSTS: self.crawl_ptt_latest_posts,
            JobType.CRAWL_PTT_BOARD_LIST: self.crawl_ptt_board_list,
            JobType.CRAWL_DCARD_LATEST_POSTS: self.crawl_dcard_latest_posts,
            JobType.CRAWL_DCARD_BOARD_LIST: self.crawl_dcard_board_list,
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
