'''Eyes crawlers
'''
import abc
import logging
import os
import re
from datetime import datetime
from typing import List

import bs4
import requests
from lxml import etree

from eyes.data import DcardComment, DcardPost, Post, PttComment, PttPost

PTT_OVER_18_BOARDS = [
    'Gossiping',
]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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

    def get_post_id(
        self,
        url: str,
    ) -> str:
        '''Get post id by url

        Args:
            url (str): post url

        Returns:
            str: post id
        '''
        return os.path.basename(url).replace('.html', '')

    def crawl_post(
        self,
        url: str,
    ) -> PttPost:
        '''Crawl a ptt post into a PttPost

        Args:
            url (str): a post url

        Returns:
            PttPost: ptt post data container
        '''
        logger.info('Crawl %s', url)
        cookies = {}

        if self.board in PTT_OVER_18_BOARDS:
            cookies.update({
                'over18': '1',
            })

        resp = requests.get(url, cookies=cookies)
        soup = bs4.BeautifulSoup(resp.content, 'html.parser')
        dom = etree.HTML(str(soup))

        # article meta
        author = dom.xpath('//*[@id="main-content"]/div[1]/span[2]/text()')[0]
        board = dom.xpath('//*[@id="main-content"]/div[2]/span[2]/text()')[0]
        title = dom.xpath('//*[@id="main-content"]/div[3]/span[2]/text()')[0]
        post_created_at = dom.xpath(
            '//*[@id="main-content"]/div[4]/span[2]/text()')[0]
        post_created_at = datetime.strptime(
            post_created_at,
            '%a %b  %d %H:%M:%S %Y',
        )

        # content
        content = dom.xpath('//*[@id="main-content"]/text()')[0]

        # comments
        comments = []
        comments_etree = dom.xpath('//div[@class="push"]')

        for com in comments_etree:
            span = com.xpath('span')
            comment_created_at = re.findall(
                '[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}', span[3].text)[0]
            comment_created_at = datetime.strptime(
                comment_created_at,
                '%m/%d %H:%M',
            )
            comment_created_at = comment_created_at.replace(
                year=datetime.now().year)

            comments.append(
                PttComment(
                    reaction=span[0].text.strip(),
                    author=span[1].text,
                    content=span[2].text[2:],
                    created_at=comment_created_at,
                ))

        # post
        post = PttPost(
            id=self.get_post_id(resp.url),
            title=title,
            author=author,
            board=board,
            content=content,
            comments=comments,
            created_at=post_created_at,
            url=resp.url,
        )

        return post

    def crawl_latest_posts(
        self,
        limit: int = 100,
    ) -> List[PttPost]:
        '''Crawl latest N posts

        Args:
            limit (int): limitation number of posts

        Returns:
            List[PttPost]: a list of ptt data containers
        '''
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
