import logging
import os
import re
from datetime import datetime
from typing import List

import requests
from lxml import etree

from eyes.data import PttPost, PttComment
from eyes.crawler.utils import get_dom

PTT_OVER_18_BOARDS = [
    'Gossiping',
]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_post_id(url: str, ) -> str:
    '''Get post id by url

    Args:
        url (str): post url

    Returns:
        str: post id
    '''
    return os.path.basename(url).replace('.html', '')


def crawl_post(
    url: str,
    board: str,
) -> PttPost:
    '''Crawl a ptt post into a PttPost

    Args:
        url (str): a post url
        board (str): board name

    Returns:
        PttPost: ptt post data container
    '''
    logger.info('Crawl %s', url)
    cookies = {}

    if board in PTT_OVER_18_BOARDS:
        cookies.update({
            'over18': '1',
        })

    resp = requests.get(url, cookies=cookies)
    dom = get_dom(resp)

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
        comment_created_at = re.findall('[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}',
                                        span[3].text)[0]
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
        id=get_post_id(resp.url),
        title=title,
        author=author,
        board=board,
        content=content,
        comments=comments,
        created_at=post_created_at,
        url=resp.url,
    )

    return post


def get_next_url(dom: etree.Element) -> str:
    '''Get next page url

    Args:
        dom (etree.Element): current page DOM

    Returns:
        str: next page url
    '''
    return dom.xpath(
        '//*[@id="action-bar-container"]/div/div[2]/a[2]/@href')[0]


def crawl_latest_posts(
    board: str,
    limit: int = 100,
) -> List[PttPost]:
    '''Crawl latest N posts

    Args:
        board (str): board name
        limit (int): limitation number of posts

    Returns:
        List[PttPost]: a list of ptt data containers
    '''
    start = f'https://www.ptt.cc/bbs/{board}/index.html'
    tasks = []

    resp = requests.get(start, cookies={'over18': '1'})
    dom = get_dom(resp)
    next_url = get_next_url(dom)
