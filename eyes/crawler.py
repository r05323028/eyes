'''Eyes crawlers
'''
import abc
from typing import List

import bs4
import requests

from eyes.data import DcardPost, Post, PttPost


class Crawler(abc.ABC):
    '''Crawler base class
    '''
    @abc.abstractmethod
    def crawl_latest_posts(
        self,
        limit: int = 100,
    ) -> List[Post]:
        '''Crawl latest posts

        Args:
            limit (int): limitation number of crawled posts

        Returns:
            List[Post]: list of crawled posts
        '''
        return NotImplemented


class PttCrawler(Crawler):
    '''Ptt Crawler
    '''
    name = 'ptt_crawler'

    def __init__(
        self,
        board: str,
    ):
        self.board = board

    def crawl_latest_posts(
        self,
        limit: int = 100,
    ) -> List[PttPost]:
        ...


class DcardCrawler(Crawler):
    '''Dcard Crawler
    '''
    name = 'dcard_crawler'

    def crawl_latest_posts(
        self,
        limit: int = 100,
    ) -> List[DcardPost]:
        ...
