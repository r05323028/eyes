'''PTT crawler module
'''
import logging
import os
import re
from datetime import datetime
from typing import Iterator

import requests
from lxml import etree

from eyes.crawler.utils import get_dom
from eyes.data import PttComment, PttPost

PTT_OVER_18_BOARDS = [
    'Gossiping',
]

PTT_BASE_URL = 'https://www.ptt.cc'

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
    content = dom.xpath('//*[@id="main-content"]/text()')
    content = ''.join(content)

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
                post_id=get_post_id(resp.url),
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


def crawl_post_urls(board: str) -> Iterator[str]:
    '''Crawl latest N post urls

    Args:
        board (str): board name

    Returns:
        Iterator[str]: a list of ptt data containers
    '''
    cookies = {}

    if board in PTT_OVER_18_BOARDS:
        cookies.update({'over18': '1'})

    next_url = f'{PTT_BASE_URL}/bbs/{board}/index.html'
    resp = requests.get(next_url, cookies=cookies)
    dom = get_dom(resp)

    while next_url:
        # get post urls
        logger.info('Page: %s', next_url)
        r_ents = dom.xpath('//*[@class="r-ent"]')

        for row in r_ents:
            href = row.xpath('div[@class="title"]/a/@href')

            if href:
                post_url = href[0]
                yield f'{PTT_BASE_URL}{post_url}'

        next_url = get_next_url(dom)
        resp = requests.get(f'{PTT_BASE_URL}{next_url}', cookies=cookies)
        dom = get_dom(resp)
